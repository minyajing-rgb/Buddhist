#!/usr/bin/env python3
"""Research-only import: metadata, bibliography and locators, never full translations.
Run with --refresh to perform bounded requests to the named public authority repos.
An imported citation is not a claim that a scholar has read or validated that paper.
"""
from __future__ import annotations
import argparse, concurrent.futures, datetime, hashlib, json, pathlib, re, urllib.request, urllib.parse, xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]
NS={'t':'http://www.tei-c.org/ns/1.0'}
XMLID='{http://www.w3.org/XML/1998/namespace}id'

def fetch(url:str, maximum:int=20000000)->bytes:
    req=urllib.request.Request(url,headers={'User-Agent':'DharmaAtlas-MetadataResearch/1.1 (+https://github.com/minyajing-rgb/Buddhist)'})
    with urllib.request.urlopen(req,timeout=35) as response:
        data=response.read(maximum+1)
        if len(data)>maximum: raise ValueError('response exceeds research size limit')
        return data

def text(node):
    return ' '.join(' '.join(node.itertext()).split()) if node is not None else ''

def elements(node,path):
    return list(dict.fromkeys(text(e) for e in node.findall(path,NS) if text(e)))

def parse_tei(data,url,sha,path,provider):
    # Entity resolution is deliberately disabled; XML is parsed as data, not executed.
    r=ET.fromstring(data)
    h=r.find('t:teiHeader',NS)
    if h is None: raise ValueError('no TEI header')
    title_nodes=h.findall('.//t:titleStmt/t:title',NS)
    titles=[{'title':text(n),'type':n.get('type'),'language':n.get('{http://www.w3.org/XML/1998/namespace}lang')} for n in title_nodes]
    refs=[]
    for b in r.findall('.//t:listBibl/t:bibl',NS)+r.findall('.//t:listBibl/t:biblStruct',NS):
        # Bibliographic facts only: no description/abstract or translation text.
        titles_b=elements(b,'.//t:title')
        if not titles_b: continue
        refs.append({'local_id':b.get(XMLID),'titles':titles_b,'authors':elements(b,'.//t:author'),'editors':elements(b,'.//t:editor'),'dates':elements(b,'.//t:date'),'publishers':elements(b,'.//t:publisher'),'places':elements(b,'.//t:pubPlace'),'scope':elements(b,'.//t:biblScope'),'links':list(dict.fromkeys(x.get('target') for x in b.findall('.//t:ref',NS) if x.get('target'))),'source_url':url,'source_locator':('#'+b.get(XMLID)) if b.get(XMLID) else 'listBibl','verification':'authority_bibliography_metadata_imported_not_fulltext_reviewed'})
    # Material edition identifiers/locations are version evidence, not extant autograph claims.
    source_desc=h.find('.//t:sourceDesc',NS)
    edition_evidence=[]
    if source_desc is not None:
        for b in source_desc.findall('.//t:bibl',NS):
            edition_evidence.append({'key':b.get('key'),'id':b.get(XMLID),'titles':elements(b,'.//t:title'),'identifiers':elements(b,'.//t:idno'),'locations':elements(b,'.//t:location'),'scopes':elements(b,'.//t:biblScope')})
    sections=[]
    for d in r.findall('.//t:div',NS):
        typ=d.get('type','')
        if typ in ['introduction','bibliography','acknowledgment','acknowledgements','colophon']:
            sections.append({'type':typ,'id':d.get(XMLID),'paragraphs':len(d.findall('.//t:p',NS))})
    return {'provider':provider,'source_url':url,'source_commit':sha,'source_path':path,'content_sha256':hashlib.sha256(data).hexdigest(),'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'metadata_imported','titles':titles,'authors':elements(h,'.//t:titleStmt/t:author'),'editors':elements(h,'.//t:titleStmt/t:editor'),'edition_evidence':edition_evidence,'publication_dates':elements(h,'.//t:publicationStmt/t:date'),'bibliography':refs,'research_sections':sections,'is_repository_placeholder':'/placeholders/' in path,'rights':'Third-party source retained at provider; only bibliographic facts, identifiers and section locators imported. No source translation or illustration redistributed.','chronology_note':'Publication dates are modern edition/translation metadata, not ancient composition dates.'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--refresh',action='store_true');args=parser.parse_args()
    target=ROOT/'data/authority_metadata_v0.7.json'
    if target.exists() and not args.refresh:
        print('Using cached authority metadata');return
    current=json.loads((ROOT/'data/CURRENT.json').read_text())
    records=json.loads((ROOT/current['canonical_datasets']['deep_crosswalk']).read_text())['records']
    errors=[];jobs=[];snapshots={}
    for repo,branch in [('84000/data-tei','master'),('cbeta-org/xml-p5','master')]:
        try:
            obj=json.loads(fetch(f'https://api.github.com/repos/{repo}/commits/{branch}'))
            snapshots[repo]={'commit':obj['sha'],'commit_date':obj['commit']['committer']['date']}
        except Exception as e: errors.append({'repository':repo,'error':str(e)})
    tree=[]
    if '84000/data-tei' in snapshots:
        sha=snapshots['84000/data-tei']['commit']
        try:
            tree_json=json.loads(fetch(f'https://api.github.com/repos/84000/data-tei/git/trees/{sha}?recursive=1'))
            tree=tree_json.get('tree',[])
            if tree_json.get('truncated'): errors.append({'repository':'84000/data-tei','error':'tree truncated; discovery is incomplete'})
        except Exception as e: errors.append({'repository':'84000/data-tei','error':str(e)})
    for record in records:
        wid=record['work_id']; paths=set()
        # Only explicit IDs are used. Ranges and collections are not expanded into claims of equivalence.
        for route in record.get('authority_routes',[]):
            for code in re.findall(r'T\d{2}n\d{4}[a-z]?',route.get('url','')):
                if 'cbeta-org/xml-p5' in snapshots:
                    path=f'T/{code[:3]}/{code}.xml';sha=snapshots['cbeta-org/xml-p5']['commit']
                    paths.add(('CBETA','cbeta-org/xml-p5',sha,path))
        toh_ids=set(re.findall(r'/translation/toh([0-9]+(?:-[0-9]+)?)', ' '.join(a.get('url','') for a in record.get('authority_routes',[]))))
        if not toh_ids:
            value=str(record.get('canonical_ids',{}).get('toh') or '')
            if re.fullmatch(r'Toh\s+[0-9]+',value): toh_ids.add(re.sub(r'\D','',value))
        for toh in sorted(toh_ids):
            matches=[x for x in tree if x['type']=='blob' and x['path'].endswith('.xml') and x['path'].startswith('translations/') and re.search(r'_toh'+re.escape(toh)+r'(?=[,_-]|\.)',x['path'])]
            # Prevent a chapter matching the containing work; validate XML bibl key below.
            for item in matches[:4]:
                paths.add(('84000','84000/data-tei',snapshots['84000/data-tei']['commit'],item['path']))
        for provider,repo,sha,path in sorted(paths):
            jobs.append((wid,provider,repo,sha,path))
    def run(job):
        wid,provider,repo,sha,path=job
        url=f'https://raw.githubusercontent.com/{repo}/{sha}/'+urllib.parse.quote(path,safe='/,')
        try: return wid,parse_tei(fetch(url),url,sha,path,provider)
        except Exception as e: return wid,{'provider':provider,'source_url':url,'status':'fetch_or_parse_failed','error':str(e)}
    by_work={r['work_id']:[] for r in records}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for wid,result in pool.map(run,jobs): by_work[wid].append(result)
    result={'version':'0.7','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_snapshots':snapshots,'scope':'Exact-ID metadata import for the canonical 100 works; source repository snapshot may lag current publisher website.','rules':['Imported bibliography is a research lead, not a reviewed paper.','Do not infer composition dates from modern publication metadata.','A placeholder is a catalogue entry, not a published translation.','Matching file/ID is not proof of identical cross-language recension.'],'errors':errors,'records':[{'work_id':wid,'imports':imports} for wid,imports in by_work.items()]}
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({'works':len(by_work),'works_with_imports':sum(any(i.get('status')=='metadata_imported' for i in a) for a in by_work.values()),'bibliography_entries':sum(len(i.get('bibliography',[])) for a in by_work.values() for i in a),'source_errors':errors},ensure_ascii=False))
if __name__=='__main__': main()

#!/usr/bin/env python3
"""Import bibliographic facts from already pinned TEI sources (never translation bodies).
Handles both TEI listBibl elements and 84000 div type=listBibl. Preserve mixed-content
citations because a title element can name a journal, not the cited article.
"""
from __future__ import annotations
import concurrent.futures, datetime, hashlib, json, pathlib, re, urllib.request, xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]
NS={'t':'http://www.tei-c.org/ns/1.0'}
XI='{http://www.w3.org/XML/1998/namespace}id'
def tx(n):return ' '.join(' '.join(n.itertext()).split())
def read_source(url):
    req=urllib.request.Request(url,headers={'User-Agent':'DharmaAtlas-BibliographyAudit/0.7'})
    with urllib.request.urlopen(req,timeout=35) as r:
        data=r.read(20000001)
        if len(data)>20000000:raise ValueError('Source too large')
    return data

def collect(url):
    try:
        raw=read_source(url);root=ET.fromstring(raw);parents={c:p for p in root.iter() for c in p};items=[]
        nodes=root.findall('.//t:listBibl//t:bibl',NS)+root.findall('.//t:listBibl//t:biblStruct',NS)+root.findall('.//t:div[@type="listBibl"]//t:bibl',NS)+root.findall('.//t:div[@type="listBibl"]//t:biblStruct',NS)
        seen=set();previous_author=''
        for b in nodes:
            citation=tx(b)
            if not citation or citation in seen:continue
            seen.add(citation)
            heads=[];p=parents.get(b)
            while p is not None:
                h=p.find('t:head',NS)
                if h is not None:heads.append(tx(h))
                p=parents.get(p)
            quoted=re.search('[“"](.+?)[”"]',citation)
            tagged=[' '.join(tx(x).split()) for x in b.findall('.//t:title',NS)]
            title=quoted.group(1).rstrip('.') if quoted else tagged[0] if tagged else citation[:150]
            author_nodes=b.findall('.//t:author',NS)
            author='; '.join(tx(n) for n in author_nodes)
            leading=citation.split('“')[0].strip().rstrip('.') if '“' in citation else ''
            if not author and leading and len(leading)<120:author=leading
            if author.startswith('_'):author=previous_author
            if author and not author.startswith('_'):previous_author=author
            years=re.findall(r'(?<!\d)(?:1[5-9]\d{2}|20[0-2]\d)(?!\d)',citation)
            links=list(dict.fromkeys(x.get('target') for x in b.findall('.//t:ref',NS) if x.get('target')))
            source_type='canonical_edition' if any(re.search('canonical|tibetan texts|sanskrit texts|primary',h,re.I) for h in heads) else 'bibliographic_citation'
            items.append({'local_id':b.get(XI),'title':title,'titles':tagged,'author':author or None,'year':int(years[-1]) if len(set(years))==1 else None,'candidate_years':list(dict.fromkeys(years)),'citation_raw':citation,'section_path':list(reversed(heads)),'source_type':source_type,'links':links,'source_url':url,'source_locator':('#'+b.get(XI)) if b.get(XI) else 'listBibl','reading_status':'authority_bibliography_metadata_checked; cited_fulltext_not_reviewed','parsing_note':'Title/author/year are conservative machine extraction; citation_raw and locator remain authoritative. Underscore author repetition is expanded only from the preceding identified author.'})
        return {'items':items,'sha256':hashlib.sha256(raw).hexdigest(),'status':'metadata_imported'}
    except Exception as e:return {'items':[],'status':'bibliography_import_failed','error':str(e)}

def main():
    path=ROOT/'data/authority_metadata_v0.7.json';data=json.loads(path.read_text())
    urls=sorted({i['source_url'] for r in data['records'] for i in r['imports'] if i.get('provider')=='84000' and i.get('status')=='metadata_imported' and not i.get('is_repository_placeholder')})
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=dict(zip(urls,pool.map(collect,urls)))
    for record in data['records']:
        for imp in record['imports']:
            result=results.get(imp['source_url'])
            if result:
                imp['bibliography']=result['items'];imp['bibliography_import_status']=result['status']
                if 'error' in result:imp['bibliography_error']=result['error']
                if result.get('sha256')!=imp.get('content_sha256'):imp['integrity_warning']='Source bytes changed or earlier hash differed; verify pinned source.'
    data['bibliography_parser_version']='0.7.1';data['bibliography_repaired_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    data['bibliography_count_note']='Raw counts include editions, repeat citations across works and duplicate source files; builder deduplicates per work using full citation, not journal title.'
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2))
    print(json.dumps({'unique_sources_checked':len(urls),'source_failures':sum(v['status']!='metadata_imported' for v in results.values()),'raw_bibliographic_records':sum(len(i.get('bibliography',[])) for r in data['records'] for i in r['imports']),'works_with_bibliography':sum(any(i.get('bibliography') for i in r['imports']) for r in data['records'])},ensure_ascii=False))
if __name__=='__main__':main()

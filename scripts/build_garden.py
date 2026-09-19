#!/usr/bin/env python3
"""Compile the public garden from the existing research build using an allowlist.
The public site is not a private database: everything deliberately displayed is
public. Do not publish raw research objects, source repository paths or QA reports.
Repository visibility is deliberately NOT changed by this script.
"""
from __future__ import annotations
import argparse,base64,copy,datetime,hashlib,json,pathlib,re,shutil,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
BLOCKED_HOSTS=('github.com','githubusercontent.com')
CATEGORIES={'early':{'zh':'早期佛典','en':'Early discourses'},'wisdom':{'zh':'般若经典','en':'Perfection of Wisdom'},'mahayana':{'zh':'大乘经论','en':'Mahāyāna'},'yogacara':{'zh':'瑜伽行派','en':'Yogācāra'},'madhyamaka':{'zh':'中观论书','en':'Madhyamaka'},'tibetan':{'zh':'藏传经典','en':'Tibetan traditions'},'chinese':{'zh':'汉传经典','en':'Chinese traditions'},'pali':{'zh':'巴利文献','en':'Pāli literature'}}
ROLE_ZH={'teacher':'导师','attributed speaker':'传统中的说法者','translator':'译者','author':'作者','commentator':'注释者','pilgrim':'行旅者','traveller':'行旅者','scholar':'学者','editor':'编者','researcher':'研究者','monk':'僧人','patron':'赞助者','traditionally_attributed_translator':'传统归属的译者','traditional author':'传统归属的作者'}

def clean(value):
    value=str(value or '')
    value=re.sub(r'https?://[^\s<>]*github[^\s<>]*','',value,flags=re.I)
    value=re.sub(r'\[(?:H|O|A|T|K)\d(?:,[A-Z]\d)*\]','',value)
    value=re.sub(r'(?i)(?:data|docs|skills|scripts|build)/[^\s；。]+','',value)
    return value.strip()
def public_url(url):
    if not isinstance(url,str):return ''
    try:
        p=urllib.parse.urlsplit(url)
        if p.scheme not in ('http','https') or not p.hostname:return ''
        if any(p.hostname.endswith(h) for h in BLOCKED_HOSTS):
            if '84000' in p.path:
                m=re.search(r'_toh([0-9]+(?:-[0-9]+)?)',urllib.parse.unquote(p.path))
                return 'https://84000.co/translation/toh'+m[1] if m else ''
            return ''
        if 'minyajing-rgb' in url.lower():return ''
        return url
    except ValueError:return ''
def wid(x):return 'w'+str(x).split('-')[-1] if x else None
def oid(x):return 'o'+str(x).split('-')[-1] if x else None
def categories(w):
    ts=w.get('traditions',[]);out=[]
    for needle,key in [('Early Buddhist','early'),('Prajñāpāramitā','wisdom'),('Mahāyāna','mahayana'),('Yogācāra','yogacara'),('Madhyamaka','madhyamaka'),('Tibetan','tibetan'),('Chinese','chinese'),('Pāli','pali')]:
        if any(needle in t for t in ts):out.append(key)
    return out or ['mahayana']
def write(path,content):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(content if isinstance(content,str) else json.dumps(content,ensure_ascii=False,indent=2))

def stage_public():
    dst=ROOT/'build/public';src=ROOT/'docs/garden'
    if dst.exists():shutil.rmtree(dst)
    shutil.copytree(src,dst)
    # Other live products keep their own paths. Internal Dharma review/archive/data
    # directories are intentionally NOT copied, so direct legacy URLs return 404.
    q=ROOT/'docs/quantum'
    if q.exists():shutil.copytree(q,dst/'quantum')
    if (ROOT/'docs/CNAME').exists():shutil.copyfile(ROOT/'docs/CNAME',dst/'CNAME')
    (dst/'.nojekyll').touch()
    write('build/public/404.html','<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Dharma Atlas</title><body style="background:#fffaf1;color:#353044;font-family:serif;text-align:center;padding:15vh 24px"><h1>这条小径，暂未开放。</h1><p>This path is not available.</p><a href="./">返回花园 · Return to the garden</a></body></html>')
    return dst

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',default='docs/index.html');ap.add_argument('--stage-only',action='store_true');args=ap.parse_args()
    if args.stage_only:stage_public();return
    source=ROOT/args.source;html=source.read_text()
    m=re.search(r'<script id="atlas-data" type="application/json">(.*?)</script>',html,re.S)
    if not m:raise ValueError('Expected fresh research build, not an already-projected garden page.')
    d=json.loads(m[1]);en=json.loads((ROOT/'web/garden/editorial.en.json').read_text())
    assert len(d['works'])==100 and len(d['stories'])==len(en['stories'])==12
    out=ROOT/'docs/garden';out.mkdir(parents=True,exist_ok=True)
    public={'categories':CATEGORIES,'works':[],'stories':[],'people':[],'objects':[],'libraries':[],'places':[],'events':[],'sources':[],'methods':[],'questions':[],'media':[],'figures':[],'storySources':[]}
    for w in d['works']:
        routes=[{'url':public_url(r['url']),'label':{'cbeta':'CBETA','84000':'84000','suttacentral':'SuttaCentral','sat':'SAT'}.get(r.get('source_id'),clean(r.get('source_id') or 'Text source')),'discovery':r.get('route_level')=='discovery'} for r in w.get('authority_routes',[]) if public_url(r.get('url'))]
        themes=[clean(t) for t in w.get('themes',[])];title=w['titles'].get('en') or w['titles']['zh']
        books=[]
        for b in w.get('research_bibliography',[]):
            url=public_url(b.get('url') or b.get('source_url'))
            books.append({'title':clean(b.get('title') or ' / '.join(b.get('titles',[]))),'citation':clean(b.get('citation_raw') or ' · '.join(str(x) for x in [b.get('author'),b.get('year')] if x)),'url':url})
        chron=[]
        for c in w.get('reviewed_chronology',[]):
            start=c.get('start');end=c.get('end',start)
            chron.append({'label_zh':clean(c.get('display')),'label_en':str(start)+(('–'+str(end)) if start!=end else '')+' CE','note_zh':clean(c.get('caution_zh')),'note_en':'A date for the surviving copy or printing, not the original composition of the work.','url':public_url(c.get('source'))})
        parallel={k:[clean(x) if isinstance(x,str) else clean(json.dumps(x,ensure_ascii=False)) for x in v] for k,v in w.get('typed_relations',{}).get('suttacentral_work_level',{}).items() if isinstance(v,list)}
        relations=[{'id':p['person_id'],'role_zh':ROLE_ZH.get(p.get('relation'),p.get('relation','')),'role_en':p.get('relation','').replace('_',' ')} for p in w.get('related_people',[])]
        public['works'].append({'id':wid(w['work_id']),'zh':w['titles']['zh'],'en':title,'aliases':' / '.join(dict.fromkeys(t for t in w['titles'].values() if t)),'themes':themes,'categories':categories(w),'intro_zh':clean(w.get('evidence',{}).get('why_it_matters')),'intro_en':'Explore '+', '.join(themes[:3])+'. Follow the text, its editions and the questions behind its transmission.' if themes else 'Begin with the text, then explore its editions and transmission.','caution_zh':'同名、译文相近或主题相关，不等于同一部作品。版本、写本与形成史仍需分别核对。','caution_en':clean(w.get('evidence',{}).get('relation_warning')) or 'A similar title or theme does not establish textual identity. Editions, surviving copies and composition history require separate study.','routes':routes,'ids':[{'label':{'taisho':'大正藏 / Taishō','suttacentral':'SuttaCentral','toh':'Toh'}.get(k,k),'value':str(v)} for k,v in w.get('canonical_ids',{}).items() if v],'versions':[{'system':clean(v.get('system')),'label':clean(v.get('id'))} for v in w.get('versions',[])],'parallel':parallel,'chronology':chron,'objects':[oid(v['witness_id']) for v in w.get('reviewed_item_evidence',[])],'people':relations,'books':books})
    for i,s in enumerate(d['stories']):
        body=s['body']
        body=re.sub(r'\*\*交互设计\*\*：.*?(?=\n|$)','',body)
        body=body.replace('数据库最底层会一直保留四件事：','理解一卷经，可以沿着四个层次继续探索：').replace('**Work → Version → Witness → Source**。','**作品 → 版本 → 实物 → 来源**。')
        body=re.sub(r'Dharma Atlas会把译者做成一个Network node：[^\n]+','沿着译者的经历，可以继续查找他参与的作品、不同译本、相关材料与现代研究。',body)
        body=body.replace('所以你最初提出的“唐三藏取回来又被翻坏了吗？”可以转成一个更有证据的问题：','关于译经差异，我们可以提出一个更有依据的问题：')
        body=body.replace('**Timeline**','**时间线**').replace('**Map**','**地图**').replace('**Evidence**','**资料来源**').replace('**Data nodes**','**相关人物与文本**').replace('**Research path**','**进一步阅读**').replace('**Crosswalk**','**版本对照**').replace('**Evidence path**','**查阅路径**').replace('**Season 1 Final Map**','**这一季的旅程**')
        public['stories'].append({'title_zh':clean(s['title']),'title_en':en['stories'][i]['title'],'teaser_zh':clean(s['teaser']),'teaser_en':en['stories'][i]['teaser'],'body_zh':clean(body),'body_en':en['stories'][i]['body']})
    for p in d['people']:
        roles=p.get('role',[]);period=p.get('period','')
        public['people'].append({'id':p['id'],'name_zh':p['name_zh'],'name_en':p['name_en'],'roles_zh':' / '.join(ROLE_ZH.get(x,x) for x in roles),'roles_en':' / '.join(roles),'intro_zh':clean(p.get('learn_hook')),'intro_en':'Explore the texts and traditions connected with '+p['name_en']+'.','period':clean(period),'regions':' / '.join(p.get('regions',[]))})
    for v in d['witnesses']:
        date=clean(v.get('date_range'))
        if re.search(r'[\u3400-\u9fff]',date):date='1015 CE; later post-colophon: 1139 CE' if v['id']=='WIT-0010' else date
        urls=list(dict.fromkeys(public_url(u) for u in [v.get('access_url')]+v.get('source_urls',[]) if public_url(u)))
        public['objects'].append({'id':oid(v['id']),'title_zh':v['title_zh'],'title_en':v.get('title_en') or v['title_zh'],'intro_zh':clean(v.get('significance_zh')),'intro_en':'Follow the surviving material and its institutional record. Distinguish the date of a copy from the composition of a work.','date':date,'material':clean(v.get('material')),'language':' / '.join(str(x) for x in [v.get('language'),v.get('script')] if x),'holding':clean(v.get('holding_institution')),'shelfmark':clean(v.get('shelfmark_or_id')),'origin':clean(v.get('origin_or_findspot')),'urls':urls})
    for l in d['libraries']:
        public['libraries'].append({'id':l['id'],'name':l['name'],'city':l['city'],'country':l['country'],'coords':l.get('coordinates'),'strengths':l.get('strengths',[]),'urls':[public_url(u) for u in l.get('source_urls',[]) if public_url(u)]})
    for p in d['places']:
        v=p['properties'];public['places'].append({'id':v['id'],'name_zh':v['name_zh'],'name_en':v['name_en'],'coords':p['geometry']['coordinates'],'note':clean(v.get('note'))})
    for i,e in enumerate(d['events']):
        t=en['events'][i];public['events'].append({'id':'event-'+str(i+1),'start':e['start'],'end':e.get('end',e['start']),'title_zh':e['title_zh'],'title_en':t[0],'date_zh':e['date_label'],'date_en':t[1],'note_zh':e['note_zh'],'note_en':t[2],'caution_zh':e.get('place_caution_zh') or '实物的纪年、现代收藏事件与作品成书年代，需分开理解。','caution_en':t[3],'place':e.get('place_id'),'work':wid(e.get('work_id')),'object':oid(e.get('witness_id')),'url':public_url(e.get('source'))})
    for s in d['sources']:
        u=public_url(s.get('url'))
        if not u:continue
        intro=s.get('strengths_zh','');intro='；'.join(intro) if isinstance(intro,list) else intro
        public['sources'].append({'name_zh':s.get('name') or s.get('name_en'),'name_en':s.get('name_en') or s.get('name'),'intro_zh':clean(intro),'intro_en':'Languages: '+', '.join(s.get('languages',[]))+'. Explore the provider’s collections, catalogues and access conditions.','url':u})
    for i,m in enumerate(d['methods']):
        t=en['methods'][i];public['methods'].append({'name_zh':clean(m['name']),'name_en':t[0],'question_zh':clean(m['question']),'question_en':t[1],'steps_zh':clean(m['steps']),'steps_en':t[2]})
    for i,q in enumerate(d['dossiers']):
        t=en['questions'][i];public['questions'].append({'title_zh':q['topic_zh'],'title_en':t[0],'intro_zh':clean(q.get('traditional_frame')),'intro_en':t[1]})
    titles_en=['Conserving the Diamond Sūtra','Explore the Gandhara Scroll']
    for i,m in enumerate(d['publicMedia']):
        public['media'].append({'title_zh':m['title_zh'],'title_en':titles_en[i] if i<len(titles_en) else m['provider'],'provider':m['provider'],'url':public_url(m['url'])})
    fig_en=['Dates in Buddhist textual history','Textual journeys and geography','Works, editions and relationships','From a work to a surviving object','Paths for learning','Comparing languages and editions']
    assets=out/'assets';assets.mkdir(exist_ok=True)
    for i,f in enumerate(d.get('figures',[])):
        name=f['id']+'.png';raw=f.get('data','')
        if raw.startswith('data:image/png;base64,'):(assets/name).write_bytes(base64.b64decode(raw.split(',',1)[1],validate=True))
        else:
            original=ROOT/'docs/review/assets'/name
            if not original.exists():raise FileNotFoundError(name)
            shutil.copyfile(original,assets/name)
        public['figures'].append({'id':f['id'],'title_zh':f['title'],'title_en':fig_en[i],'src':'./assets/'+name})
    for s in d.get('storySources',[]):
        u=public_url(s.get('url'))
        if u:public['storySources'].append({'url':u,'label':clean(s.get('title'))})
    # Stop the release if an internal source identifier survived projection.
    payload=json.dumps(public,ensure_ascii=False,separators=(',',':'))
    for forbidden in ['minyajing-rgb','github.com','githubusercontent.com','canonical_datasets','reported_level_legacy','source_commit','content_sha256','review_flags','data/CURRENT','work-dossiers','release-manifest','DA-W-','WIT-']:
        if forbidden.lower() in payload.lower():raise ValueError('Internal value leaked into public projection: '+forbidden)
    template=(ROOT/'web/garden/index.html').read_text()
    page=template.replace('__PUBLIC_CONTENT__',payload.replace('<','\\u003c'))
    (out/'index.html').write_text(page)
    for name in ['garden.css','garden.js']:shutil.copyfile(ROOT/'web/garden'/name,out/name)
    from render_garden import main as render
    render()
    # Archive the visitor page at the familiar entry point; deployment uses only stage.
    shutil.copyfile(out/'index.html',ROOT/'docs/index.html')
    dst=stage_public()
    public_files=sorted(str(p.relative_to(dst)) for p in dst.rglob('*') if p.is_file())
    report={'built_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ui_release':'garden-1.0','counts':{k:len(v) for k,v in public.items() if isinstance(v,list)},'public_projection':'allowlist_only','internal_paths_in_site':False,'raw_research_dataset_embedded':False,'published_payload_note':'All visitor-visible text and bibliography are public. This does not make the existing source repository private.','source_repository_visibility_changed':False,'custom_domain_or_dns_changed':False,'preserved_subsites':['quantum'] if (dst/'quantum').exists() else [],'homepage_sha256':hashlib.sha256(page.encode()).hexdigest(),'garden_html_bytes':len(page.encode()),'public_files':public_files}
    write('build/garden-release.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='public_files'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()

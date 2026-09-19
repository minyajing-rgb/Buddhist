#!/usr/bin/env python3
"""Build the complete functional RESEARCH PREVIEW, not a scholar-certified release.
Pure stdlib, deterministic input handling, no network. Existing canonical files are
never overwritten. Optional PNG figures are used only when already present.
"""
from __future__ import annotations
import copy,csv,datetime,hashlib,io,json,os,pathlib,re,subprocess,unicodedata
ROOT=pathlib.Path(__file__).resolve().parents[1]
INPUTS={}

def read(path):
    path=pathlib.Path(path)
    if path.is_absolute() or '..' in path.parts:raise ValueError('Input must remain in repository')
    raw=(ROOT/path).read_bytes();INPUTS[str(path)]=hashlib.sha256(raw).hexdigest()
    return raw.decode('utf-8')
def js(path):return json.loads(read(path))
def save(path,obj):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def arr(obj,key):
    value=obj.get(key,[]) if isinstance(obj,dict) else obj
    if not isinstance(value,list):raise TypeError(f'Expected list: {key}')
    return value
def normalized(s):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',str(s))).strip().casefold()
def source_ref():
    if os.environ.get('GITHUB_SHA'):return os.environ['GITHUB_SHA']
    try:return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()
    except (OSError,subprocess.CalledProcessError):return 'local-working-copy; see release-manifest input hashes'

def main():
    current=js('data/CURRENT.json');manifest=current['canonical_datasets']
    canon=lambda name,key:arr(js(manifest[name]),key)
    original=canon('deep_crosswalk','records')
    works=copy.deepcopy(original)
    assert len(works)==100 and len({w['work_id'] for w in works})==100,'100 unique work IDs required'
    authority=js('data/authority_metadata_v0.7.json')
    add=js('data/review_addendum_v0.7.json')
    imports={r['work_id']:r.get('imports',[]) for r in authority['records']}
    review={r['work_id']:r for r in add['work_evidence']}
    sources=canon('sources','sources');libraries=canon('physical_holdings','libraries')
    people=canon('people','people');places=canon('geography','features')
    witnesses=copy.deepcopy(canon('witnesses','witnesses'))
    witmap={v['id']:v for v in witnesses}
    people_edges=js('data/person_work_edges_v0.3.json')['edges']
    place_edges=js('data/place_work_edges_v0.3.json')['edges']
    for c in add['corrections']:
        if c['entity_id'] in witmap:
            v=witmap[c['entity_id']];v[c['field']]=c['value'];v.setdefault('applied_corrections',[]).append(c)
    for v in witnesses:
        v['reviewed_item']=v['id'] in ['WIT-0001','WIT-0003','WIT-0010']
        if v.get('applied_corrections'):
            v['review_note']='本轮已按列明来源校正馆藏号/纪年/访问字段；其余历史解释不自动取得新的审核等级。'
            v['source_urls']=list(dict.fromkeys(v.get('source_urls',[])+[c['source'] for c in v['applied_corrections']]))
    for e in people_edges:
        if e['person_id']=='paramartha' and e['work_id']=='DA-W-0029':
            e['legacy_relation']=e['relation'];e['relation']='traditionally_attributed_translator'
    places+=add.get('extra_places',[])
    notes={}
    if (ROOT/'data/learning_notes_0033_0100_v0.7.tsv').exists():
        notes={r['work_id']:r for r in csv.DictReader(io.StringIO(read('data/learning_notes_0033_0100_v0.7.tsv')),delimiter='\t')}
    discovery_markers=['worldcat.org','library.bdrc.io','gret_csxbk.htm','gret_utfbk.htm','/canon/mind-only','/canon/epistemology-and-logic']
    type_conflicts=[];dangling=[]
    for w in works:
        wid=w['work_id'];w['reported_level_legacy']=w.get('crosswalk_level')
        w['assessed_level']='not_scholar_certified; dimension_review_required'
        w['imports']=imports.get(wid,[])
        w['related_people']=[e for e in people_edges if e['work_id']==wid]
        we=review.get(wid,{})
        w['reviewed_chronology']=we.get('chronology',[])
        w['reviewed_item_evidence']=we.get('item_witnesses',[])
        w['research_bibliography']=[];seen=set()
        candidates=[b for b in add['bibliography'] if wid in b.get('work_ids',[])]+[b for imp in w['imports'] for b in imp.get('bibliography',[])]
        for b in candidates:
            key=normalized(b.get('citation_raw') or '|'.join([b.get('title',''),str(b.get('year','')),b.get('author') or '']))
            if not key or key in seen:continue
            seen.add(key);w['research_bibliography'].append(b)
        for route in w.get('authority_routes',[]):
            route['route_level']='discovery' if any(s in route.get('url','') for s in discovery_markers) else 'work_candidate'
            route['access_caution']='Catalogue or source route; online availability is not a claim of completed philological verification.'
        w['review_flags']=['成书年代仍需逐部论证；实体纪年与现代出版日期均不能代替。','旧版L3标签保留供比较，但本轮不据此认证研究完成。']
        if not w['reviewed_item_evidence']:w['review_flags'].append('本轮未核实具体作品—实体见证关系；馆藏背景不是持有证明。')
        if not w['research_bibliography']:w['review_flags'].append('没有已定位的条目级书目，仍需补专著、论文与署名立场。')
        else:w['review_flags'].append('已取得书目记录；多数为目录元数据，未读全文，不代表已完成文献综述。')
        if any(i.get('is_repository_placeholder') for i in w['imports']):w['review_flags'].append('至少一个来源快照是目录占位；不能据此声称已有可读译文。')
        if any(a['route_level']=='discovery' for a in w.get('authority_routes',[])):w['review_flags'].append('含平台/分类/检索入口，不能计为已经读到作品全文。')
        typed=w.get('typed_relations',{})
        if isinstance(typed.get('source'),dict):
            w['typed_relation_provenance']=copy.deepcopy(typed['source']);typed['source']=typed['source'].get('source_url')
        rel=typed.get('suttacentral_work_level',{})
        full=set(map(str,rel.get('full',[])));similar=set(map(str,rel.get('resembling',[])))
        if full & similar:
            conflict={'work_id':wid,'overlap':sorted(full & similar),'action':'retain raw classifications; require source-level resolution'}
            type_conflicts.append(conflict);w['parallel_classification_conflicts']=conflict
            w['review_flags'].append('完整/近似平行列表有重叠，分类待复核；原列表保留，不自动判定全文相同。')
        if wid in notes:
            w['evidence_legacy']=copy.deepcopy(w.get('evidence',{}));w.setdefault('evidence',{})
            w['learning_note']={**notes[wid],'status':'editorial_reading_prompt_based_on_existing_title_theme_metadata; not_new_historical_finding','source_routes':[r.get('url') for r in w.get('authority_routes',[])]}
            w['evidence']['why_it_matters']=notes[wid]['learning_question_zh']+' '+notes[wid]['reading_focus_zh']
        if wid=='DA-W-0079':w['review_flags'].append('中文复合标题“百譬喻/百事”仍需规范化，暂不与《百喻经》合并。')
        if wid=='DA-W-0100':w['review_flags'].append('这是传统/文集导航层，非已证实的单一古典作品；现代选译与仪轨版本必须分拆。')
        for key in ['versions','verified_additional_ids','physical_access','material_context','traditions']:
            if not isinstance(w.get(key),list):w[key]=[]
    ids={w['work_id'] for w in works}
    pids={p['id'] for p in people};gids={p['properties']['id'] for p in places}
    for edge in people_edges:
        if edge['person_id'] not in pids or edge['work_id'] not in ids:dangling.append(edge)
    for edge in place_edges:
        if edge['place_id'] not in gids or edge['work_id'] not in ids:dangling.append(edge)
    story_text=read(manifest['season1'])
    matches=list(re.finditer(r'^## EP(\d+)｜(.+)$',story_text,re.M));stories=[]
    end=story_text.find('# Season 1 Source Shelf');end=end if end>=0 else len(story_text)
    for i,m in enumerate(matches):
        body=story_text[m.end():matches[i+1].start() if i+1<len(matches) else end].strip().rstrip('-').strip()
        first=next((s.strip() for s in body.split('\n\n') if s.strip() and not s.strip().startswith(('#','---'))),'')
        teaser=re.sub(r'[*`#]','',first).replace('\n',' ')
        stories.append({'id':'EP'+m.group(1),'title':m.group(2),'body':body,'teaser':teaser[:90]+('…' if len(teaser)>90 else '')})
    assert len(stories)==12,'Expected 12 complete story sections'
    story_sources=[{'title':a.strip(),'url':b.strip()} for a,b in re.findall(r'^- (.+?) — (https?://\S+)',story_text[end:],re.M)]
    method_doc=read('skills/global-knowledge-atlas/references/EXECUTION_PLAYBOOK_v1.1.md')
    methods=[]
    for line in method_doc.splitlines():
        if not re.match(r'^\|M\d{2}',line):continue
        cells=[x.strip() for x in line.strip('|').split('|')]
        if len(cells)!=5:raise ValueError('Unexpected method row: '+line)
        m=re.match(r'(M\d+)\s+(.+)',cells[0])
        methods.append(dict(zip(['id','name','question','steps','output','gate'],[m[1],m[2],*cells[1:]])))
    assert len(methods)==33
    all_bibl=[b for w in works for b in w['research_bibliography']]
    unique_bibl={normalized(b.get('citation_raw') or '|'.join([b.get('title',''),str(b.get('year',''))])) for b in all_bibl}
    counts={'works':len(works),'sources':len(sources),'libraries':len(libraries),'places':len(places),'people':len(people),'witness_records':len(witnesses),'stories':len(stories),'methods':len(methods),'imported_works':sum(any(i.get('status')=='metadata_imported' for i in w['imports']) for w in works),'import_records':sum(len(w['imports']) for w in works),'placeholder_records':sum(bool(i.get('is_repository_placeholder')) for w in works for i in w['imports']),'works_with_bibliography':sum(bool(w['research_bibliography']) for w in works),'bibliography_records':len(all_bibl),'unique_bibliographic_citations_across_works':len(unique_bibl),'reviewed_item_works':sum(bool(w['reviewed_item_evidence']) for w in works),'dated_events':len(add['events']),'parallel_classification_conflict_works':len(type_conflicts),'new_work_specific_learning_prompts':len(notes),'scholar_certified_L4_works':0}
    generated=datetime.datetime.now(datetime.timezone.utc).isoformat();commit=source_ref()
    audit={'version':'0.7','generated_at':generated,'counts':counts,'legacy_claim':'100 L3','review_result':'Legacy L3 claims not certified by actual chronology/bibliography/item fields.','parallel_conflicts':type_conflicts,'dangling_edges':dangling,'records':[{'work_id':w['work_id'],'title':w['titles']['zh'],'reported_level_legacy':w['reported_level_legacy'],'assessed_level':w['assessed_level'],'review_flags':w['review_flags'],'bibliography_records':len(w['research_bibliography']),'reviewed_items':len(w['reviewed_item_evidence'])} for w in works],'release_gate':'RESEARCH_PREVIEW_ONLY','limits':['100 records are representative entries, not the entirety of Buddhist literature.','Imported metadata and bibliography are not full scholarly review.','Collection-level contexts are not specific item holdings.','No official public deployment is certified by this build.','The base 100 records were present before this review; they are not 100 newly researched works.']}
    payload={'meta':{'version':'0.7 research preview','generated_at':generated,'source_commit':commit,'counts':counts,'source_snapshots':authority.get('source_snapshots',{})},'works':works,'people':people,'peopleEdges':people_edges,'places':places,'placeEdges':place_edges,'witnesses':witnesses,'libraries':libraries,'sources':sources,'concepts':canon('concepts','concepts'),'paths':canon('learning_paths','paths'),'dossiers':canon('research_questions','dossiers'),'stories':stories,'storySources':story_sources,'methods':methods,'methodDoc':method_doc,'curatedBibliography':add['bibliography'],'publicMedia':add['public_media_links'],'events':add['events'],'figures':[],'audit':audit}
    template=read('site/index.template.html')
    # Small source-controlled compatibility/accuracy fixes; no external code or CDN.
    template=template.replace("${esc(title)}</b><div class=\"small muted\">", "${esc(title)}</b>${b.citation_raw?'<p class=\"small\">'+esc(b.citation_raw)+'</p>':''}<div class=\"small muted\">")
    template=template.replace('基线审计发现：100部没有完整逐部年代论证、100部没有条目级书目，95部未记录写本链接。','基线审计发现：100部没有完整逐部年代论证、100部没有条目级书目，95部未记录写本链接。导入后数量以本页实时统计为准。')
    template=template.replace('</style>','.large-font .prose{font-size:20px}.large-font .card p,.large-font .detailrow{font-size:18px}</style>')
    if template.count('__ATLAS_DATA__')!=1:raise ValueError('Exactly one payload placeholder required')
    html=template.replace('__ATLAS_DATA__',json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c'))
    save('build/site/index.html',html);save('build/Dharma-Atlas-v0.7.html',html)
    save('docs/review/index.html',html)
    save('data/deep_crosswalk_100_v0.7.review.json',{'version':'0.7','source_commit':commit,'generated_at':generated,'scope':'100 representative entries; review overlay, not 100 certified deep scholarly crosswalks','records':works})
    save('data/research_audit_v0.7.json',audit);save('build/research-audit-v0.7.json',audit)
    for w in works:
        lines=[f"# {w['titles']['zh']}｜{w['work_id']}",'','状态：研究审阅记录；旧版L3标签不自动获得认证。','',w.get('evidence',{}).get('why_it_matters',''),'','## 版本与入口','']
        lines += [f"- {a.get('source_id','source')} [{a['route_level']}]：{a.get('url','')}" for a in w.get('authority_routes',[])]
        lines+=['','## 编号与跨版本关系','',json.dumps(w.get('canonical_ids',{}),ensure_ascii=False),'',w.get('evidence',{}).get('relation_warning',''),'','## 本轮核对年代（不是成书年代）','']
        lines += [f"- {c['display']}：{c['caution_zh']} 来源：{c['source']}" for c in w['reviewed_chronology']] or ['尚无逐部核对结果。']
        lines+=['','## 已取得书目','']
        lines += [f"- {b.get('citation_raw') or b.get('title') or ' / '.join(b.get('titles',[]))}；来源：{b.get('url') or b.get('source_url')}；阅读状态：{b.get('reading_status','目录导入，未读全文')}" for b in w['research_bibliography']] or ['待补；平台主页不计作论文。']
        lines+=['','## 待核项目','']+[f'- {flag}' for flag in w['review_flags']]
        lines+=['','## 完整结构化记录','','```json',json.dumps(w,ensure_ascii=False,indent=2),'```','']
        save(f"docs/review/work-dossiers/{w['work_id']}.md",'\n'.join(lines))
    release={'version':'0.7','source_commit':commit,'generated_at':generated,'status':'functional_research_preview','public_deployment':'not_performed','source_inputs_sha256':INPUTS,'counts':counts,'html_sha256':hashlib.sha256(html.encode()).hexdigest(),'browser_tests':'separate verification required; compilation does not certify UI or historical accuracy'}
    save('build/release-manifest.json',release)
    print(json.dumps({'counts':counts,'html_bytes':len(html.encode()),'output':'build/Dharma-Atlas-v0.7.html','gate':'RESEARCH_PREVIEW_ONLY'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()

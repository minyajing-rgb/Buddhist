#!/usr/bin/env python3
"""Promote the working atlas to the public homepage without erasing other sites.
User authorization, 2026-09-19: publish existing content now; improve research and
website in parallel. Unknown evidence remains labelled, not a publication blocker.
"""
from __future__ import annotations
import datetime, hashlib, json, os, pathlib, re, shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
URL='https://minyajing-rgb.github.io/Buddhist/'

PUBLIC_JS=r'''
<script id="public-beta-ui">
// A public preview is not a claim of completed scholarly review.
const publicBetaTitle='Dharma Atlas · 公开研究预览';
const oldQuality=qualityHtml;
qualityHtml=function(){return oldQuality().replace('此构建不自动部署，不宣称正式官网已经上线。','公开研究预览；最新发布结果、时间和版本见发布记录。')};
const originalOpenWork=openWork;
openWork=function(id){originalOpenWork(id);const w=W.get(id);if(w&&w.parallel_review){
 const note=document.createElement('div');note.className='callout';
 note.textContent='平行关系更新：'+w.parallel_review.summary_zh;
 $('modalBody').insertBefore(note,$('modalBody').querySelector('h3'));
}};
const publicFooter=document.createElement('div');publicFooter.className='endnote';
publicFooter.innerHTML='公开预览 · 内容与网站同步迭代。<a href="release.json" target="_blank" rel="noopener">发布版本</a> · <a href="updates.html">更新记录</a> · <a href="quantum/">量子知识地图 ↗</a>';
$('home').appendChild(publicFooter);
const navStatus=document.querySelector('.notice');
navStatus.innerHTML='公开研究预览 · 已有内容现在可用，研究继续完善 · <button data-action="status">查看数据覆盖与待核事项</button>';
</script>
'''

def main():
    source=ROOT/'docs/review/index.html'
    html=source.read_text(encoding='utf-8')
    found=re.search(r'(<script id="atlas-data" type="application/json">)(.*?)(</script>)',html,re.S)
    if not found:raise ValueError('No embedded atlas data')
    data=json.loads(found[2])
    assert len(data['works'])==len({x['work_id'] for x in data['works']})==100
    assert len(data['stories'])==12
    overlay_path=ROOT/'data/parallel_review_v0.8.json'
    applied=0
    if overlay_path.exists():
        overlay=json.loads(overlay_path.read_text());patches={r['work_id']:r for r in overlay.get('records',[])}
        for w in data['works']:
            patch=patches.get(w['work_id'])
            if not patch or patch.get('status')!='source_encoding_checked':continue
            w['typed_relations_legacy_before_v08']=w['typed_relations']
            w['typed_relations']={'suttacentral_work_level':patch['relations'],'source':patch['source_url'],'note':patch['limits_zh']}
            w['parallel_review']=patch
            w['review_flags']=[x for x in w['review_flags'] if '完整/近似平行列表有重叠' not in x]
            w['review_flags'].append('本轮核对官方关系编码，不等于已逐段比较全部平行经文。')
            w.pop('parallel_classification_conflicts',None)
            applied+=1
        data['meta']['counts']['parallel_source_encoding_reviewed_works']=applied
        data['meta']['counts']['parallel_classification_conflict_works']=sum(bool(w.get('parallel_classification_conflicts')) for w in data['works'])
    version='0.8-public-beta' if applied else '0.7.1-public-beta'
    data['meta'].update({'version':version,'publication_mode':'living_public_beta','parallel_review_applied':applied})
    data['audit']['release_gate']='PUBLIC_BETA_ALLOWED_WITH_VISIBLE_RESEARCH_GAPS'
    data['audit']['limits']=[x for x in data['audit']['limits'] if 'deployment' not in x.lower()]
    data['audit']['counts']=data['meta']['counts']
    data['audit']['parallel_conflicts']=[x for x in data['audit'].get('parallel_conflicts',[]) if x['work_id'] not in {w['work_id'] for w in data['works'] if w.get('parallel_review')}]
    embedded=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    html=html[:found.start(2)]+embedded+html[found.end(2):]
    html=html.replace('研究预览 v0.7 ·','公开研究预览 ·')
    html=html.replace('GitHub文件页显示源码，不等于公网官网。','当前为公开研究预览，内容持续更新。')
    html=html.replace('95部未记录写本链接。','95部未记录写本链接。上述为旧基线缺口，不是本轮更新后的全部状态。')
    html=html.replace('按标准化题名去重','按完整书目引用去重')
    html=html.replace("'此构建不自动部署，不宣称正式官网已经上线。'","'公开研究预览；部署版本与时间见发布记录。'")
    html=html.replace('[/\u0000]','')
    # Relative release links work from either the homepage or /review/.
    html=html.replace('</body>',PUBLIC_JS+'\n</body>')
    archive=ROOT/'docs/archive/pre-public-beta/index.html'
    if not archive.exists() and (ROOT/'docs/index.html').exists():
        archive.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/'docs/index.html',archive)
    (ROOT/'docs/index.html').write_text(html,encoding='utf-8')
    source.write_text(html.replace('href="release.json"','href="../release.json"').replace('href="updates.html"','href="../updates.html"').replace('href="quantum/"','href="../quantum/"'),encoding='utf-8')
    (ROOT/'docs/.nojekyll').touch()
    release={'version':version,'source_commit':os.environ.get('GITHUB_SHA','local-build'),'built_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'public_url':URL,'intended_status':'public_research_beta','deployment_status':'candidate; consult public_deployment.json for verified result','counts':data['meta']['counts'],'homepage_sha256':hashlib.sha256(html.encode()).hexdigest(),'research_complete':False,'data_policy':'Research gaps remain visible. They do not block functional preview releases.','preserved_subsites':['quantum/'],'language_status':'This release publishes the existing Chinese research interface; complete English localization remains a separate tracked task.'}
    (ROOT/'docs/release.json').write_text(json.dumps(release,ensure_ascii=False,indent=2))
    (ROOT/'data/public_beta_manifest.json').write_text(json.dumps(release,ensure_ascii=False,indent=2))
    # Update only the publication policy, not counts or canonical research pointers.
    current_path=ROOT/'data/CURRENT.json';current=json.loads(current_path.read_text())
    current['phase']='LIVE_PREVIEW_AND_RESEARCH_IN_PARALLEL'
    current['public_site_rebuild']='PUBLIC_BETA_ALLOWED_WITH_VISIBLE_RESEARCH_GAPS'
    current['publication_policy']={'authorized_at':'2026-09-19','mode':'publish_existing_now_iterate_content_and_ui','public_url':URL,'scholarly_completeness_blocks_preview':False,'functional_and_safety_checks_required':True}
    current['rules']=[r for r in current.get('rules',[]) if not any(x in r.lower() for x in ['website remains frozen','official scholarly publication remains gated','no public website deployment is implied'])]
    current['rules'].append('Publish usable beta increments with honest evidence labels; do not delay all preview releases until scholarship is complete.')
    current.setdefault('site',{}).update({'root':'docs/index.html','preview':'docs/review/index.html','public_url':URL,'deployment_status':'see docs/public_deployment.json','preserved_subsites':['docs/quantum/']})
    current_path.write_text(json.dumps(current,ensure_ascii=False,indent=2))
    print(json.dumps(release,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

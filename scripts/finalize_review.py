#!/usr/bin/env python3
"""Finalize the research preview: render existing project diagrams, improve offline UX.
No historical reconstruction is asserted. PNGs are exports of existing project SVGs,
not images of ancient objects. CairoSVG is used only for format conversion.
"""
from __future__ import annotations
import base64,hashlib,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
TITLES={'01_timeline':'佛典时间线：不同日期意味着什么','02_geography':'文本传播与地理关系示意','03_textual_tree':'作品、版本与文本关系','04_evidence_chain':'从作品走到实物的证据链','05_learning_map':'小白逐层学习地图','06_crosswalk':'多语言与版本 Crosswalk 示意'}
RUNTIME=r'''
<script>
// A successful in-session action is not a successful persistent save.
let previewStorageAvailable=true;
try{const k='dharma-atlas-storage-check';localStorage.setItem(k,'1');localStorage.removeItem(k)}catch(e){previewStorageAvailable=false}
const baseToast=toast;
toast=function(message){
  if(!previewStorageAvailable && /已保存|已加入收藏|已取消收藏/.test(message)){
    message=message.replace('已保存','已更新')+'；仅本次有效，本地存储不可用，可导出记录。';
  }
  baseToast(message);
};
const baseRenderStories=renderStories;
renderStories=function(){baseRenderStories();if(!previewStorageAvailable){$('storyProgress').textContent=`已读完 ${completed.size} / ${D.stories.length} 集 · 当前浏览器不允许本地保存，可导出阅读记录。`;}}
if(storage.largeFont)document.body.classList.add('large-font');
function figureCard(f){return `<figure class="figure card"><button data-figure="${esc(f.id)}" style="padding:0;border:0;background:none;width:100%;cursor:zoom-in" aria-label="放大${esc(f.title)}"><img src="${f.data}" alt="${esc(f.title)}" loading="lazy"></button><figcaption>${esc(f.title)} · 点击放大 · 项目教学图解，非历史原件。</figcaption></figure>`}
const baseRenderLibrary=renderLibrary;
renderLibrary=function(){baseRenderLibrary();if(libMode==='media'){$('libraryGrid').insertAdjacentHTML('beforeend','<div class="sectionhead" style="grid-column:1/-1"><div><div class="eyebrow">SIX VISUAL GUIDES</div><h2>从一张图，把关系看明白</h2><p>既有项目图解的PNG版本；示意路线不作为新发现或精确年代证据。</p></div></div>'+D.figures.map(figureCard).join(''));}}
document.addEventListener('click',e=>{const button=e.target.closest('[data-figure]');if(!button)return;const f=D.figures.find(x=>x.id===button.dataset.figure);if(f)openModal(f.title,`<figure class="figure"><img src="${f.data}" alt="${esc(f.title)}"><figcaption>教学示意；须与具体记录的来源、年代和争议一起使用，不能代替学术证据。</figcaption></figure>`,'VISUAL GUIDE / PROJECT DIAGRAM')});
const visual=document.createElement('div');visual.id='homeVisualGuides';visual.innerHTML='<div class="sectionhead"><div><div class="eyebrow">VISUAL GUIDES</div><h2>先看关系，再读术语</h2><p>从一张图进入，继续点到每条记录与它的依据。</p></div><a class="btn secondary small" href="#library" id="allFiguresLink">全部图解 →</a></div><div class="grid two">'+D.figures.filter(f=>/04_|06_/.test(f.id)).map(figureCard).join('')+'</div>';
$('home').insertBefore(visual,$('home').querySelector('.endnote'));
$('allFiguresLink').addEventListener('click',()=>{libMode='media';document.querySelectorAll('[data-lib]').forEach(x=>x.classList.toggle('active',x.dataset.lib==='media'))});
renderStories();
</script>
'''

def main():
    html_path=ROOT/'build/Dharma-Atlas-v0.7.html';html=html_path.read_text()
    match=re.search(r'(<script id="atlas-data" type="application/json">)(.*?)(</script>)',html,re.S)
    if not match:raise ValueError('Embedded data missing')
    data=json.loads(match[2]);figures=[];assets=ROOT/'docs/review/assets';assets.mkdir(parents=True,exist_ok=True)
    try:
        import cairosvg
        for stem,title in TITLES.items():
            source=ROOT/f'docs/infographics/{stem}.svg'
            if not source.exists():continue
            target=assets/f'{stem}.png'
            cairosvg.svg2png(bytestring=source.read_bytes(),write_to=str(target),output_width=1600)
            png=target.read_bytes()
            figures.append({'id':stem,'title':title,'data':'data:image/png;base64,'+base64.b64encode(png).decode(),'source_file':str(source.relative_to(ROOT)),'png_sha256':hashlib.sha256(png).hexdigest(),'status':'project_teaching_diagram_not_historical_object','rights':'Project-authored diagram exported from the existing repository; not a third-party manuscript image.'})
    except ImportError:
        raise RuntimeError('Install CairoSVG to create the public PNG exports; do not silently omit promised diagrams.')
    assert len(figures)==6,'All six project diagrams must be available'
    data['figures']=figures;data['meta']['counts']['public_png_infographics']=6
    embedded=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    html=html[:match.start(2)]+embedded+html[match.end(2):]
    html=html.replace('</body>',RUNTIME+'\n</body>')
    for path in ['build/site/index.html','build/Dharma-Atlas-v0.7.html','docs/review/index.html']:
        (ROOT/path).write_text(html)
    release_path=ROOT/'build/release-manifest.json';release=json.loads(release_path.read_text())
    release['html_sha256']=hashlib.sha256(html.encode()).hexdigest();release['counts']['public_png_infographics']=6
    release['finalizer_source_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    release['figure_exports']=[{k:v for k,v in f.items() if k!='data'} for f in figures]
    release_path.write_text(json.dumps(release,ensure_ascii=False,indent=2))
    (assets/'README.md').write_text('# Project infographic PNG exports\n\nSix existing project diagrams, exported to PNG for the review website. These are teaching schematics, not images of manuscripts or independently verified historical maps. Dates and routes must be checked against item-level evidence.\n')
    print(json.dumps({'png_infographics':len(figures),'standalone_html_bytes':len(html.encode()),'storage_feedback':'unavailable persistence explicitly distinguished from in-session state'},ensure_ascii=False))
if __name__=='__main__':main()

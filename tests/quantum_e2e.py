"""Functional browser QA; supports local DOM snapshots or a real HTTP URL."""
import argparse
import json
import re
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('--url')
p.add_argument('--out', default='build/quantum-qa')
a = p.parse_args()
ROOT = Path(__file__).resolve().parents[1]
out = Path(a.out)
out.mkdir(parents=True, exist_ok=True)
checks = []
errors = []
def check(name, condition):
    checks.append({'name': name, 'passed': bool(condition)})
    assert condition, name

def cjk(s):
    return bool(re.search(r'[\u3400-\u9fff]', s))

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=shutil.which('chromium') or None)
    page = browser.new_page(viewport={'width':1440,'height':1100}, reduced_motion='reduce')
    page.on('pageerror', lambda e: errors.append(str(e)))
    if a.url:
        response = page.goto(a.url, wait_until='networkidle')
        check('HTTP 200', response.status == 200)
    else:
        page.set_content((ROOT/'quantum/index.html').read_text(encoding='utf-8'), wait_until='load')
    check('Expected build', page.evaluate('window.QURI_BUILD') == '0.2.0-cosmic-bilingual')
    page.locator('[data-lang=zh]').click()
    check('Chinese document language', page.locator('html').get_attribute('lang') == 'zh-CN')
    check('24 concepts', page.locator('.concept').count() == 24)
    check('20 sources', page.locator('.source').count() == 20)
    check('Dark background', page.evaluate("getComputedStyle(document.body).backgroundColor") == 'rgb(7, 11, 24)')
    page.screenshot(path=str(out/'desktop-zh.png'))
    page.locator('.concept[data-entry=Q004]').click()
    page.locator('[data-read=Q004]').click()
    page.locator('[data-action=close]').click()
    check('Progress updates', '1 / 24' in page.locator('#progress').inner_text())
    page.locator('[data-lang=en]').click()
    check('English document language', page.locator('html').get_attribute('lang') == 'en')
    check('Shared progress across language', '1 / 24' in page.locator('#progress').inner_text())
    check('English title', not cjk(page.title()))
    page.evaluate('document.querySelectorAll("details").forEach(d=>d.open=true)')
    check('No Chinese body text except language switch', not cjk(page.locator('body').inner_text().replace('中文','')))
    page.evaluate('document.querySelectorAll("details").forEach(d=>d.open=false)')
    page.screenshot(path=str(out/'desktop-en.png'))
    for i in range(1,25):
        id = f'Q{i:03d}'
        page.locator(f'.concept[data-entry={id}]').click()
        check(id+' English modal', not cjk(page.locator('#entryDialog').inner_text()))
        check(id+' source link', page.locator('#entryDialog a').count() > 0)
        page.locator('[data-action=close]').click()
    page.locator('#search').fill('纠缠')
    check('Chinese search in English mode', page.locator('.concept[data-entry=Q014]').count() == 1)
    page.locator('#search').fill('wavefunction')
    check('English search', page.locator('.concept[data-entry=Q006]').count() == 1)
    page.locator('#search').fill('')
    page.locator('[data-cat=matter]').click()
    check('Category filter', page.locator('.concept').count() == 4)
    page.locator('[data-cat=all]').click()
    page.locator('[data-path=spiritual]').click()
    check('Spiritual path', page.locator('#steps button').count() == 8)
    page.locator('[data-action=many]').click()
    check('Double-slit samples', '200' in page.locator('#labValue').inner_text())
    page.locator('[data-lang=zh]').click()
    check('Samples preserved across language switch', '200' in page.locator('#labValue').inner_text())
    page.locator('#detector').check()
    check('Which-path sets zero visibility', 'V = 0.00' in page.locator('#labValue').inner_text())
    check('Changing conditions clears samples', page.locator('#labValue').inner_text().startswith('已累积 0'))
    check('Visibility disabled when distinguishable', page.locator('#visibility').is_disabled())
    page.locator('[data-lang=en]').click()
    page.evaluate('''window.canvasText=[];const f=CanvasRenderingContext2D.prototype.fillText;
CanvasRenderingContext2D.prototype.fillText=function(s,...a){window.canvasText.push(s);return f.call(this,s,...a)};null''')
    for model in ['slits','phase','uncertainty','bell']:
        page.locator(f'[data-lab={model}]').click()
        check(model+' English controls and explanations', not cjk(page.locator('.labs').inner_text()))
    check('All canvas labels English', not cjk(' '.join(page.evaluate('window.canvasText'))))
    check('Bell quantum maximum', '2.828' in page.locator('#labValue').inner_text())
    page.locator('[data-action=pairs]').click()
    check('Bell sampling disclaimer', 'not S estimated' in page.locator('#pairStats').inner_text())
    page.locator('#theta').evaluate("e=>{e.value='0';e.dispatchEvent(new Event('input',{bubbles:true}))}")
    check('Bell local bound', '2.000' in page.locator('#labValue').inner_text())
    page.locator('[data-lab=phase]').click()
    page.locator('#phase').evaluate("e=>{e.value='180';e.dispatchEvent(new Event('input',{bubbles:true}))}")
    check('Destructive interference', 'amplitude = 0.00' in page.locator('#labValue').inner_text())
    page.locator('[data-lab=uncertainty]').click()
    page.locator('#width').evaluate("e=>{e.value='1';e.dispatchEvent(new Event('input',{bubbles:true}))}")
    check('Minimum Gaussian uncertainty', 'ΔxΔp = 0.50' in page.locator('#labValue').inner_text())
    for i in range(6):
        page.locator(f'[data-time="{i}"]').click()
        check('Timeline '+str(i)+' English', not cjk(page.locator('#timecard').inner_text()))
    check('Desktop width', page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
    for language in ['en','zh']:
        page.locator(f'[data-lang={language}]').click()
        svg=page.locator('#atlasSvg').evaluate('(s)=>new XMLSerializer().serializeToString(s)')
        (out/f'knowledge-map-{language}.svg').write_text(svg, encoding='utf-8')
        page.set_viewport_size({'width':390,'height':900})
        page.wait_for_timeout(200)
        page.evaluate('scrollTo(0,0)')
        page.screenshot(path=str(out/f'mobile-{language}.png'))
        check('Mobile '+language+' width', page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
        check('Mobile '+language+' vertical map', page.locator('#atlasSvg').get_attribute('viewBox')=='0 0 420 940')
        page.locator('.concept[data-entry=Q021]').click()
        box=page.locator('#entryDialog').bounding_box()
        check('Mobile '+language+' dialog fits', box['x']>=0 and box['x']+box['width']<=390)
        page.locator('[data-action=close]').click()
        page.locator('[data-lab=slits]').click()
        page.locator('[data-action=one]').click()
        check('Mobile '+language+' sample button', page.locator('#labValue').inner_text().startswith('Detections: 1' if language=='en' else '已累积 1'))
        page.locator('[data-action=clear]').click()
        page.set_viewport_size({'width':1440,'height':1100})
        page.wait_for_timeout(200)
    if a.url:
        page.locator('[data-lang=en]').click()
        page.reload(wait_until='networkidle')
        check('Language persists on reload', page.locator('html').get_attribute('lang')=='en')
        check('Reading persists on reload', '1 / 24' in page.locator('#progress').inner_text())
        check('Language URL parameter', 'lang=en' in page.url)
        with page.expect_download() as dl:
            page.locator('[data-action=export]').click()
        download=dl.value
        download.save_as(str(out/download.suggested_filename))
        check('SVG download English filename', download.suggested_filename=='QuriAtlas-map-en.svg')
    check('No JS errors', not errors)
    browser.close()
report={'build':'0.2.0-cosmic-bilingual','mode':'HTTP' if a.url else 'offline DOM snapshot','url':a.url,
        'passed':len(checks),'checks':checks,'javascript_errors':errors,
        'not_claimed':['exhaustive research coverage','independent physics review','DNS or custom-domain verification']}
(out/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(checks),'mode':report['mode'],'url':a.url}))

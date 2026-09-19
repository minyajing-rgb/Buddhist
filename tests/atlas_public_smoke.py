#!/usr/bin/env python3
"""Browser smoke checks against actual HTTP, with explicit DOM readiness waits."""
from __future__ import annotations
import argparse, datetime, hashlib, json, pathlib, urllib.request
from playwright.sync_api import sync_playwright

def main():
    a=argparse.ArgumentParser();a.add_argument('--url',required=True);a.add_argument('--out',required=True);args=a.parse_args()
    out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    checks=[];errors=[]
    def check(name,condition):
        checks.append({'name':name,'passed':bool(condition)})
        if not condition:raise AssertionError(name)
    report={'url':args.url,'verification_mode':'actual_http_navigation','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(args.url,timeout=30) as response:
            html=response.read();check('Public/local HTTP returns 200',response.status==200)
            report['html_sha256']=hashlib.sha256(html).hexdigest()
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            context=browser.new_context(viewport={'width':1440,'height':1000})
            page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(args.url,wait_until='load',timeout=60000)
            page.wait_for_selector('#homeStats .stat')
            check('Published beta notice visible','公开研究预览' in page.locator('.notice').inner_text())
            check('100 embedded unique works',page.evaluate('D.works.length===100 && new Set(D.works.map(w=>w.work_id)).size===100'))
            check('12 readable story bodies',page.evaluate('D.stories.length===12 && D.stories.every(s=>s.body.length>300)'))
            page.screenshot(path=str(out/'desktop-home.png'),full_page=True)
            page.locator('nav a[href="#works"]').click();page.locator('#workQuery').fill('心经')
            check('Search returns Heart Sutra',page.locator('#workGrid').inner_text().find('心经')>=0)
            page.locator('#workGrid [data-action="work"]').first.click()
            check('Work detail opens',page.locator('#modal').is_visible())
            page.locator('#closeModal').click()
            page.locator('#workQuery').fill('zzzzz-no-such-work')
            check('Empty search state',page.locator('#workGrid .empty').count()==1)
            page.locator('#workQuery').fill('')
            page.locator('#workGrid input[data-compare]').nth(0).check();page.locator('#workGrid input[data-compare]').nth(1).check()
            page.locator('[data-action="compare"]').click()
            check('Comparison displays two works',page.locator('.comparegrid .card').count()==2)
            page.locator('#closeModal').click();page.locator('[data-action="clear-compare"]').click()
            opened=page.evaluate('''() => {let n=0;for(const w of D.works){openWork(w.work_id);if(document.querySelector('#modalTitle').textContent!==w.titles.zh)throw Error(w.work_id);closeModal();n++;}return n;}''')
            check('All 100 work details open',opened==100)
            page.locator('nav a[href="#stories"]').click();page.locator('#storyGrid [data-action="story"]').first.click()
            check('Story text renders',len(page.locator('#modalBody .prose').inner_text())>300)
            page.locator('[data-action="complete-story"]').click();page.locator('#closeModal').click();page.reload(wait_until='load')
            check('Reading progress persists after reload',page.evaluate('completed.has(0)'))
            page.locator('nav a[href="#atlas"]').click()
            page.wait_for_function("document.querySelectorAll('#eventList .eventitem').length===D.events.length")
            before=page.locator('#eventList .eventitem').count()
            page.locator('#yearRange').fill('868')
            page.locator('#yearRange').dispatch_event('input')
            page.wait_for_function("document.querySelectorAll('#eventList .eventitem').length===D.events.filter(e=>e.start<=868).length")
            check('Year filter changes event count',page.locator('#eventList .eventitem').count()<before)
            page.locator('[data-map="libraries"]').click();check('Modern libraries not filtered by ancient date',page.locator('#yearRange').is_disabled())
            page.locator('nav a[href="#library"]').click();page.locator('[data-lib="media"]').click()
            page.wait_for_function("document.querySelectorAll('#libraryGrid [data-figure]').length===6")
            check('Six PNG guides available',page.locator('#libraryGrid [data-figure]').count()==6)
            page.locator('#libraryGrid [data-figure]').first.click();check('PNG enlarges in modal',page.locator('#modal img').count()==1);page.locator('#closeModal').click()
            page.locator('nav a[href="#research"]').click()
            page.wait_for_function("document.querySelectorAll('#researchBody .methodrow').length===33")
            check('33 methods render',page.locator('#researchBody .methodrow').count()==33)
            page.locator('[data-research="sources"]').click();check('44 source cards render',page.locator('#sourceGrid .card').count()==44)
            page.locator('[data-research="quality"]').click();check('QA visible',page.locator('#researchBody .notebox').count()>=4)
            for width in [390,768]:
                page.set_viewport_size({'width':width,'height':844})
                for route in ['home','works','atlas','library']:
                    page.evaluate('(route)=>{location.hash=route;navigate()}',route)
                    page.wait_for_function('(route)=>!document.getElementById(route).hidden',arg=route)
                    check(f'No page overflow {width}px {route}',page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'))
            page.set_viewport_size({'width':390,'height':844});page.evaluate("location.hash='home';navigate()")
            page.screenshot(path=str(out/'mobile-home.png'),full_page=True)
            check('No observed runtime errors',not errors)
            browser.close()
        report['status']='passed'
    except Exception as e:
        report['status']='failed';report['error']=str(e)
        raise
    finally:
        report.update({'passed':sum(x['passed'] for x in checks),'total':len(checks),'checks':checks,'runtime_errors':errors,'limitations':['Functional smoke checks are not scholarly review.','Current interface is Chinese; complete English localization remains a separate task.','No guarantee is made about every external source URL or all browser engines.']})
        (out/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
        print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

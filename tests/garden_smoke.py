#!/usr/bin/env python3
"""Browser checks over real HTTP; also test the public serving boundary.
UI correctness is not a certification of scholarly content or repository privacy.
"""
import argparse,hashlib,json,pathlib,time,urllib.error,urllib.request
from playwright.sync_api import sync_playwright

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--url',required=True);ap.add_argument('--out',default='build/garden-qa');ap.add_argument('--executable');ap.add_argument('--skip-boundary',action='store_true');args=ap.parse_args()
    dest=pathlib.Path(args.out);dest.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
    def check(name,ok,detail=None):
        checks.append({'name':name,'passed':bool(ok),'detail':detail})
        if not ok:raise AssertionError(name+': '+str(detail))
    with sync_playwright() as p:
        opts={'headless':True}
        if args.executable:opts['executable_path']=args.executable
        browser=p.chromium.launch(**opts);context=browser.new_context(viewport={'width':1440,'height':1060},device_scale_factor=1)
        page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(args.url+'?lang=zh',wait_until='networkidle',timeout=60000)
        check('Homepage visible',page.locator('.hero-copy h1').is_visible())
        check('Six visual exploration portals',page.locator('#heroPortalDeck .portal-card').count()==6)
        check('Gamified journey entry visible',page.locator('#journeyButton').is_visible())
        page.locator('#journeyButton').click();page.wait_for_timeout(80);check('Journey drawer opens',page.locator('#journeyDrawer').get_attribute('aria-hidden')=='false' and page.locator('.stamp-grid .stamp').count()==6);page.locator('[data-close-journey]').click();page.wait_for_timeout(40)
        check('Garden PNG loaded',page.request.get(args.url+'assets/garden.png').status==200)
        content=page.eval_on_selector('#public-content','e=>JSON.parse(e.textContent)')
        check('100 texts preserved',len(content['works'])==100)
        check('12 bilingual stories',len(content['stories'])==12 and all(len(s['body_en'])>350 and len(s['body_zh'])>100 for s in content['stories']))
        raw=json.dumps(content,ensure_ascii=False)
        check('No raw research or own-repository identifiers',not any(x.lower() in raw.lower() for x in ['minyajing-rgb','github.com','githubusercontent.com','review_flags','source_commit','canonical_datasets','DA-W-','WIT-']))
        check('No repository links in homepage',page.locator('a[href*="github"]').count()==0)
        page.screenshot(path=str(dest/'desktop-home.png'),full_page=True)
        page.screenshot(path=str(dest/'desktop-first-screen.png'))
        def route(h):
            page.evaluate('(h)=>location.hash=h',h)
            page.locator('#'+h).wait_for(state='visible')
            page.wait_for_timeout(80)
        def close():
            if page.locator('#modal').evaluate('e=>e.open'):page.locator('#closeModal').click()
        route('works');check('First page has 18 text cards',page.locator('#workGrid .work-card').count()==18)
        page.locator('#workQuery').fill('心经');check('Chinese search',page.locator('#workGrid').inner_text().find('般若波罗蜜多心经')>=0)
        page.locator('#workGrid [data-act="work"]').first.click();check('Text details open',page.locator('#modal').evaluate('e=>e.open'));close()
        page.locator('#workQuery').fill('SN 56.11');check('Catalogue number search',page.locator('#workGrid .work-card').count()>=1)
        page.locator('#workQuery').fill('');page.locator('#evidenceFilter').select_option('books');check('Bibliography filter',str(sum(bool(w['books']) for w in content['works'])) in page.locator('#workCount').inner_text())
        page.locator('#evidenceFilter').select_option('objects');check('Object filter',page.locator('#workGrid .work-card').count()==sum(bool(w['objects']) for w in content['works']))
        page.locator('#evidenceFilter').select_option('all');page.locator('[data-choose]').nth(0).check();page.locator('[data-choose]').nth(1).check();page.locator('[data-act="compare"]').click();check('Two-text comparison',page.locator('.compare-grid .card').count()==2);close();page.locator('[data-act="clear"]').click()
        page.locator('#workGrid [data-act="bookmark"]').first.click();page.locator('#savedOnly').check();check('Bookmark filtering',page.locator('#workGrid .work-card').count()==1);page.reload(wait_until='networkidle');page.locator('#savedOnly').check();check('Bookmark persists after refresh',page.locator('#workGrid .work-card').count()==1);page.locator('#savedOnly').uncheck()
        page.evaluate('for (const w of A.works) { showWork(w.id); if (!document.getElementById("modalTitle").textContent) throw Error(w.id); closeModal(); }')
        check('All 100 text details render',not errors,errors)
        route('stories');check('12 story cards render',page.locator('#storyGrid .story-card').count()==12);page.locator('#storyGrid [data-act="story"]').first.click();check('Story has full body',len(page.locator('.prose').inner_text())>100);page.locator('[data-act="read"]').click();close();page.reload(wait_until='networkidle');check('Reading progress persists', '1 / 12' in page.locator('#readingStatus').inner_text())
        route('atlas');check('Seven sourced events',page.locator('#eventList .event').count()==7);page.locator('#yearRange').fill('868');check('Year slider uses dated events',page.locator('#eventList .event').count()==2);page.locator('[data-tab="map"][data-value="libraries"]').click();check('Modern libraries separated from ancient dates',page.locator('#yearRange').is_disabled() and page.locator('#placeButtons button').count()==17)
        route('people');check('People collection retained',page.locator('#peopleGrid .card').count()==len(content['people']))
        route('library');check('Object collection retained',page.locator('#libraryGrid .card').count()==len(content['objects']));page.locator('[data-tab="library"][data-value="figures"]').click();check('Six visual guides',page.locator('.library-figure').count()==6)
        for f in content['figures']:check('Guide asset: '+f['id'],page.request.get(args.url+f['src'].removeprefix('./')).status==200)
        route('about');check('33 public method cards',page.locator('#aboutBody .card').count()==33);page.locator('[data-tab="about"][data-value="sources"]').click();check('Institutional sources retained',page.locator('#aboutBody .card').count()==len(content['sources']))
        route('home');page.locator('#langToggle').click();check('English is separately selectable',page.locator('html').get_attribute('lang')=='en' and 'lang=en' in page.url)
        check('English homepage copy', 'Dharma Atlas' in page.locator('.hero-copy').inner_text() and 'Places · People · Wisdom' in page.locator('.hero-copy').inner_text())
        page.screenshot(path=str(dest/'desktop-english.png'))
        route('stories');page.locator('#storyGrid [data-act="story"]').first.click();check('English story body', 'shared memory' in page.locator('.prose').inner_text());close()
        route('works');page.locator('#workQuery').fill('Heart Sutra');check('English transliteration search',page.locator('#workGrid .work-card').count()>=1)
        page.locator('#workGrid [data-act="work"]').first.click();check('English text details', 'A place to start' in page.locator('#modalBody').inner_text());close()
        page.locator('#langToggle').click();route('home')
        for width in [390,360]:
            page.set_viewport_size({'width':width,'height':844});route('home');check('Mobile homepage no overflow '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
            page.locator('#menuToggle').click();page.locator('#nav').wait_for(state='visible');check('Mobile navigation opens '+str(width),page.locator('#nav').is_visible())
            page.locator('#nav a[href="#works"]').click();page.locator('#works').wait_for(state='visible');check('Mobile navigation works '+str(width),page.locator('#works').is_visible())
            page.locator('#workQuery').fill('');page.locator('#workGrid [data-act="work"]').first.click();check('Mobile dialog fits '+str(width),page.locator('#modal').bounding_box()['width']<=width);close();route('atlas');check('Mobile map no overflow '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.set_viewport_size({'width':390,'height':844});route('home');page.screenshot(path=str(dest/'mobile-home.png'),full_page=True)
        check('No JavaScript errors',not errors,errors)
        check('No backend/export links added by interactions',page.locator('a[href*="github"],a[href$=".json"]').count()==0)
        if not args.skip_boundary:
            for path in ['data/CURRENT.json','review/index.html','release.json','public_deployment.json','archive/pre-public-beta/index.html','research_audit_v0.7.json']:
                response=page.request.get(args.url+path)
                check('Internal path not served: '+path,response.status==404,response.status)
        browser.close()
    report={'url':args.url,'passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'javascript_errors':errors,'tested_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'limits':['UI and serving-boundary tests are not scholarly certification.','Public repository visibility is unchanged.','Existing third-party source links are not all live-checked.']}
    (dest/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False))
if __name__=='__main__':main()

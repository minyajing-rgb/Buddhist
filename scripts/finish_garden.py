#!/usr/bin/env python3
"""Stage approved cinematic visitor assets; never silently fall back to SVG."""
from pathlib import Path
import hashlib,json,re,shutil
from build_garden import stage_public
ROOT=Path(__file__).resolve().parents[1]
ASSETS=('sacred-world.webp','sacred-world-mobile.webp','garden.png','map.webp','texts.webp','places.webp','people.webp','timeline.webp','library.webp')

def main():
    asset_dir=ROOT/'web/garden/cinematic-assets'
    for name in ASSETS:
        path=asset_dir/name
        if not path.is_file() or path.stat().st_size<1000:
            raise FileNotFoundError(f'Required approved cinematic asset missing: {path}')
    page=ROOT/'docs/garden/index.html';html=page.read_text()
    if 'href="./enhancements.css' not in html:
        html=html.replace('</head>','<link rel="stylesheet" href="./enhancements.css"></head>')
    if 'src="./enhancements.js' not in html:
        html=html.replace('</body>','<script src="./enhancements.js" defer></script></body>')
    if 'name="dharma-ui-release"' not in html:
        html=html.replace('</head>','<meta name="dharma-ui-release" content="cinematic-4.0"><link rel="preload" href="./assets/sacred-world.webp" as="image"></head>')
    html=re.sub(r'<title>.*?</title>','<title>Dharma Atlas · 佛典世界</title>',html,count=1)
    html=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="探索佛典世界。沿着圣地、人物、经典与馆藏，开启可互动的智慧旅程。">',html,count=1)
    for name in ('garden.css','garden.js','enhancements.css','enhancements.js'):
        html=html.replace('./'+name+'"','./'+name+'?v=cinematic-4.0"')
    page.write_text(html)
    for name in ('enhancements.css','enhancements.js'):
        shutil.copyfile(ROOT/'web/garden'/name,ROOT/'docs/garden'/name)
    for name in ASSETS:
        shutil.copyfile(asset_dir/name,ROOT/'docs/garden/assets'/name)
    shutil.copyfile(page,ROOT/'docs/index.html')
    dest=stage_public()
    manifest=ROOT/'build/garden-release.json';data=json.loads(manifest.read_text())
    data.update(ui_release='cinematic-4.0',homepage_sha256=hashlib.sha256(html.encode()).hexdigest(),garden_html_bytes=len(html.encode()))
    data['public_files']=sorted(str(p.relative_to(dest)) for p in dest.rglob('*') if p.is_file())
    data['cinematic_asset_sha256']={n:hashlib.sha256((asset_dir/n).read_bytes()).hexdigest() for n in ASSETS}
    data['ux_refinements']=['independent no-text cinematic raster artwork','live multilingual HTML interface','cross-entity search','scene hotspots and guided journey','native accessible journey dialog','local learning progress','quiet view and motion controls','mobile scene art direction','no fallback to the old vector garden','versioned CSS and JavaScript URLs']
    manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2))
    print('Cinematic v4 visitor distribution staged. Publication requires successful deployment and HTTPS verification.')
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Add small public UX refinements, then refresh the allowlisted distribution."""
import hashlib,json,pathlib,shutil
from build_garden import stage_public
ROOT=pathlib.Path(__file__).resolve().parents[1]

def main():
    page=ROOT/'docs/garden/index.html';html=page.read_text()
    if 'href="./enhancements.css"' not in html:
        html=html.replace('</head>','<link rel="stylesheet" href="./enhancements.css"></head>')
    if 'src="./enhancements.js"' not in html:
        html=html.replace('</body>','<script src="./enhancements.js" defer></script></body>')
    page.write_text(html)
    for name in ['enhancements.css','enhancements.js']:
        shutil.copyfile(ROOT/'web/garden'/name,ROOT/'docs/garden'/name)
    shutil.copyfile(page,ROOT/'docs/index.html')
    dest=stage_public()
    manifest=ROOT/'build/garden-release.json';data=json.loads(manifest.read_text())
    data['ui_release']='garden-1.0.1'
    data['homepage_sha256']=hashlib.sha256(html.encode()).hexdigest()
    data['garden_html_bytes']=len(html.encode())
    data['public_files']=sorted(str(p.relative_to(dest)) for p in dest.rglob('*') if p.is_file())
    data['ux_refinements']=['mobile art composition retains flowering trees','in-page anchors do not reset the route','reduced-motion respected']
    manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2))
    print('Garden responsive artwork and in-page navigation refinements included.')
if __name__=='__main__':main()

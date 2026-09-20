"""Rebuild the bilingual Atlantis site from the canonical corpus pointer.
Generated HTML is a reproducible snapshot, not a separate content master.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / 'data/CURRENT.json').read_text(encoding='utf-8'))
path = (ROOT / 'data' / manifest['dataset']).resolve()
if not path.is_relative_to((ROOT / 'data').resolve()):
    raise ValueError('The corpus must be inside quantum/data')
data = json.loads(path.read_text(encoding='utf-8'))
en = json.loads((ROOT / 'site/en.json').read_text(encoding='utf-8'))
assert {e['id'] for e in data['entries']} == set(en['entries']), 'Missing English concepts'
assert all(len(v) == 4 for v in en['entries'].values()), 'Incomplete concept translation'
for key in ('categories', 'bridges', 'timeline'):
    assert len(en[key]) == len(data[key]), 'Translation count mismatch: ' + key
assert len(en['domains']) == len(data['expansion_plan']['domains'])
assert all(s['id'] in en['source_limits'] for s in data['sources'] if s.get('limitation'))
def pack(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
css = (ROOT / 'site/style.css').read_text(encoding='utf-8') + (ROOT / 'site/mobile.css').read_text(encoding='utf-8')
js = (ROOT / 'site/app.js').read_text(encoding='utf-8')
page = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="theme-color" content="#f7faff">
<title>量子漫游 QuriAtlas | Interactive Quantum Physics</title>
<meta name="description" content="A bilingual quantum learning atlas with stories, interactive experiments, and traceable sources.">
<meta name="quri-build" content="0.3.0-atlantis-bilingual">
<style>''' + css + '''</style></head><body>
<div id="app"></div><dialog id="entryDialog"></dialog>
<noscript>This interactive atlas requires JavaScript. 本互动知识地图需要启用 JavaScript。</noscript>
<script id="atlas-data" type="application/json">''' + pack(data) + '''</script>
<script id="english-data" type="application/json">''' + pack(en) + '''</script>
<script>''' + js + '''</script></body></html>'''
for out in (ROOT / 'index.html', ROOT.parent / 'docs/quantum/index.html'):
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding='utf-8')
print(json.dumps({'build': '0.3.0-atlantis-bilingual', 'concepts': len(data['entries']),
                  'sources': len(data['sources']), 'bytes': len(page.encode()),
                  'sha256': hashlib.sha256(page.encode()).hexdigest()}))

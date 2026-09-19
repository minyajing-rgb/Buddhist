"""Build a standalone HTML snapshot from the canonical CURRENT.json pointer."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / 'data' / 'CURRENT.json').read_text(encoding='utf-8'))
data_path = (ROOT / 'data' / manifest['dataset']).resolve()
if not data_path.is_relative_to(ROOT.resolve()):
    raise ValueError('Dataset must remain within this project')
data = json.loads(data_path.read_text(encoding='utf-8'))
page = (ROOT / 'index.html').read_text(encoding='utf-8')
marker = '<script>\n'
if marker not in page:
    raise ValueError('Application script marker not found')
snapshot = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
page = page.replace(marker, '<script id="offline-data" type="application/json">' + snapshot + '</script>\n' + marker, 1)
out = ROOT / 'preview.html'
out.write_text(page, encoding='utf-8')
print(f'Wrote {out.name}: {len(data["entries"])} concepts, {len(data["sources"])} sources')

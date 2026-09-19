"""Rebuild the bilingual site and export its self-contained HTML."""
from pathlib import Path
import runpy
import shutil

ROOT = Path(__file__).resolve().parent
runpy.run_path(str(ROOT / 'build.py'), run_name='__main__')
out = ROOT / 'preview.html'
shutil.copyfile(ROOT / 'index.html', out)
print(f'Offline bilingual preview: {out}')

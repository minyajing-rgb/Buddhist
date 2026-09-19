# 量子漫游 / QuriAtlas

> 从一束光，走进量子世界。  
> A spark of light. A quantum universe.

## v0.2.0 — Cosmic / 中文 + English

The quantum project is isolated from the existing Buddhist website and its canonical corpus.

- 深空蓝、紫青色光晕、细金线、原创星空与波纹 SVG；支持减少动效。
- Complete Chinese/English switching: navigation, 24 concept cards and full explanations, six bridge questions, six timeline records, evidence limits, source labels, diagrams, canvas text and controls.
- `?lang=zh` / `?lang=en` direct entry links; browser language preference, shared reading progress, bilingual search.
- Language switching preserves experimental settings and accumulated samples.
- Four teaching models: double slit, phase interference, Gaussian uncertainty, and ideal CHSH correlations. These are not live experiments.
- Responsive desktop/mobile layout; localized editable SVG export.

## Published route and verification

Target route: https://minyajing-rgb.github.io/Buddhist/quantum/

Chinese: `?lang=zh` · English: `?lang=en`

The workflow `.github/workflows/quantum-site.yml` builds, tests, commits the derived HTML, requests a build through the existing branch-based Pages configuration, waits for a byte-for-byte SHA256 match on the public URL, then runs the interaction tests on that URL.

A successful source commit alone is **not** deployment verification. Public verification is recorded, only after success, in `data/qa.v0.2.public.json` and the workflow artifact `quriatlas-cosmic-bilingual`.

## Rebuild / offline export

Requires Python 3.9+; the browser page has no package/CDN dependencies.

```sh
python quantum/build.py
# outputs: quantum/index.html and docs/quantum/index.html

python quantum/export_offline.py
# optional additional output: quantum/preview.html
```

The HTML includes generated snapshots of the canonical corpus and English translation layer. It opens offline in a modern JavaScript-capable browser; external source links need a connection. `file://` local storage behavior is browser-dependent. HTTP/HTTPS storage is separately tested in CI.

## Canonical files

| File | Role |
|---|---|
| `data/CURRENT.json` | Canonical corpus pointer; unchanged by visual localization work |
| `data/atlas.v0.1.json` | 24 concepts, 6 bridge questions, 6 timeline records, 20 sources |
| `site/en.json` | Full English translations linked to the same stable IDs |
| `site/app.js` | Bilingual UI and interactive model logic |
| `site/style.css`, `site/mobile.css` | Responsive cosmic visual system |
| `build.py` | Reproducible standalone HTML generation |
| `../tests/quantum_e2e.py` | Browser, language, model, mobile, persistence and export checks |
| `../docs/quantum/index.html` | Derived Pages entry, not a separate content master |

Historical v0.1 artwork and QA remain archived; the live knowledge map is now generated in both languages from current data.

## QA and scientific scope

Local offline-DOM verification passed 93 checks. The same suite has additional HTTP, reload/persistence and browser-download checks when `--url` is supplied. Consult the actual public report rather than inferring success from this README.

This update does not expand the seed corpus or complete a systematic literature review. 360 records remains a roadmap target, not current coverage. Independent physics review, full-text/raw-data verification, complete multilingual research and original-media rights expansion remain separate research work. The brand remains a working proposal, not a trademark-clearance claim.

## Domain handoff

See `DOMAIN_HANDOFF.md`. The current repository's `/docs` root remains the Buddhist website. DNS cannot select `/quantum/`; do not bind a quantum-only domain to this shared root expecting automatic path selection. The generated quantum HTML can instead be deployed as the root of a separate static site, without rewriting its asset paths.

## Change log

- 2026-09-19 / v0.2.0: complete bilingual UI/content, dark cosmic identity, preserved model state, mobile language-control fix, reproducible build and public verification workflow.
- 2026-09-19 / v0.1.0: source-linked quantum seed corpus and four interactive teaching models.

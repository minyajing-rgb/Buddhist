> **MOVED TO QURIATLAS / 已迁移**  
> 量子物理项目的独立主仓库现为 **https://github.com/minyajing-rgb/QuriAtlas**。此目录保留为迁移前历史快照，不再作为新的产品主库。  
> Standalone canonical repository: **minyajing-rgb/QuriAtlas**.

# 量子漫游 / QuriAtlas

> 从一束光，走进量子世界。  
> A spark of light. A quantum universe.

## v0.2.0 — Cosmic / 中文 + English — Published

**Live:** https://minyajing-rgb.github.io/Buddhist/quantum/

**中文:** https://minyajing-rgb.github.io/Buddhist/quantum/?lang=zh  
**English:** https://minyajing-rgb.github.io/Buddhist/quantum/?lang=en

Public HTTP verification: **98 checks passed** on 2026-09-19.

- Public report: `data/qa.v0.2.public.json`
- Successful deployment and verification: https://github.com/minyajing-rgb/Buddhist/actions/runs/35435787949
- Published HTML SHA256: `dd79893e4fce5ac6ac817ff2b4922532b825c5615b40501eef987a9e7dd65879`

The quantum project is isolated from the existing Buddhist website and its canonical corpus. The Buddhist homepage remains unchanged.

## What changed

- 深空蓝、紫青色光晕、细金线、原创星空与波纹 SVG；支持减少动效。
- Complete Chinese/English switching: navigation, 24 concept cards and full explanations, six bridge questions, six timeline records, evidence limits, source labels, diagrams, canvas text and controls.
- `?lang=zh` / `?lang=en` direct entry links; saved language preference, shared reading progress, bilingual search.
- Language switching preserves experimental settings and accumulated samples.
- Four teaching models: double slit, phase interference, Gaussian uncertainty, and ideal CHSH correlations. These are not live experiments.
- Responsive desktop/mobile layout; localized editable SVG export.

## Build and publishing

Requires Python 3.9+; the browser page has no package/CDN dependencies.

```sh
python quantum/build.py
# outputs: quantum/index.html and docs/quantum/index.html

python quantum/export_offline.py
# optional additional output: quantum/preview.html
```

The HTML embeds generated snapshots of the canonical corpus and English translation layer. It opens offline in a modern JavaScript-capable browser; external source links need a connection. `file://` storage behavior is browser-dependent; HTTP/HTTPS persistence was separately tested.

`.github/workflows/quantum-site.yml` builds and tests the page over HTTP, archives the generated files, uploads the **complete existing docs site** using `actions/upload-pages-artifact`, and deploys it with `actions/deploy-pages`. It does not replace the Buddhist root or alter domain settings.

The workflow waits for an exact SHA256 match on the public URL, then runs the interaction suite again on that URL. A successful source commit alone is not deployment verification. The first attempt's manual Pages-build API was rejected; the supported artifact deployment action completed successfully in the linked run.

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

Local offline-DOM checks: 93 passed. Local HTTP and public HTTPS checks: 98 passed each, including language/reading persistence on reload and actual SVG downloading. These are product checks, not a physics peer review.

This update does not expand the seed corpus or complete a systematic literature review. 360 records remains a roadmap target, not current coverage. Independent physics review, full-text/raw-data verification, complete multilingual research and original-media rights expansion remain separate work. The brand remains a working proposal, not a trademark-clearance claim.

## Domain handoff

See `DOMAIN_HANDOFF.md`. The current repository's `/docs` root remains the Buddhist website. DNS cannot select `/quantum/`; do not bind a quantum-only domain to this shared root expecting automatic path selection. The generated quantum HTML can instead be deployed as the root of a separate static site, without rewriting asset paths. No Aliyun resources or DNS records were changed.

## Change log

- 2026-09-19 / v0.2.0: complete bilingual UI/content, dark cosmic identity, preserved model state, mobile language-control fix, reproducible build, successful public deployment, and 98 public verification checks.
- 2026-09-19 / v0.1.0: source-linked quantum seed corpus and four interactive teaching models.

# DATABASE STATUS｜Dharma Atlas v0.3

> **Current phase: DATABASE FIRST.**  
> HTML / public-site rebuild remains paused until the database QA gates below are passed.

## Current machine-validated counts

| Layer | Count | Status |
|---|---:|---|
| Authoritative online source/platform entries | **32** | ✅ required-field QA passed |
| Physical library/archive access entries | **15** | ✅ required-field QA passed |
| Geographic map nodes | **27** | ✅ JSON valid |
| People / transmission nodes | **20** | ✅ JSON valid |
| Full-corpus entry points | **15** | ✅ JSON valid |
| Representative key works | **100** | ✅ record count complete; verification depth mixed |
| Current direct text-access crosswalk records | **32** | ✅ initial verified batch |
| Concept-learning entries | **20** | ✅ |
| Learning paths | **5** | ✅ |
| Search / research workflows | **6** | ✅ |
| Landmark manuscript / canon witnesses | **20** | ✅ required-field QA passed |
| Research-dispute dossiers | **12** | ✅ issue-map layer |
| Rights-aware media assets / placeholders | **12** | ✅ |
| Season 1 readable full episodes | **12 / 12** | ✅ no longer outline-only |

Machine QA report: `data/qa_report_v0.3.json`.

## What “100 works” means

`data/key_works_100_v0.3.json` now contains **100 representative works** across:
- early Buddhist / Pāli texts;
- Āgamas and Chinese canons;
- Prajñāpāramitā and major Mahāyāna sūtras;
- Pure Land / tathāgatagarbha / Yogācāra / Madhyamaka;
- Abhidharma and śāstra;
- Tibetan scholastic / path texts;
- East Asian Buddhist works.

**Important:** the first 32 have the stronger v0.2 crosswalk foundation. The next 68 are deliberately marked `needs_id_crosswalk` or `core_id_present_needs_crosscheck` until their version-level IDs are checked. Discovery metadata is not being mislabeled as fully verified data.

## What has changed since the outline-only version

### 1. Season 1 is now real content
`docs/stories/season1_full.md` contains all 12 readable episodes with:
- beginner explanation;
- story/person hook;
- timeline;
- geography;
- evidence/source direction;
- uncertainty / dispute framing;
- next-episode transition.

### 2. “全集” is modeled as corpus entry points + crosswalks
`data/full_canon_entrypoints_v0.3.json` connects:
- Pāli Tipiṭaka;
- early cross-tradition texts;
- Taishō;
- Xuzang;
- Jiaxing;
- Zhaocheng Jin;
- Tripitaka Koreana;
- Kangyur / Tengyur;
- surviving Sanskrit Buddhist literature;
- Gāndhāran manuscripts;
- Dunhuang / Central Asian manuscripts;
- Nepalese Buddhist manuscripts;
- Southeast Asian palm-leaf traditions;
- modern scholarship.

This avoids copying third-party copyrighted full texts while still giving a global “where to find it” master map.

### 3. Online → physical access is now explicit
For a work, the intended research chain is:

```
Work / Title
→ canonical IDs
→ direct authoritative online text
→ parallel/version platforms
→ manuscript/witness record
→ physical holding / shelfmark
→ modern bibliography
```

## Remaining database gates before website rebuild

### Gate A — 100-work authority verification
- [x] 100 representative Work records
- [x] 32 stronger crosswalk records
- [ ] verify version IDs / direct links for remaining 68
- [ ] attach chronology + bibliography status to all priority works

### Gate B — physical evidence
- [x] 20 landmark witnesses
- [ ] expand to 50+ landmark witnesses / collections
- [ ] add item-level shelfmark / IIIF links where available
- [ ] add witness ↔ work relationships

### Gate C — research bibliography
- [x] 12 controversy/research dossiers
- [ ] add paper/book-level bibliography
- [ ] encode attributed scholarly positions
- [ ] add publication year / DOI / stable URL / language

### Gate D — media layer
- [x] rights-aware media registry structure
- [ ] project-owned PNG/JPG visual assets in `docs/assets/img/`
- [ ] YouTube / public video registry
- [ ] 3D/IIIF-compatible asset fields
- [ ] per-asset rights QA

### Gate E — link QA
- [ ] external link-health check for all source/holding URLs
- [ ] redirect/dead-link report
- [ ] replacement/fallback URLs

## Definition of Done

The website phase begins only when the database can answer these questions reliably:

1. **我想学佛教，从哪里开始？**
2. **我听说过某部经，在哪里在线读？**
3. **它有哪些版本/语言/编号？**
4. **原文还在吗？最早实体证据是什么？**
5. **如果线上没有，原件在哪个图书馆/寺院/档案馆？**
6. **我怎么预约、查馆藏号、申请复制？**
7. **这部经有哪些学术争议？谁在研究？**
8. **我只想看故事/视频/地图，不想先学术语，可以怎么进入？**

Until these are covered, **do not label the public product “complete.”**

# DATABASE STATUS｜Dharma Atlas v0.6

> **Current phase: DATABASE FIRST.**  
> Public HTML remains intentionally paused. The next website will be generated from the canonical datasets after database QA.

## Current verified coverage

| Layer | Current | Status |
|---|---:|---|
| Authoritative online source/platform entries | **44** | ✅ |
| Physical library/archive access entries | **17** | ✅ |
| Geographic map nodes | **27** | ✅ |
| People / transmission nodes | **20** | ✅ |
| Full-corpus entry points | **15** | ✅ |
| Representative key works | **100** | ✅ |
| Work access records with ≥1 direct authority route | **100 / 100** | ✅ |
| L3 deep crosswalk records | **100 / 100** | ✅ unified evidence-navigation layer |
| L4 scholar-grade crosswalks | **0 / 100** | 🟡 chronology + item witness + bibliography next |
| Concept-learning entries | **20** | ✅ |
| Learning paths | **5** | ✅ |
| Search/research workflows | **6** | ✅ |
| Landmark manuscript/material witnesses | **24** | 🟡 target 50+ |
| Research-dispute dossiers | **12** | 🟡 paper/book bibliography next |
| Season 1 readable episodes | **12 / 12** | ✅ |

## Important correction to the old status

The old v0.3 status said **46 works still lacked an ID crosswalk**.  
That is now stale.

Current reality:
- all **100 works have at least one direct authority route** in `text_access_index_100_v0.3.json`;
- the work records carry authority-level verification statuses across CBETA / SuttaCentral / 84000 / GRETIL / Tipitaka / Adarshah routes;
- however only the first **32** currently have the deeper v0.2-style Work/Version/parallel foundation.

So the remaining task is **not “find any source for 68 works.”**  
It is to deepen them from **authority route → scholar-grade crosswalk**:

```
Work
→ Versions / recensions
→ canonical IDs
→ parallel relations
→ chronology
→ manuscript / print witnesses
→ physical holdings
→ paper/book bibliography
→ confidence statement
```

## v0.4 regional expansion completed

New/expanded coverage:
- Korea: Dongguk KABC / integrated Buddhist archive
- Nepal: NGMCP / National Archives route
- Sri Lanka: National Library palm-leaf collection
- Thailand: National Library Ancient Manuscript DB + D-Library
- Myanmar: National Library Buddhist Literature + Palm-leaf Digital Collections
- Mongolia: National Library Tibetan/Mongolian catalog + BDRC-linked digitization

See:
- `data/regional_coverage_matrix_v0.4.json`
- `docs/research/GLOBAL_INDEX_METHOD.md`
- `docs/research/OFFLINE_ACCESS_GUIDE.md`

## Remaining gates before website build

### Gate A — deepen 100 key works
- [x] 100 work records
- [x] 100/100 direct authority routes
- [x] 100/100 L3 deep Crosswalk records
- [x] 100/100 direct authority routes
- [x] 100/100 typed Version/Edition routes
- [x] 100/100 physical/material access context
- [x] SuttaCentral official typed parallel extraction for the Pāli sutta batch
- [x] verified Chinese version IDs added where directly checked
- [ ] L4: work-specific chronology for 100/100
- [ ] L4: item-level witness / shelfmark where available
- [ ] L4: paper/book-level bibliography and attributed scholarly positions

### Gate B — physical evidence
- [x] 24 landmark witnesses/collections
- [ ] expand to 50+
- [ ] add more item-level shelfmarks / stable image or IIIF routes
- [ ] connect more witnesses directly to works

### Gate C — scholarly bibliography
- [x] 12 issue dossiers
- [ ] paper/book-level entries
- [ ] attributed scholarly positions
- [ ] DOI / stable URL / year / language

### Gate D — media
- [ ] project PNG/JPG asset package under `docs/assets/img/`
- [ ] YouTube / public video registry
- [ ] 3D / IIIF-compatible media fields
- [ ] rights QA per asset

## Definition of done before HTML

The database must reliably answer:

1. 我从零开始怎么学？
2. 某部经在线在哪里读？
3. 它有哪些语言、版本和编号？
4. 原文是否存世？
5. 最早实体证据是什么？
6. 如果线上没有，原件在哪？
7. 怎么预约、申请复制或查 shelfmark？
8. 学术界对它争什么？
9. 我要只看故事 / 图 / 视频，入口在哪里？
10. 我要做专业 crosswalk，如何从 Work 追到 Witness？

**Until these gates pass, do not call the public product complete and do not rebuild the website shell.**


## v0.6 Crosswalk milestone

`data/deep_crosswalk_100_v0.6.json` is now the canonical 100-work Crosswalk layer.

**L3 means:** authority route + typed version/edition route + material/physical access context + explicit relationship/gap tracking.

It does **not** mean every composition date, manuscript identity, or scholarly controversy is settled.

The next research depth is **L4 Scholar Crosswalk**, not another shallow URL expansion.

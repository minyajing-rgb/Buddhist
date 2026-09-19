# DATABASE STATUS｜Dharma Atlas v0.3

> **Current phase: DATABASE FIRST.**  
> Public-site rebuild is intentionally paused until the content database passes QA.

## Current validated counts

- **32** authoritative online source/platform entries
- **15** physical library/archive access entries
- **27** map nodes
- **20** people/transmission nodes
- **15** full-corpus entry points
- **32** key-text records with access crosswalk
- **20** concept-learning entries
- **5** learning paths
- **6** search/research workflows
- **12** Season 1 episodes now have actual readable content in `docs/stories/season1_full.md`, not outline-only placeholders.

## What is already structurally complete

### 1. Global source layer
Chinese / Pāli / Tibetan / Sanskrit / Gāndhārī / Dunhuang-Central Asian / Korean / Nepalese / Thai / Sri Lankan / modern scholarship entry points are represented.

### 2. Online → offline research chain
The database now records:
- where to read/search online;
- what each source is good for;
- limitations;
- how to query;
- when a physical holding is still needed;
- how to proceed to an archive/library.

### 3. Beginner → scholar learning layer
The content model supports:
- story-first;
- concept-first;
- map-first;
- text-critical research;
- physical-manuscript hunting.

## What is NOT yet allowed to be called “complete”

- The current **32 key texts are not yet a 100+ work representative master index**.
- Landmark manuscript **witness-level records** still need their own table.
- High-priority disputed texts still need a structured **bibliography / positions matrix**.
- Public multimedia (video / image / audio) still needs a rights-aware registry.
- Current SVG files are legacy assets and **must not be the public-facing image format**.
- HTML website visual rebuild has **not started in this database-first phase**.

## Next database gate

The next batch should finish these four tables before any public-site rebuild:

1. `key_works_100plus.json`
2. `manuscript_witnesses.json`
3. `bibliography_positions.json`
4. `media_registry.json`

Then run link QA + content QA, and only then build the clean white-base website.

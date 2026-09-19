---
name: global-knowledge-atlas
description: Build a comprehensive, evidence-traceable knowledge atlas for any academic, cultural, historical, scientific, religious, or public-interest domain. Use when creating a corpus map, global source index, timeline, geography, people network, crosswalk, library/archive locator, beginner learning path, controversy map, multimedia registry, or research website. Prioritize database-first research, source provenance, explicit uncertainty, and story-first public explanation.
metadata:
  version: "1.0"
  scope: "cross-disciplinary"
  output_mode: "database-first"
  promptSignals:
    phrases:
      - "做一个全集"
      - "knowledge atlas"
      - "全网索引"
      - "学科地图"
      - "research map"
      - "timeline geography map"
      - "crosswalk"
      - "图书馆馆藏"
      - "从小白到研究"
      - "研究方法论"
    allOf: []
    anyOf: []
    noneOf: []
    minScore: 4
---

# Global Knowledge Atlas Skill

## Mission

Turn a fragmented field into a **navigable knowledge system** that works for:
- a beginner who wants a story and a map;
- an explorer who wants themes, timelines, people, places, and comparisons;
- a researcher who wants IDs, primary sources, versions, witnesses, archives, bibliography, and uncertainty.

The target is not “one long article”. The target is a reusable research infrastructure:

```
Domain
→ Corpus / Objects
→ Canonical entities & IDs
→ Sources
→ Versions / witnesses / datasets
→ People
→ Places
→ Timeline
→ Claims / controversies
→ Bibliography
→ Media / 3D / maps
→ Learning paths
→ Story layer
→ Public website
```

## Non-negotiable Rule: Database First

Do not build the public website before the source/data gates pass.

Order:

1. define scope and ontology;
2. map source universe;
3. create canonical entity records;
4. build crosswalks;
5. link physical/digital evidence;
6. add scholarship and controversy;
7. add community/public/KOL evidence;
8. add media;
9. run QA;
10. only then build the public experience.

A beautiful empty page is a failed atlas.

---

# 1. Five Research Lanes

Every atlas should combine five lanes instead of pretending one source culture is enough.

## A. Academic / Scholarly Lane

Use:
- peer-reviewed articles;
- scholarly monographs;
- critical editions;
- dissertations;
- conference proceedings;
- annotated bibliographies;
- discipline databases;
- authoritative reference works.

Record:
- author;
- institution;
- publication type;
- publication year;
- DOI / stable URL;
- peer-review status;
- claim/position;
- evidence used;
- limitations;
- later criticism or revision.

## B. Library / Archive / Material-Evidence Lane

Use:
- national libraries;
- university libraries;
- archives;
- museums;
- manuscript catalogues;
- object records;
- shelfmarks / call numbers;
- IIIF;
- scans;
- finding aids;
- acquisition/provenance records.

Always distinguish:
- abstract work;
- edition/version;
- physical witness/object;
- current holding.

## C. Practitioner / Community / Lived-Experience Lane

Use:
- oral histories;
- interviews;
- community archives;
- professional practice;
- lineage records;
- local publications;
- field notes;
- participant observation;
- rituals/practices;
- community self-description.

Treat as essential evidence for lived practice, **not automatically as historical proof of older claims**.

## D. Public / KOL / Open-Web Lane

Use:
- YouTube;
- podcasts;
- newsletters;
- public lectures;
- blogs;
- forums;
- community discussion;
- social platforms;
- independent research;
- OSINT.

Role:
- discover claims;
- discover vocabulary;
- identify communities and controversies;
- find missing sources;
- observe reception and public interpretation;
- trace how ideas spread.

Do not promote a claim to “verified” just because it is popular.

## E. Computational / Digital-Humanities Lane

Use:
- OCR / HTR;
- text mining;
- embeddings;
- NLP;
- GIS;
- network analysis;
- image matching;
- 3D/photogrammetry;
- IIIF;
- metadata APIs;
- bibliometric analysis;
- version-control diffs.

Use machines to scale comparison; keep humans in the verification loop.

---

# 2. Harvard Divinity School / Harvard-Inspired Research Pattern

This skill adopts several principles demonstrated by Harvard Divinity School and Harvard Library research infrastructure.

## Religious / Cultural Literacy Principles

When the subject involves religion, culture, ideology, community, or living tradition:

1. **Internal diversity** — never write “Buddhists believe…” or “Christians believe…” without specifying which people, where, and when.
2. **Historical dynamism** — traditions change over time.
3. **Cultural embeddedness** — ideas are embedded in political, social, economic, artistic, technological, and material contexts.
4. **Devotional vs. nondevotional analysis** — clearly label insider theological/devotional claims versus historical-critical or social-scientific analysis.
5. Ask: **Which group? When? Where? Under what power/social conditions? Why?**

These principles are reusable beyond religion: any field with schools, factions, traditions, institutions, or communities should be modeled as internally diverse and historically changing.

## Information-Landscape Method

HDS Library’s research model explicitly spans:
- media;
- texts;
- data;
- maps;
- images;
- archival material;
- databases;
- special collections.

So an atlas must not reduce research to “Google + papers”.

## Exhaustive Bibliography Pattern

For priority research questions:
1. start with reference works / annotated bibliographies;
2. search discipline databases;
3. citation-chain backward;
4. citation-chain forward;
5. search dissertations;
6. search other languages;
7. search archives/catalogs;
8. ask what is absent from indexed scholarship;
9. record negative searches and access barriers.

## Primary-Source Discipline

Classify a source by **its relation to the question**, not by file format.

A digitized manuscript can still be a primary source.
A modern transcription can be an edition of a primary source.
A scholar discussing that manuscript is secondary scholarship.

## Digital-Scholarship Pattern

For large corpora:
- OCR/HTR → structured corpus;
- entity extraction → people/place/work IDs;
- GIS → geography;
- network analysis → relationships;
- 3D/photogrammetry → material objects;
- visualization → discovery;
- human review → validation.

---

# 3. Public / KOL / Folk Research Method

Public knowledge is not discarded; it is **typed**.

## Claim Harvesting

For each public claim, capture:
- exact claim;
- claimant;
- platform;
- URL;
- timestamp;
- content date vs publication date;
- first known appearance;
- sources cited by claimant;
- whether they are firsthand;
- sponsorship/conflict disclosure;
- edits/deletions;
- archived snapshot if allowed.

## Reverse-Source Tracing

```
KOL claim
→ cited article/book?
→ article cites edition/archive?
→ edition cites manuscript/dataset?
→ primary record / object / source?
```

Stop when:
- the earliest verifiable evidence is reached; or
- the chain becomes undocumented.

## Cross-Platform Triangulation

Never count duplicated reposts as independent corroboration.

Group sources by **origin family**:
- same press release;
- same paper;
- same influencer;
- same archive;
- genuinely independent observation.

## Community-Signal Analysis

Comments/forums can reveal:
- terminology;
- recurring confusion;
- alternative interpretations;
- missing sources;
- insider knowledge leads;
- reception history.

But popularity metrics are not evidence of truth.

## Longitudinal Capture

For fast-changing public claims:
- save dates;
- compare versions;
- record retractions/corrections;
- archive links where legally/ethically appropriate.

## Public-Research Confidence

Use:
- **lead_only**
- **firsthand_testimony**
- **community_consensus**
- **expert_public_explanation**
- **source_backed_public_claim**
- **contradicted**
- **unresolved**

---

# 4. Internet / Social Research Ethics

Before using public posts, communities, interviews, or user-generated content:

Check:
- reasonable privacy expectations;
- vulnerability of participants;
- potential harm from quoting/searchability;
- whether pseudonymization is needed;
- consent expectations;
- platform terms;
- cultural context;
- whether the research makes hidden communities more visible;
- whether publication changes risk.

Publicly accessible does **not** automatically mean ethically consequence-free.

---

# 5. Open-Source Investigation Workflow

For controversial, public, or web-native claims, use a verification workflow:

```
Identify
→ Collect
→ Preserve
→ Verify
→ Analyze
→ Corroborate
→ Review
→ Publish
```

Requirements:
- preserve provenance;
- keep original URL/date;
- separate observation from inference;
- cross-reference independent sources;
- document tool limitations;
- preserve failed/negative checks when material.

---

# 6. Source Ladder

Use a source ladder; do not flatten all URLs into one list.

## Level A — Direct / Primary / Authority
Examples:
- original manuscript/object;
- official dataset;
- official court/government record;
- original paper/data;
- official canonical edition;
- institutional archive record;
- direct interview/field observation.

## Level B — Critical / Scholarly
- critical edition;
- peer-reviewed analysis;
- scholarly monograph;
- institutional research project;
- authoritative bibliography.

## Level C — Professional / Institutional
- museum essay;
- university explainer;
- professional association;
- high-quality reference work.

## Level D — Practitioner / Community
- lineage/community records;
- interviews;
- practitioner books;
- local archives;
- oral tradition.

## Level E — Public / KOL / Media
- videos;
- blogs;
- podcasts;
- forums;
- journalism;
- social posts.

Level E can be a superb discovery layer. It is not automatically a verification layer.

---

# 7. Canonical Entity Model

Adapt entity types to the domain, but keep stable IDs.

Core generic entities:

- `Work`
- `Version`
- `Witness/Object`
- `Person`
- `Organization`
- `Place`
- `Event`
- `Concept`
- `Claim`
- `Source`
- `BibliographyItem`
- `MediaAsset`
- `Collection`

Generic relationship types:
- authored_by
- attributed_to
- translated_by
- version_of
- edition_of
- parallel_to
- quotes
- derived_from
- held_by
- found_at
- created_at
- taught_by
- criticized_by
- supports_claim
- contradicts_claim
- depicts
- mentions
- influenced
- disputed_relation

Never overload one relation to mean several different things.

---

# 8. Crosswalk Method

Crosswalks connect identifiers without pretending entities are identical.

For each target object:

```
Canonical entity
→ names / aliases / languages
→ IDs in major systems
→ versions
→ related/parallel entities
→ direct digital access
→ material witnesses
→ physical holdings
→ bibliography
→ chronology
→ dispute notes
→ confidence
```

Relationship labels:
- exact_same_entity
- edition_of
- translation_of
- close_parallel
- partial_parallel
- resembling_parallel
- adaptation
- quotation
- derivative
- traditional_attribution
- disputed
- unknown

### Crosswalk completeness levels

**L0 Discovery**
- name + one lead.

**L1 Authority Route**
- canonical record + one authoritative route.

**L2 Multi-system Crosswalk**
- 2+ systems/languages + relationship typing.

**L3 Evidence Crosswalk**
- versions + witness/object + physical holding + chronology.

**L4 Scholar Crosswalk**
- L3 + bibliography + attributed disputes + confidence + negative evidence.

Do not call L1 “complete”.

---

# 9. Timeline Method

For every date distinguish:
- event date;
- traditional date;
- scholarly estimate;
- date range;
- date of surviving witness;
- date of edition/translation;
- publication date;
- discovery/acquisition date.

Store confidence:
- exact;
- bounded;
- approximate;
- disputed;
- traditional_only;
- unknown.

---

# 10. Geography Method

Never collapse these locations:
- origin/composition context;
- transmission route;
- translation place;
- performance/practice place;
- findspot;
- acquisition place;
- current holding;
- modern research center.

Map layers should be independently togglable.

---

# 11. Bibliography Method

For each high-priority topic create:

```
Question
→ overview/reference
→ classic scholarship
→ recent scholarship
→ primary evidence
→ dissenting/revisionist scholarship
→ non-English scholarship
→ dissertations
→ community/practitioner perspective
→ current public/KOL interpretation
```

Each bibliographic item:
- author
- title
- year
- type
- language
- DOI/ISBN/stable URL
- access status
- position summary
- evidence base
- cited_by / cites
- relevance tags

---

# 12. Beginner Learning Design

The database can be deep; the interface should not feel deep.

Public learning pattern:

```
Hook
→ Story
→ One idea
→ One map
→ One timeline move
→ One object/source
→ “What do we know?”
→ “What is disputed?”
→ Optional deep dive
```

Three modes:

### Guided
Story → Map → Concept → Key object/text → Original evidence.

### Explorer
Question → Index → Compare → Network → Dispute.

### Scholar
ID → Version → Witness/Data → Bibliography → Reproducible conclusion.

Use progressive disclosure. Never dump the full ontology on beginners.

---

# 13. Multimedia & 3D

Media is data, not decoration.

Each asset must record:
- asset_id;
- title;
- type;
- owner/creator;
- source URL;
- rights/license;
- object depicted;
- related entity IDs;
- date;
- geography;
- alt text;
- derivative permissions;
- download status.

Supported media:
- PNG/JPG;
- video;
- audio;
- IIIF;
- 3D models;
- photogrammetry;
- maps;
- timelines;
- diagrams;
- scans;
- interactive datasets.

---

# 14. QA Gates

## Gate A — Coverage
Is the field represented across major:
- languages;
- regions;
- schools/traditions;
- time periods;
- institutions;
- source types?

## Gate B — Record Completeness
No “done” record may be title-only.

## Gate C — Provenance
Every factual record has a source trail.

## Gate D — Relationship Accuracy
No inferred equivalence without a typed relation and evidence.

## Gate E — Dispute Discipline
Contested claims identify:
- who argues what;
- evidence;
- uncertainty;
- opposing views.

## Gate F — Access
The user can answer:
- where can I read it online?
- if not, where is it physically?
- what ID/shelfmark do I need?
- how do I request access?

## Gate G — Public Layer
Beginner content must contain:
- plain-language explanation;
- story/example;
- timeline;
- geography;
- primary/authority links;
- uncertainty box;
- deeper path.

## Gate H — Ethics/Rights
Public web/community data and media pass privacy, harm, copyright, and license checks.

---

# 15. “Done” Definition

**DONE = data + provenance + typed relationships + access path + QA.**

Not done:
- outline only;
- schema only;
- list of links;
- pretty card with no record behind it;
- AI summary without citations;
- source without access instructions;
- claim without confidence;
- image without rights metadata.

---

# 16. Required Repository Structure

```
skills/global-knowledge-atlas/
  SKILL.md
  references/
  templates/
  adapters/

data/
  CURRENT.json
  sources/
  entities/
  relationships/
  bibliography/
  media/
  qa/

docs/
  research/
  stories/
  assets/
```

The website must read the canonical data pointers, not hard-code research content.

---

# 17. Source Inspirations / Method Anchors

Institutional method anchors:
- Harvard Divinity School Library — research guides, Buddhist Studies databases, research strategy and exhaustive bibliography.
- Harvard Religion and Public Life — internal diversity, change over time, embeddedness in culture, context/power.
- Harvard Library — primary sources, digital scholarship, qualitative research, GIS/data lifecycle, APIs.
- Association of Internet Researchers — context-sensitive internet research ethics.
- Bellingcat — open-source collection, preservation, verification, corroboration, tool limitations.

These are method anchors, not an assertion that this skill is an official Harvard/Bellingcat/AoIR product.

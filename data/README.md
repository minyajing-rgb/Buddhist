# Dharma Atlas Data Layer

## Current database version: v0.3

**Do not guess which file is current.**  
The only source of truth for the future site is:

`data/CURRENT.json`

It maps each product layer to the canonical dataset.

## Architecture

```
Corpus / Canon Entry Points
        ↓
      Works
        ↓
     Versions
        ↓
Physical Witnesses
        ↓
Online Source / Physical Holding
        ↓
Bibliography / Research Positions
```

Cross-cutting layers:

```
People · Places · Concepts · Media · Learning Paths · Search Strategies
```

## Current product philosophy

The database is designed to support two very different experiences from one source of truth:

### Beginner layer
Story → visual explanation → timeline → map → concept → key text.

### Research layer
Work → ID → version → witness → source → bibliography → confidence.

The public website should **not** duplicate or hard-code its own content.

## Historical snapshots

Files with older versions remain for traceability, but should not be used by the future site unless explicitly comparing database history.

See `CURRENT.json` for the authoritative list.

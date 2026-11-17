# RBXMeta Wiki

## Build

```bash
python builder.py
```

The static site is generated into `dist/`.

## Canonical data sources

- `data/entities.json` is the canonical unit dataset used by the unit database, Tier List, Team Builder, Unit Comparison, and editorial unit lists.
- `data/codes.json` is the canonical code dataset. `status` controls whether a code is currently reported active; `verification` distinguishes cross-source-confirmed entries from unverified reports. An unverified code must not be presented as confirmed.
- `data/guides.json` contains guide content and update dates.
- `config.json` contains site configuration and FAQ content.

The former `data/tierlist.json` duplicated unit identity, rarity, and placement data and is no longer used. Tier List output is derived from `data/entities.json` to avoid data drift.

## Verification notes

Cross-source confirmation is not equivalent to an in-game redemption test. Numerical game data and drop rates should be labelled with their actual source and verification method. The Team Builder currently checks placement coverage only; it does not claim to calculate combat strength or mode readiness.

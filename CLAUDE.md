# Gnosis AI — Project Context

**Read `docs/PRODUCT_PLAN.md` first.** That is the canonical document for what Gnosis AI is and how to build it.

For background context on the research papers and methodology, see `docs/HANDOVER.md`.

## Quick Summary

Gnosis AI is the world's first autonomous knowledge discovery system. It uses Convergent Descent — the methodology from the 15 Infinitography research papers — to scan across all fields of science, find structural convergences, and generate genuine new knowledge.

**Three modes:**
- **Guided** — question + domains → findings
- **Exploration** — domains only → convergences
- **Auto** — all fields → systematic discovery (the real vision)

**Two AI fields implemented:**
- **CI (Convergence Intelligence)** — runs Convergent Descent at scale
- **EA (Epistemic Assurance)** — validates everything CI produces

**Architecture:** Custom CI/EA orchestration layer on top of Claude API. We orchestrate, the frontier model thinks.

## Key Documents

| Document | What It Is |
|----------|-----------|
| `docs/PRODUCT_PLAN.md` | **THE canonical doc.** Vision, modes, architecture, data model, CI/EA engines, field taxonomy, CLI, implementation phases, validation, demo plan, tech spec. Read this first. |
| `docs/HANDOVER.md` | Background context — the research papers, the methodology, the three AI fields, connection to the website |
| `papers/markdown/` | All 15 papers as markdown (readable) |
| `papers/pdf/` | All 15 papers as PDF (original from Zenodo) |

## Build Order

```
Phase 1: Foundation     → Project structure, taxonomy, Knowledge Store, API layer
Phase 2: CI Engine      → Surveyor, Extractor, Convergence Detector, Meta-Convergence
Phase 3: EA Engine      → Strength, Independence, Adversarial, Reproducibility, Consistency
Phase 4: Three Modes    → Guided, Exploration, Auto + Orchestrator + Self-Amplifying Loop
Phase 5: Reports        → Markdown, JSON, website export, CLI polish
Phase 6: Demo Run       → Full auto across 52 fields → curated discovery report
```

## Rules

- Architecture sits above frontier models (Claude API). Novel contribution = the CI/EA layer.
- Open source
- v1 with honest scope — acknowledge limitations
- Validate against the papers first (reproduce their findings), then run on novel domains
- GitHub: always `wonderben-code`
- Collaboration style: fun, optimistic, direct
- Don't pause between phases — keep going

## Tech Stack

- Python 3.11+
- Claude API (Sonnet for speed, Opus for depth)
- JSON + SQLite storage
- Click CLI framework
- Dependencies: anthropic, click, rich

## Creator

Mark E. Mala (Ekram Alam) — serial founder, YC alum, Forbes Technology Council.

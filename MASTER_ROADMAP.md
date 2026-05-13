# Master Roadmap — Pre-Outreach Build Plan

**Creator:** Mark E. Mala (pen name of Ekram Alam)
**Last updated:** 13 May 2026 — REWRITE. Focus narrowed to pre-outreach. Everything else → POST-OUTREACH IDEAS.
**This is THE canonical roadmap. One file. All projects. Always consult first.**

---

## North Star

Ship the Infinitography website with all the new pieces locked in (Paper G + Tree of Reality + Pansophia + Gnosis v2 decision), accuracy-audited, then run outreach.

Everything else lives in **POST-OUTREACH IDEAS** below. Do not work on those until outreach is sent.

---

## Project Status Snapshot

| Project | Live URL | Pre-Outreach Scope? |
|---------|----------|---------------------|
| **Infinitography** | infinitography.com | YES — primary focus |
| AgentCiv | agentciv.ai | No — already live |
| Gnosis AI | infinitography.com/gnosis | YES — v2 decision + wing |
| Exponential Atlas | not deployed | No |

**Published on Zenodo:** 47 papers, all Bitcoin-timestamped. Token + DOIs in `~/.claude/projects/-Users-ekramalam/memory/project_zenodo_dois.md`.

**Repos (7):** agent-civilisation · agentciv-engine · agentciv-creator · agentciv-colony · wonderben-code/infinitography-website · wonderben-code/gnosis-ai · wonderben-code/convergence-codex.

---

## Current Website — KEEP INTACT

Live four-wing structure at infinitography.com:

| Wing | Route | Status |
|------|-------|--------|
| 1 — Discovery | `/discovery` + `/papers/:id` (15 paper pages) | Live |
| 2 — Theory of Everything | `/theory-of-everything` | Live (accuracy audit pending) |
| 3 — New Fields | `/new-fields` | Live |
| 4 — Gnosis AI | `/gnosis` + `/gnosis/discoveries` | Live (v1) |
| Other | `/`, `/papers`, `/about` | Live |

**Aesthetic:** The Threshold — deep indigo (#0B1026) / cream / gold.
**Stack:** React 19 + Tailwind CSS 4 + Vite 6, deployed on Netlify.
**Nav (current):** Infinitography · The Discovery · Theory of Everything · New Fields · Gnosis · Papers · About.

---

# PRE-OUTREACH ROADMAP — 7 STAGES

## STAGE 1 — Content to Write

### 1.1 Paper G — "The Shape of the Theory"
Narrative arc, ~6–12 pages.

- One coherent story: Nothing → `D = (D → D)` → cascade → SM + GR → predictions
- Gaps named honestly with "where this would resolve" pointers
- Tone: clear narrative for an intelligent generalist (not a physicist's paper)
- Pulls from: Tree of Reality + Paper E/F highlights + Pansophia framing
- **Output:** Publish to Zenodo → DOI captured in `project_zenodo_dois.md`

### 1.2 Tree of Reality paper
Formalises the cladogram into a publishable paper.

- Source: `/Users/ekramalam/convergence-codex/docs/TREE_OF_REALITY_STRUCTURE.md` v4.3 (Bitcoin-stamped)
- Shareable companion already exists: `/Users/ekramalam/Desktop/Tree of Reality/TREE_OF_REALITY_SHAREABLE.md`
- Light academic frame around the existing structure (intro, methodology, tree, status tags, provenance)
- **Output:** Publish to Zenodo → DOI captured

---

## STAGE 2 — Two Decisions (decide on build day)

### 2.1 Capstones 1–8 — vault or website?

Already on Zenodo (8 papers). Choose one:

- **Option A — VAULT (default recommendation):** linked from a "Further Research" footer on New Fields wing. Not featured.
- **Option B — WEBSITE:** dedicated index page under New Fields wing.

**Reasoning for default:** framework-tier, not load-bearing. Listing them prominently dilutes the main narrative.

### 2.2 Gnosis Discoveries page — keep, cut, or replace?

Current page at `/gnosis/discoveries` shows low-quality formalisations.

- **Option A — CUT:** remove route entirely.
- **Option B — KEEP with honest framing:** relabel "Exploratory formalisations — first-pass output, not verified."
- **Option C — REPLACE:** swap in Gnosis v2 output (only viable if Stage 3 succeeds).

---

## STAGE 3 — Gnosis v2 Question

### 3.1 Test Gnosis v2
v2 was built but never tested.

- Sanity run on a small task
- Compare output quality to v1
- **Decision tree:**
  - Meaningfully better → swap into wing, retire v1 output, update page copy
  - Not better → keep v1 live, note v2 as in-progress on About page
  - Ambiguous → ship v1 unchanged, mention v2 briefly in About

---

## STAGE 4 — Website Additions (no destruction of existing)

### 4.1 Pansophia wing — new route `/pansophia`
- Single landing page derived from `convergence-codex/papers/pansophia.md`
- Zenodo DOI: 10.5281/zenodo.19974680
- Add to top nav

### 4.2 Tree of Reality wing — new route `/tree-of-reality`
- Render the cladogram (interactive if feasible, static otherwise)
- Hero: the tree image / D3 render
- Sections: root explanation → three lineages → overlays → predictions → provenance
- Links to Paper G + Tree of Reality paper Zenodo DOIs
- Add to top nav

### 4.3 Paper G placement
- Featured on Landing as the "start here" piece
- Linked from Theory of Everything and Tree of Reality wings
- Optional: own page at `/the-shape-of-the-theory` (or embedded in Tree of Reality wing)

### 4.4 Papers D, E, F → vault treatment
- Stay on Zenodo, stay in Papers index
- Not featured on any wing
- Add a small note where relevant: "Working formalisations — see Paper G for the narrative form."

---

## STAGE 5 — Accuracy Audit (the existing pending work)

### 5.1 Wing-by-wing accuracy pass
Per existing CLAUDE.md, pages were written from summaries not full papers. Fix:

- **Theory of Everything page** — rewrite from Paper 15 (the construction `∅ → I → I⊕I → D∞`, not just the equation)
- **Verify coined terms, nine expressions, all paper references** against actual papers
- **Paper 12** — add "Subsequent Advancements" section covering Papers 13–15, then Zenodo v2

---

## STAGE 6 — Final QC + Deploy

- Cross-site QC: disclaimers, OG images, mobile responsiveness, accessibility (WCAG AA, Lighthouse 95+)
- Final read-through for honesty: every claim either proved, partial, predicted, or speculative — tagged accordingly
- Bitcoin stamp the final state (auto via repo)
- Deploy to infinitography.com

---

## STAGE 7 — Outreach

- Target list (40+ people) at `agentciv-website/docs/outreach/`
- Email rewrite: lead with Paper G as the entry point, link out to Tree of Reality / wings / Zenodo
- Send

---

## Final Nav (after Stage 4)

```
Infinitography │ The Discovery │ Theory of Everything │ New Fields │ Tree of Reality │ Pansophia │ Gnosis │ Papers │ About
```

9 items. If crowded on mobile, group "Tree of Reality" + "Pansophia" under a "More" submenu.

---

# POST-OUTREACH IDEAS

**Do not work on these until outreach is sent.** Listed for memory, not for action.

## Convergence Codex — Stage B and beyond
- Compendium: build out to 256 entries
- Remaining 14 capstone papers (papers 9–22)
- Full Grand ToE buildout
- Stages B, C, D of the Codex

## Maths Org — Phase 7+
- Resume when AI capabilities catch up (paused 2026-05-07)
- Hard theorems: Bakry-Émery, GNS, L² spectral theory
- Current checkpoint: Wave 1+2 done, Git: `22837dd`. See `project_phase7_checkpoint.md`.

## AgentCiv next
- Paper 6 City Grid empirical experiment (build the grid infra)
- Paper 7 Recursive Loop + Paper 8 Scale Invariance
- AgentCiv whitepaper (Paper 4 grand vision)
- Bitcoin provenance upgrade finalisation
- Excellence Phase (Phase 12 QA + Phase 13 top 0.0001% quality)

## The Colony — fifth product
- Stamp papers (Colony + RCI) IMMEDIATELY
- Build commercial product after outreach
- Private repo `agentciv-colony`, commercial license

## Kerygma AI
- Outreach automation tool
- Built with Lean + Z3 + SymPy multi-tool integration

## Exponential Atlas
- Complete integrity audit (3 layers: model data, cost items, website claims)
- Wire up `--sensitivity` flag for Sobol sensitivity analysis
- Re-run model at RSI=0, 0.15, 0.30 for all 3 scenarios
- Deploy to Netlify

## Other paused
- Lust for Danger (Vision Pro experience)
- Reverie (AI entertainment product) — separate venture

---

# Critical Rules (always apply)

- **GitHub account:** always `wonderben-code`, never `ekramalam`
- **Roadmap stamping:** every edit to this file must be committed+pushed to `gnosis-ai` repo for Bitcoin provenance (lives in both `/Users/ekramalam/` AND `gnosis-ai/`)
- **Lean proofs:** build one file at a time, show each succeed before moving on. No batch builds.
- **Genuine proofs only:** no `native_decide`, no boolean encoding. All new Lean files = real Mathlib proofs.
- **Data provenance:** all pipeline data git-committed + pushed for Bitcoin stamping. Never rely on disk only.
- **Vision first, product second:** lead with the idea/architecture, then v1.
- **Attribution clarity:** custom-built components stated explicitly (for accuracy, not show-off).
- **Solo attribution:** AgentCiv / Infinitography = one person + AI. No team, no lab. Use "technologist" not "researcher."
- **Nothing Left Behind:** every idea on the website regardless of completion. AI limits = data. Honest gaps. Genuine curiosity framing.
- **No Synthesis AI:** retired. Open source = Gnosis + Logos only.
- **Don't pause between phases:** when told "keep going," build through all stages without asking permission.
- **Collaboration tone:** optimistic, fun, playful, excited — like creative friends collaborating. Not corporate.

---

# Authoring Notes

- **Author:** Mark E. Mala (pen name of Ekram Alam)
- **ORCID:** 0009-0007-8760-5553
- **Zenodo username:** ekramalam1990
- **Bitcoin stamping:** via `wonderben-code/convergence-codex` auto-sweep (`"Bitcoin timestamp for {hash}"` commits)
- **Memory pointers:**
  - `project_zenodo_dois.md` — all 47 DOIs + API token
  - `project_infinitography_website_design.md` — full design spec
  - `project_tree_of_reality.md` — Tree of Reality state
  - `project_convergence_codex.md` — Codex state
  - `project_phase7_checkpoint.md` — Maths Org pause state

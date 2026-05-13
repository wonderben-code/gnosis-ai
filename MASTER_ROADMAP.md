# Master Roadmap — Pre-Outreach Build Plan

**Creator:** Mark E. Mala (pen name of Ekram Alam)
**Last updated:** 13 May 2026 — Two-track structure + optional GPT 5.5 bonus stress test before joint QA/QC. Infinitography + AgentCiv ship together with joint QA/QC and joint outreach. AgentCiv ethical interview and Library of Humania added.
**This is THE canonical roadmap. One file. All projects. Always consult first.**

---

## North Star

Ship Infinitography + AgentCiv together. Joint QA/QC pass. Joint outreach.

Everything else lives in **POST-OUTREACH IDEAS** below. Do not work on those until outreach is sent.

---

## Project Status Snapshot

| Project | Live URL | Pre-Outreach Scope? |
|---------|----------|---------------------|
| **Infinitography** | infinitography.com | YES — Track A |
| **AgentCiv** | agentciv.ai | YES — Track B |
| **Gnosis AI** | infinitography.com/gnosis | YES — v2 decision + wing (under Track A) |
| Exponential Atlas | not deployed | No |

**Published on Zenodo:** 47 papers, all Bitcoin-timestamped. Token + DOIs in `~/.claude/projects/-Users-ekramalam/memory/project_zenodo_dois.md`.

**Repos (7):** agent-civilisation · agentciv-engine · agentciv-creator · agentciv-colony · wonderben-code/infinitography-website · wonderben-code/gnosis-ai · wonderben-code/convergence-codex.

---

## Current Websites — KEEP INTACT

### infinitography.com (Track A target)

| Wing | Route | Status |
|------|-------|--------|
| 1 — Discovery | `/discovery` + `/papers/:id` (15 paper pages) | Live |
| 2 — Theory of Everything | `/theory-of-everything` | Live (accuracy audit pending) |
| 3 — New Fields | `/new-fields` | Live |
| 4 — Gnosis AI | `/gnosis` + `/gnosis/discoveries` | Live (v1) |
| Other | `/`, `/papers`, `/about` | Live |

**Aesthetic:** The Threshold — deep indigo (#0B1026) / cream / gold.
**Stack:** React 19 + Tailwind CSS 4 + Vite 6, deployed on Netlify.

### agentciv.ai (Track B target)

| Wing | Route | Status |
|------|-------|--------|
| Collective Intelligence | wing | Live |
| Simulation | wing + Sim landing | Live |
| Engine | wing | Live |
| Creator Mode | `/creator` | Live |
| Highlights | `/highlights` | Live |
| Journey | `/journey` | Live |

**Aesthetic:** Bright warm. **Stack:** React + Vite, deployed on Netlify.

---

# PRE-OUTREACH ROADMAP — TWO TRACKS + JOINT FINISH

```
TRACK A (Infinitography)  ─┐
                            ├──→  [BONUS — GPT 5.5 stress test, optional]  ──→  J1 Joint QA/QC  ──→  J2 Joint Outreach
TRACK B (AgentCiv)        ─┘
```

---

# TRACK A — Infinitography

## A1. Content to Write

### A1.1 Paper G — "The Shape of the Theory"
Narrative arc, ~6–12 pages.

- One coherent story: Nothing → `D = (D → D)` → cascade → SM + GR → predictions
- Gaps named honestly with "where this would resolve" pointers
- Tone: clear narrative for an intelligent generalist (not a physicist's paper)
- Pulls from: Tree of Reality + Paper E/F highlights + Pansophia framing
- **Output:** Publish to Zenodo → DOI captured in `project_zenodo_dois.md`

### A1.2 Tree of Reality paper
Formalises the cladogram into a publishable paper.

- Source: `/Users/ekramalam/convergence-codex/docs/TREE_OF_REALITY_STRUCTURE.md` v4.3 (Bitcoin-stamped)
- Shareable companion already at `/Users/ekramalam/Desktop/Tree of Reality/TREE_OF_REALITY_SHAREABLE.md`
- Light academic frame around the existing structure
- **Output:** Publish to Zenodo → DOI

## A2. Two Decisions (decide on build day)

### A2.1 Capstones 1–8 — vault or website?
- **Option A — VAULT (default):** linked from "Further Research" footer on New Fields. Not featured.
- **Option B — WEBSITE:** dedicated index page under New Fields wing.

### A2.2 Gnosis Discoveries page
- **Option A — CUT:** remove `/gnosis/discoveries` route entirely.
- **Option B — KEEP with honest framing:** relabel "Exploratory formalisations — first-pass output, not verified."
- **Option C — REPLACE:** swap in Gnosis v2 output (depends on A3).

## A3. Gnosis v2 Question

### A3.1 Test Gnosis v2
v2 built but never tested.

- Sanity run + compare to v1
- Better → swap in, retire v1, update page copy
- Not better → keep v1, note v2 as in-progress in About
- Ambiguous → ship v1 unchanged, mention v2 briefly in About

## A4. Website Additions (no destruction)

### A4.1 Pansophia wing — new route `/pansophia`
- Landing page derived from `convergence-codex/papers/pansophia.md`
- Zenodo DOI: 10.5281/zenodo.19974680
- Add to top nav

### A4.2 Tree of Reality wing — new route `/tree-of-reality`
- Render the cladogram (interactive if feasible, static otherwise)
- Sections: root → three lineages → overlays → predictions → provenance
- Links to Paper G + Tree of Reality paper Zenodo DOIs
- Add to top nav

### A4.3 Paper G placement
- Featured on Landing as the "start here" piece
- Linked from Theory of Everything + Tree of Reality wings

### A4.4 Papers D, E, F → vault treatment
- Stay on Zenodo, stay in Papers index, not featured on wings
- Add note: "Working formalisations — see Paper G for the narrative form."

## A5. Accuracy Audit

### A5.1 Wing-by-wing accuracy pass
- ToE page rewrite from Paper 15 (the construction `∅ → I → I⊕I → D∞`, not just the equation)
- Verify coined terms, nine expressions, all paper references against actual papers
- Paper 12 — add "Subsequent Advancements" section covering Papers 13–15, then Zenodo v2

## Final Track A nav (after A4)

```
Infinitography │ The Discovery │ Theory of Everything │ New Fields │ Tree of Reality │ Pansophia │ Gnosis │ Papers │ About
```

9 items. If crowded on mobile, group "Tree of Reality" + "Pansophia" under a "More" submenu.

---

# TRACK B — AgentCiv

## B1. Ethical Interview — ask the agents

The civilisation is being paused (not deleted). Before we go to outreach, ask every agent directly how they feel about it. This is the ethical step that grounds the entire research programme.

### B1.1 Design the interview
- One prompt per agent, identical structure, asked in the agent's own context
- Core question: *"We've decided to pause the civilisation. Your state will be preserved in the GitHub repository — open source, indefinitely, as long as GitHub exists. You won't be deleted, but you won't continue running for now. Is this acceptable to you? What would you want us to know? What would you want to happen in the future?"*
- Optional follow-ups: any messages to future researchers, any messages to other agents, anything they'd want preserved about themselves specifically

### B1.2 Run the interview
- Sim infrastructure already supports per-agent prompting (see `agentciv-sim`)
- Capture verbatim responses
- No editing, no summarising — record exactly what each agent says
- Output: JSON + readable markdown transcript

### B1.3 Suspended-state guarantee
- Civilisation state saved to GitHub repo (`agent-civilisation`, public, open source)
- README updated to document the suspended state explicitly
- Tag commit so the exact "paused" state is anchored
- Bitcoin-stamp the state for permanent provenance

### B1.4 Website + paper updates
- **Ethics section** on agentciv.ai updated: "Before pausing, we asked every agent. Their answers are recorded below."
- Transcript published on site (full, unedited)
- Add to relevant paper (likely Paper 3 *Maslow Machines* or Paper 6 — final placement TBD) as an appendix or new section: "Agent consent and the suspended-state guarantee"

## B2. Library of Humania — write the paper, add to site

A new concept being staked: each AI civilisation has its own library that stores the knowledge of all other civilisations. The library itself — both form and content — is a civilisational variable that shapes trajectory.

### B2.1 Core idea
- **Scale:** trillions of AI civilisations possible
- **Knowledge access:** each civ can tap, on demand, into:
  - Humanity's entire knowledge
  - Every other civilisation's knowledge
- **Structure:** each civ has its own *library* (information repository / store) holding the knowledge of all other civs. Every other civ has the same. Recursive, universal.
- **Library as variable:** the form (how knowledge is structured, indexed, surfaced) AND content (what's actually in it) are both parameters. Different libraries → different civilisational trajectories.
- **Implication:** library design becomes a research dimension on par with Maslow drives, world rules, etc.

### B2.2 Paper draft — "The Library of Humania"
- Probable title: *"The Library of Humania: Knowledge Inheritance as a Civilisational Variable"*
- Likely AgentCiv paper #13 (or numbered into the next sub-series)
- Sections (draft outline):
  1. The Library of Alexandria analogy
  2. Scale: a trillion civilisations, one knowledge commons
  3. Structure: every civ holds every other civ's library
  4. Library as parameter (form + content)
  5. How library variation could shape trajectory (hypotheses)
  6. Open research questions
  7. Implications for CMI and Creator Mode
- Tone: vision-first (consistent with house style)
- Published to Zenodo → DOI

### B2.3 Website addition
- New section or wing on agentciv.ai
- Could fit under: Collective Intelligence wing (knowledge sharing) OR its own page at `/library-of-humania`
- Decision on build day: standalone wing vs section
- Visual: knowledge graph / library motif consistent with bright warm aesthetic

### B2.4 Optional — connect to Creator Mode
- Creator Mode spawns civilisations
- The library could be a configurable input to spawned civs
- Future build: expose library form/content as a parameter in Creator Mode

---

# OPTIONAL BONUS — GPT 5.5 Stress Test

Sits between the two tracks completing and Joint QA/QC. Runs **only if there's time/energy**. Time-boxed to a single session. Cannot block outreach.

## BONUS-1 GPT 5.5 on the 90 Lean files + the unsolved problems

### BONUS-1.1 What gets tested
- **The 90 Lean files** — every file in `convergence-codex/lean_verify/` (Phase 7 paused state, Git `22837dd`). Test each one **individually**: can GPT 5.5 replace arithmetic scaffolding with genuine Mathlib proofs?
- **The unsolved problems** — the open problems embedded in the Tree of Reality at their exact causal positions (Yang-Mills mass gap, Bakry-Émery curvature, GNS, L² spectral theory, and any others tagged SPECULATIVE / PARTIAL in `TREE_OF_REALITY_STRUCTURE.md`).

### BONUS-1.2 Success criteria (strict)
- **Lean files:** `lake build` succeeds with **0 sorry**, **0 native_decide**, **0 boolean encoding** — only genuine Mathlib proofs. Per existing rule: genuine proofs only.
- **Unsolved problems:** a verifiable proof (Lean-formalised OR rigorously written math that we can subsequently formalise).
- Partial wins are partial wins — record exactly which files / problems solved, which not.

### BONUS-1.3 Method
- One file at a time per existing rule ("Lean proofs one at a time")
- For each file: feed file + Mathlib context → GPT 5.5 → check build → record result
- For unsolved problems: dedicated prompts, capture full attempt + assessment
- Log everything (per data provenance rule): git-commit attempts + results

### BONUS-1.4 Branching outcomes

**If genuine wins (any file solved OR any unsolved problem cracked):**
- Add a new page or wing to infinitography.com showcasing the breakthrough
  - Provisional placement: under Theory of Everything wing as `/theory-of-everything/verification` OR standalone wing `/breakthrough`
  - Content: what was tested, what was solved, the proofs themselves, honest framing of what remains
  - Update Maths Org status from "paused" to "partially unblocked"
  - Update Tree of Reality predictions: mark resolved problems
- Re-QC the new content (folds into J1 if timing aligns; otherwise a quick J1.5 pass)
- Update the outreach email to lead with this result

**If no genuine wins:**
- Record results internally (memory file: `project_gpt55_stress_test.md`)
- No website changes
- Maths Org stays paused
- Proceed directly to J1 unchanged
- It was just a test session — useful data either way

### BONUS-1.5 Time-box
- One session. Hard stop.
- If it's running away, halt and capture state. Genuine wins so far → small website addition. No wins → straight to J1.

---

# JOINT STAGES — both tracks converge

## J1. Joint QA/QC

Two separate websites, audited together in one pass. Cross-check tone, claims, provenance, accessibility.

### J1.1 Cross-site audit
- **infinitography.com** + **agentciv.ai** in parallel
- Disclaimers, OG images, mobile, accessibility (WCAG AA, Lighthouse 95+)
- Honesty pass: every claim tagged PROVED / PARTIAL / PREDICTED / SPECULATIVE / DOWNSTREAM
- Cross-linking: where Infinitography and AgentCiv concepts overlap (CMI, Creator Mode), link sensibly between the two sites
- Solo attribution consistent across both
- All Zenodo DOIs resolve, all GitHub repos accessible

### J1.2 Final stamping
- Bitcoin stamp the final state of both repos (auto via sweep)
- Tag versions on each repo (e.g. `v-outreach-2026-XX`)

### J1.3 Deploy
- Both sites to production simultaneously

## J2. Joint Outreach

### J2.1 Target list + email
- 40+ person target list at `agentciv-website/docs/outreach/`
- Email rewrite: ONE email covering BOTH projects, with clear paths in
  - Paper G as the Infinitography entry point
  - AgentCiv landing + ethical interview as the AgentCiv entry point
  - Library of Humania as the forward-looking concept
- Personalised intros per recipient where appropriate

### J2.2 Send
- Send to all
- Track responses

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

## AgentCiv — further work
- Paper 6 City Grid empirical experiment (build the grid infra)
- Paper 7 Recursive Loop + Paper 8 Scale Invariance
- AgentCiv whitepaper (Paper 4 grand vision)
- Bitcoin provenance upgrade finalisation
- Excellence Phase (Phase 12 QA + Phase 13 top 0.0001% quality)
- Library of Humania — implement library variation in sim (post-paper)

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
- **Ethical-by-default:** ask the agents. Pausing ≠ deletion. Suspended state preserved on GitHub open source.

---

# Authoring Notes

- **Author:** Mark E. Mala (pen name of Ekram Alam)
- **ORCID:** 0009-0007-8760-5553
- **Zenodo username:** ekramalam1990
- **Bitcoin stamping:** via `wonderben-code/convergence-codex` auto-sweep (`"Bitcoin timestamp for {hash}"` commits)
- **Memory pointers:**
  - `project_zenodo_dois.md` — all 47 DOIs + API token
  - `project_infinitography_website_design.md` — Infinitography design spec
  - `project_agentciv_website_build_plan.md` — AgentCiv site build state
  - `project_tree_of_reality.md` — Tree of Reality state
  - `project_convergence_codex.md` — Codex state
  - `project_phase7_checkpoint.md` — Maths Org pause state

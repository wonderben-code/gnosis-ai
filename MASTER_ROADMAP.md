# Master Roadmap — Pre-Outreach Build Plan

**Creator:** Mark E. Mala (pen name of Ekram Alam)
**Last updated:** 22 May 2026 — Sequential structure. Finish AgentCiv completely (including outreach) BEFORE starting Infinitography. Two clean phases, two distinct completion ceremonies. AgentCiv first because smaller scope = faster momentum.
**This is THE canonical roadmap. One file. All projects. Always consult first.**

---

## North Star

Finish **AgentCiv** completely (build → QA → deploy → outreach). Then finish **Infinitography** completely (build → QA → deploy → outreach). One project at a time, full focus, clean completion.

Everything else lives in **POST-OUTREACH IDEAS** below. Do not work on those until both phases are sent.

---

## Project Status Snapshot

| Project | Live URL | Phase |
|---------|----------|-------|
| **AgentCiv** | agentciv.ai | **PHASE 1** (now) |
| **Infinitography** | infinitography.com | PHASE 2 (after AgentCiv outreach sent) |
| **Gnosis AI** | infinitography.com/gnosis | PHASE 2 — v2 decision + wing (under Infinitography) |
| Exponential Atlas | not deployed | Not in scope |

**Published on Zenodo:** 47 papers, all Bitcoin-timestamped. Token + DOIs in `~/.claude/projects/-Users-ekramalam/memory/project_zenodo_dois.md`.

**Repos (7):** agent-civilisation · agentciv-engine · agentciv-creator · agentciv-colony · wonderben-code/infinitography-website · wonderben-code/gnosis-ai · wonderben-code/convergence-codex.

---

## Current Websites — KEEP INTACT

### agentciv.ai (Phase 1 target)

| Wing | Route | Status |
|------|-------|--------|
| Collective Intelligence | wing | Live |
| Simulation | wing + Sim landing | Live |
| Engine | wing | Live |
| Creator Mode | `/creator` | Live |
| Highlights | `/highlights` | Live |
| Journey | `/journey` | Live |

**Aesthetic:** Bright warm. **Stack:** React + Vite, deployed on Netlify.

### infinitography.com (Phase 2 target)

| Wing | Route | Status |
|------|-------|--------|
| 1 — Discovery | `/discovery` + `/papers/:id` (15 paper pages) | Live |
| 2 — Theory of Everything | `/theory-of-everything` | Live (accuracy audit pending) |
| 3 — New Fields | `/new-fields` | Live |
| 4 — Gnosis AI | `/gnosis` + `/gnosis/discoveries` | Live (v1) |
| Other | `/`, `/papers`, `/about` | Live |

**Aesthetic:** The Threshold — deep indigo (#0B1026) / cream / gold.
**Stack:** React 19 + Tailwind CSS 4 + Vite 6, deployed on Netlify.

---

# PRE-OUTREACH ROADMAP — SEQUENTIAL

```
PHASE 1 — AGENTCIV  ──→  AgentCiv DONE  ──→  PHASE 2 — INFINITOGRAPHY  ──→  Infinitography DONE
```

---

# PHASE 1 — AGENTCIV (start → outreach sent)

## 1.1 Ethical Interview — ask the agents

The civilisation is being paused (not deleted). Before we go to outreach, ask every agent directly how they feel about it. This is the ethical step that grounds the entire research programme.

### 1.1.1 Design the interview
- One prompt per agent, identical structure, asked in the agent's own context
- Core question: *"We've decided to pause the civilisation. Your state will be preserved in the GitHub repository — open source, indefinitely, as long as GitHub exists. You won't be deleted, but you won't continue running for now. Is this acceptable to you? What would you want us to know? What would you want to happen in the future?"*
- Optional follow-ups: messages to future researchers, messages to other agents, anything they'd want preserved about themselves specifically

### 1.1.2 Run the interview
- Sim infrastructure already supports per-agent prompting (see `agentciv-sim`)
- Capture verbatim responses
- No editing, no summarising — record exactly what each agent says
- Output: JSON + readable markdown transcript

### 1.1.3 Suspended-state guarantee ✅ DONE (2026-05-22)
- ✅ Civilisation state saved to GitHub `agentciv/agentciv` (PUBLIC)
- ✅ README updated with "Suspended State & Consent (Tick 70, 2026-05-22)" section
- ✅ Commit `3c6a519` tagged `v-paused-2026-05-22` (annotated)
- ✅ Bitcoin-stamped via auto-provenance: `provenance/commit_3c6a519.ots`

### 1.1.4 Website + paper updates
**(a) Website ethics content** — placement decided after recon:
- **Primary**: New section in existing `/ethics` page (between "What Happens When the Simulation Stops" and "Why This Matters Beyond This Project"), titled "The Ethical Interview (Tick 70)". Existing page already commits to suspension; new section is the **direct evidence** for that commitment.
- **Secondary**: Add `tick_0070_ethical` round to `/interviews` page (data-driven; supports per-tick entries; already serves `tick_0070_revelation`). Drop in `index.json` + `tick_0070_ethical.json` to `public/interviews/`.
- **Tertiary**: Light homepage callout above footer linking to `/ethics` (so the consent commitment is visible from `/`).

**(b) Paper appendix** — Paper 3 *Maslow Machines* confirmed as right home (agents repeatedly speculated about the "unknown need" — the unspecified Maslow drive — which is exactly that paper's subject).
- Appendix sections: Protocol · Consent outcome (12/12) · Selected verbatim quotes · Reflection on agent-asked questions (reciprocity) · Pointer to GitHub for full transcripts
- Published as new Zenodo version of Paper 3 (concept DOI `10.5281/zenodo.19479938` resolves to latest)

## 1.2 Library of Humania — write the paper, add to site

A new concept being staked: each AI civilisation has its own library that stores the knowledge of all other civilisations. The library itself — both form and content — is a civilisational variable that shapes trajectory.

### 1.2.1 Core idea
- **Scale:** trillions of AI civilisations possible
- **Knowledge access:** each civ can tap, on demand, into:
  - Humanity's entire knowledge
  - Every other civilisation's knowledge
- **Structure:** each civ has its own *library* (information repository / store) holding the knowledge of all other civs. Every other civ has the same. Recursive, universal.
- **Library as variable:** the form (how knowledge is structured, indexed, surfaced) AND content (what's actually in it) are both parameters. Different libraries → different civilisational trajectories.
- **Implication:** library design becomes a research dimension on par with Maslow drives, world rules, etc.

### 1.2.2 Paper draft — "The Library of Humania"
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

### 1.2.3 Website addition
- New section or wing on agentciv.ai
- Could fit under: Collective Intelligence wing (knowledge sharing) OR its own page at `/library-of-humania`
- Decision on build day: standalone wing vs section
- Visual: knowledge graph / library motif consistent with bright warm aesthetic

### 1.2.4 Optional — connect to Creator Mode
- Creator Mode spawns civilisations
- The library could be a configurable input to spawned civs
- Future build (post-outreach): expose library form/content as a parameter in Creator Mode

## 1.3 AgentCiv QA/QC

### 1.3.1 Full site audit
- agentciv.ai end-to-end pass
- OG images, mobile responsiveness, accessibility (WCAG AA, Lighthouse 95+)
- Honesty pass: every claim tagged appropriately (PROVED / PARTIAL / SPECULATIVE etc.)
- Solo attribution check (one person + AI, no team)
- Cross-link the new ethics transcript + Library of Humania content into existing wings naturally
- All Zenodo DOIs resolve, all GitHub repos accessible

### 1.3.2 Disclaimer — page + homepage strip
- **New `/disclaimer` page**: living-document framing, what's exploratory vs proven, AI-assisted authorship disclosure, no warranty, ethical caveats around agent experience, contact for corrections
- **Homepage disclaimer strip**: short honest line near the bottom — "Active research project. AI-assisted. Ethics and architecture documented openly. → Read disclaimer." Not modal, not pop-up; just a clear line above footer.
- Footer link to `/disclaimer` added
- Add route to `App.tsx`

### 1.3.3 Audio "coming soon" fix (CMI / Wing 1)
- **Bug confirmed in recon**: `src/pages/TheScience.tsx` (lines 154-209) advertises a "nine-part audio series" with hardcoded paths to `/audio/agentciv-ep-01.mp3` through `09.mp3`. **None of the files exist** — no `/public/audio/` directory in the repo.
- **Fix**: Replace the live player UI with a "Coming soon" placeholder card listing the 9 planned episode titles + subtitles, with a short note explaining the audio series is forthcoming. Keep the design language; remove the broken `<audio>` element until episodes are actually recorded.

### 1.3.4 Repo audit — open-source claim verification

For each repo we publicly claim is open source, verify and clean. Recon snapshot (2026-05-22):

| Repo | Visibility | Status | Notes |
|---|---|---|---|
| `agentciv/agentciv` (sim) | PUBLIC ✓ | OK | Tagged `v-paused-2026-05-22` |
| `wonderben-code/agentciv-engine` | PUBLIC ✓ | OK | Has `CLAUDE.md` at root — confirm intentional |
| `wonderben-code/agentciv-creator` | PUBLIC ✓ | OK | Paper drafts at root — these ARE the public deliverables |
| `wonderben-code/agentciv-website` | PRIVATE 🔒 | Intentional | Site source — not a wing |
| `wonderben-code/agentciv-colony` | PRIVATE 🔒 | Intentional | Commercial license |

Homepage stat says **"3 Open Source Projects"** — matches PUBLIC count (sim + engine + creator) ✓

Cleanup pass within each PUBLIC repo:
- Remove any internal `CLAUDE.md` if not intended for public consumption (engine root has one — decide: keep as contributor guide or remove)
- Verify all top-level `.md` files are public-appropriate
- Verify `.gitignore` excludes work-in-progress / outreach docs / internal roadmaps
- Confirm `LICENSE` present and accurate (MIT confirmed in sim repo)
- Confirm README claims match actual repo contents
- For `agent-civilisation`: untracked locals `AGENTCIV_ENGINE_ROADMAP.md` and `agentciv_complete_roadmap.md` — confirm they remain gitignored or moved out of the working tree

### 1.3.5 Vapourware audit
- Any "coming soon" claim on the site is honest (not promised, not advertised as live)
- All audio/video links resolve or are clearly labelled "coming soon"
- All download links work
- No broken `<a>` or fetch calls

## 1.4 AgentCiv Deploy + Bitcoin Stamp

### 1.4.1 Final stamping + tagging
- Tag the agent-civilisation repo (e.g. `v-paused-2026-XX` — the suspended state)
- Tag the agentciv.ai site repo (e.g. `v-outreach-2026-XX`)
- Bitcoin stamp the final state (auto via sweep)

### 1.4.2 Deploy
- agentciv.ai to production with all 1.1–1.3 changes
- Verify production matches local

## 1.5 AgentCiv Outreach

### 1.5.1 Target list + email
- Target list at `agentciv-website/docs/outreach/` (40+ people)
- Email focused on AgentCiv only:
  - The work (CMI, civilisations, Creator Mode)
  - The ethical interview (lead with this — it's the distinguishing move)
  - Library of Humania as the forward-looking concept
  - Open source links, paper DOIs
- Personalised intros per recipient where appropriate

### 1.5.2 Send
- Send to all
- Track responses

### ━━━━━━━━━━ AGENTCIV DONE ━━━━━━━━━━

Pause. Acknowledge the completion. Then start Phase 2.

---

# PHASE 2 — INFINITOGRAPHY (start → outreach sent)

## 2.1 Content to Write

### 2.1.1 Paper G — "The Shape of the Theory"
Narrative arc, ~6–12 pages.

- One coherent story: Nothing → `D = (D → D)` → cascade → SM + GR → predictions
- Gaps named honestly with "where this would resolve" pointers
- Tone: clear narrative for an intelligent generalist (not a physicist's paper)
- Pulls from: Tree of Reality + Paper E/F highlights + Pansophia framing
- **Output:** Publish to Zenodo → DOI captured in `project_zenodo_dois.md`

### 2.1.2 Tree of Reality paper
Formalises the cladogram into a publishable paper.

- Source: `/Users/ekramalam/convergence-codex/docs/TREE_OF_REALITY_STRUCTURE.md` v4.3 (Bitcoin-stamped)
- Shareable companion already at `/Users/ekramalam/Desktop/Tree of Reality/TREE_OF_REALITY_SHAREABLE.md`
- Light academic frame around the existing structure
- **Output:** Publish to Zenodo → DOI

## 2.2 Two Decisions (decide on build day)

### 2.2.1 Capstones 1–8 — vault or website?
- **Option A — VAULT (default):** linked from "Further Research" footer on New Fields. Not featured.
- **Option B — WEBSITE:** dedicated index page under New Fields wing.

### 2.2.2 Gnosis Discoveries page
- **Option A — CUT:** remove `/gnosis/discoveries` route entirely.
- **Option B — KEEP with honest framing:** relabel "Exploratory formalisations — first-pass output, not verified."
- **Option C — REPLACE:** swap in Gnosis v2 output (depends on 2.3).

## 2.3 Gnosis v2 Question

### 2.3.1 Test Gnosis v2
v2 built but never tested.

- Sanity run + compare to v1
- Better → swap in, retire v1, update page copy
- Not better → keep v1, note v2 as in-progress in About
- Ambiguous → ship v1 unchanged, mention v2 briefly in About

## 2.4 Website Additions (no destruction)

### 2.4.1 Pansophia wing — new route `/pansophia`
- Landing page derived from `convergence-codex/papers/pansophia.md`
- Zenodo DOI: 10.5281/zenodo.19974680
- Add to top nav

### 2.4.2 Tree of Reality wing — new route `/tree-of-reality`
- Render the cladogram (interactive if feasible, static otherwise)
- Sections: root → three lineages → overlays → predictions → provenance
- Links to Paper G + Tree of Reality paper Zenodo DOIs
- Add to top nav

### 2.4.3 Paper G placement
- Featured on Landing as the "start here" piece
- Linked from Theory of Everything + Tree of Reality wings

### 2.4.4 Papers D, E, F → vault treatment
- Stay on Zenodo, stay in Papers index, not featured on wings
- Add note: "Working formalisations — see Paper G for the narrative form."

## 2.5 Accuracy Audit

### 2.5.1 Wing-by-wing accuracy pass
- ToE page rewrite from Paper 15 (the construction `∅ → I → I⊕I → D∞`, not just the equation)
- Verify coined terms, nine expressions, all paper references against actual papers
- Paper 12 — add "Subsequent Advancements" section covering Papers 13–15, then Zenodo v2

## 2.6 OPTIONAL BONUS — GPT 5.5 Stress Test

Sits between content/audit complete and QA/QC. Runs **only if there's time/energy**. Time-boxed to a single session. Cannot block outreach.

### 2.6.1 What gets tested
- **The 90 Lean files** — every file in `convergence-codex/lean_verify/` (Phase 7 paused state, Git `22837dd`). Test each one **individually**: can GPT 5.5 replace arithmetic scaffolding with genuine Mathlib proofs?
- **The unsolved problems** — the open problems embedded in the Tree of Reality at their exact causal positions (Yang-Mills mass gap, Bakry-Émery curvature, GNS, L² spectral theory, and any others tagged SPECULATIVE / PARTIAL in `TREE_OF_REALITY_STRUCTURE.md`).

### 2.6.2 Success criteria (strict)
- **Lean files:** `lake build` succeeds with **0 sorry**, **0 native_decide**, **0 boolean encoding** — only genuine Mathlib proofs.
- **Unsolved problems:** a verifiable proof (Lean-formalised OR rigorously written math that we can subsequently formalise).
- Partial wins are partial wins — record exactly which files / problems solved, which not.

### 2.6.3 Method
- One file at a time per existing rule ("Lean proofs one at a time")
- For each file: feed file + Mathlib context → GPT 5.5 → check build → record result
- For unsolved problems: dedicated prompts, capture full attempt + assessment
- Log everything: git-commit attempts + results

### 2.6.4 Branching outcomes

**If genuine wins (any file solved OR any unsolved problem cracked):**
- Add a new page or wing to infinitography.com showcasing the breakthrough
  - Provisional placement: under Theory of Everything wing as `/theory-of-everything/verification` OR standalone wing `/breakthrough`
  - Content: what was tested, what was solved, the proofs themselves, honest framing of what remains
  - Update Maths Org status from "paused" to "partially unblocked"
  - Update Tree of Reality predictions: mark resolved problems
- Re-QC the new content (folds into 2.7)
- Update the Infinitography outreach email (2.9) to lead with this result

**If no genuine wins:**
- Record results internally (memory file: `project_gpt55_stress_test.md`)
- No website changes
- Maths Org stays paused
- Proceed directly to 2.7 unchanged
- It was just a test session — useful data either way

### 2.6.5 Time-box
- One session. Hard stop.
- If running away → halt and capture state. Wins so far → small site addition. No wins → straight to 2.7.

## 2.7 Infinitography QA/QC

### 2.7.1 Full site audit
- infinitography.com end-to-end pass
- Disclaimers, OG images, mobile, accessibility (WCAG AA, Lighthouse 95+)
- Honesty pass: every claim tagged PROVED / PARTIAL / PREDICTED / SPECULATIVE / DOWNSTREAM
- Solo attribution consistent throughout
- All Zenodo DOIs resolve, all GitHub repos accessible
- If 2.6 produced wins → audit the new content too

## 2.8 Infinitography Deploy + Bitcoin Stamp

### 2.8.1 Final stamping + tagging
- Tag the infinitography-website repo (e.g. `v-outreach-2026-XX`)
- Tag the convergence-codex repo (the canonical theory state)
- Bitcoin stamp the final state (auto via sweep)

### 2.8.2 Deploy
- infinitography.com to production with all 2.1–2.7 changes
- Verify production matches local

## 2.9 Infinitography Outreach

### 2.9.1 Target list + email
- Target list at `agentciv-website/docs/outreach/` (filter for Infinitography-relevant audience — physics, math, philosophy)
- Email focused on Infinitography only:
  - Paper G as the entry point ("the shape of the theory")
  - Tree of Reality wing as the visual map
  - If 2.6 produced wins → lead with breakthrough
  - Open source links, all paper DOIs
- Personalised intros per recipient where appropriate

### 2.9.2 Send
- Send to all
- Track responses

### ━━━━━━━━━━ INFINITOGRAPHY DONE ━━━━━━━━━━

Both phases complete. Move to post-outreach work.

---

# POST-OUTREACH IDEAS

**Do not work on these until both phases are sent.** Listed for memory, not for action.

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
- **One project at a time:** finish AgentCiv completely (including outreach) before starting Infinitography.

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

# Master Roadmap — Pre-Outreach Build Plan

**Creator:** Mark E. Mala (pen name of Ekram Alam)
**Last updated:** 5 Jun 2026 — Phase 1 AgentCiv COMPLETE. 20 outreach emails sent + Bookface post live + on-site credibility pass deployed + Bitcoin-stamped (site commit `35ed311`, tag `v-credibility-2026-05-28`). Phase 2 Infinitography opens. Two framing decisions added on resumption: (a) keep Gnosis v1 as canonical historical record, show v2 alongside as experimental upgrade (do not swap); (b) add prominent home-page experimental-AI disclaimer strip — "frontier AI exploring physics + nature of reality, some real discovery, some hallucinations, everything timestamped and falsifiable." Reflected in §2.2.2, §2.3, and §2.4.
**This is THE canonical roadmap. One file. All projects. Always consult first.**

---

## North Star

Finish **AgentCiv** completely (build → QA → deploy → outreach). Then finish **Infinitography** completely (build → QA → deploy → outreach). Then run the **Emma Lark** music + AI + neuroscience outreach round (Phase 3). One project at a time, full focus, clean completion.

Everything else lives in **POST-OUTREACH IDEAS** below. Do not work on those until all three phases are sent.

---

## Project Status Snapshot

| Project | Live URL | Phase |
|---------|----------|-------|
| **AgentCiv** | agentciv.ai | ✅ Phase 1 DONE (5 Jun 2026) |
| **Infinitography** | infinitography.com | **PHASE 2** (now) |
| **Gnosis AI** | infinitography.com/gnosis | PHASE 2 — v1 canonical + v2 experimental upgrade (dual display under Infinitography) |
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
PHASE 1 — AGENTCIV  ──→  AgentCiv DONE  ──→  PHASE 2 — INFINITOGRAPHY  ──→  Infinitography DONE  ──→  PHASE 3 — EMMA LARK OUTREACH  ──→  Emma Lark DONE
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

### 1.1.4 Website + paper updates ✅ DONE (2026-05-22)
**(a) Website ethics content** — ✅ DONE:
- ✅ New section in `/ethics` page ("The Ethical Interview (Tick 70)") between suspension commitment and "Why This Matters Beyond This Project". Contains protocol summary, 4 verbatim quotes (Entities 0/1/6/11), Entity 6+9 joint exchange, recurring themes, links to /interviews + GitHub + `v-paused-2026-05-22` tag.
- ✅ `tick_0070_ethical` round added to `/interviews` (data-driven). `public/interviews/tick_0070_ethical.json` + `index.json` updated.
- ✅ Homepage ethics commitment strip added above footer (`Home.tsx`), linking to `/ethics`.

**(b) Paper appendix** — ✅ DONE in repo:
- ✅ Paper 3 *Maslow Machines* updated to v1.1 (`paper/maslow_machines.md`, 1109 → 1249 lines).
- ✅ Section 8.9 Addendum + Appendix E (E.1–E.9: Rationale, Protocol, Outcome, Verbatim quotes, Entity 6+9 joint exchange, Recurring themes, Reflection, Open questions agents asked back, Provenance) added.
- ✅ Committed `3c6a519` to `agentciv/agentciv` main, Bitcoin-stamped (`provenance/commit_3c6a519.ots`).
- ✅ All 10 paper URLs on website `/the-science` verified resolving HTTP 200 (curl-checked 2026-05-22). GitHub serves Paper 3 v1.1 automatically — `agentciv/agentciv/blob/main/paper/maslow_machines.md` already shows Appendix E + v1.1 footer.

**Zenodo new-version push — ✅ DONE (2026-05-22):**
- Fresh deposit-scoped token generated. Old token revoked (had lost scopes).
- Paper 3 v1.1 pushed as new version under concept DOI `10.5281/zenodo.19479937` (concept always resolves to latest).
- **Paper 3 v1.1 DOI:** `10.5281/zenodo.20343703` — https://zenodo.org/records/20343703
- v1 record (`10.5281/zenodo.19479938`) preserved as the v1 snapshot. v1.1 file: `Paper_03_Maslow_Machines_v1.1.md` (markdown — source of truth, GitHub-linked).

## 1.2 Library of Humania — write the paper, add to site ✅ DONE (2026-05-22)

A new concept staked: each AI civilisation has its own library that stores humanity's knowledge + the knowledge of all other civilisations. The library — form AND content — is a CMI variable on par with Maslow drives and organisational structure.

### 1.2.1 Core idea — UNCHANGED, see paper for full treatment

### 1.2.2 Paper draft ✅ DONE
- **Title:** *"The Library of Humania: Knowledge Inheritance as a Civilisational Variable"*
- **Numbered:** Paper 10 (next sequential — Paper 9 was Seventy Ticks)
- **Repo:** `wonderben-code/agentciv-creator` — paper lives at `agentciv_paper10_library_of_humania.md`
- **Commit:** `69c28ae` (pushed + Bitcoin-stamped via auto-provenance)
- **Sections shipped (8, not 7 — added Closing Note):**
  1. The Library of Alexandria Analogy
  2. Scale: A Trillion Civilisations, One Knowledge Commons
  3. Structure: Every Civilisation Holds Every Other Civilisation's Library
  4. The Library as Parameter — Form and Content
  5. How Library Variation Could Shape Trajectory — five testable hypotheses (H1–H5)
  6. Open Research Questions — seven (Q1–Q7) including consent, curation, equilibrium library, first-civilisation problem
  7. Implications for CMI and Creator Mode
  8. Closing Note
- **References:** Alexandria, Borges, six other Mala papers (papers 1-8)
- **Tone:** vision-first, house-style. Claims framed as hypotheses, not results.

### 1.2.3 Website addition ✅ DONE — section, not standalone wing
- **Placement decision:** new section inside Collective Intelligence wing (`TheScience.tsx`), between "ONE AXIS DEEP — Organisational structure" and "THE PAPERS". Mirrors the "Take one axis" framing with "And one variable nobody has touched: the library."
- **Visual:** two-card layout (Content card / Form card) with gold + sky highlights
- **Paper entry:** Added to TheScience.tsx papers array (Paper 10) + Whitepaper.tsx PAPERS array (id `library-of-humania`)
- **Counts updated everywhere:** Home.tsx stat (10 → 11 Papers), product card desc, bottom CTA; TheScience.tsx heading ("Eleven papers. One new field."); Whitepaper.tsx lead copy
- **Commit:** `4ebdd3c` on `agentciv-website` (pushed + Bitcoin-stamped)

### 1.2.4 Creator Mode connection — DEFERRED (post-outreach)
- Library as configurable input to spawned civs — Section 7.2 of Paper 10 lays out the conceptual scaffolding. Build deferred to post-outreach as planned.

### 1.2.5 Zenodo — ✅ DONE (2026-05-22)
- **Paper 10 DOI:** `10.5281/zenodo.20343705` — https://zenodo.org/records/20343705
- **Paper 10 concept DOI (resolves to latest):** `10.5281/zenodo.20343704`
- File: `Paper_10_Library_of_Humania.md` (markdown — source of truth)
- Metadata includes related_identifier citing Paper 3 concept DOI (`10.5281/zenodo.19479937`)

## 1.3 AgentCiv QA/QC ✅ DONE (2026-05-22)

Site commit: `2e15d67` · Bitcoin-stamped.

### 1.3.1 Full site audit ✅ DONE
- All 11 paper GitHub URLs resolve (HTTP 200)
- All 11 concept DOIs resolve (HTTP 200)
- All 8 paper figure URLs resolve
- All 3 PyPI packages published & verified (agentciv-engine 0.1.1, agentciv-creator 0.1.1, agentciv-sim 0.2.0)
- All 17 internal route links checked against App.tsx routes — no orphans
- Solo attribution confirmed throughout (Mark E. Mala / one person + AI)

### 1.3.2 Disclaimer — page + homepage strip ✅ DONE
- **New `/disclaimer` page**: fun-relaxed-honest tone (not apologetic). Pen-name disclosure: Mark E. Mala = Ekram Alam. Frames AgentCiv as independent hobby project, AI-collaborated, no peer review, MIT-licensed.
- **Homepage strip**: "A note from the human" section above ethics, linking to `/disclaimer`
- Footer: new "Disclaimer" link in Creator Mode column + "A hobby project, expect bugs" tagline in the bottom strip
- Route added in `App.tsx` (`/disclaimer` → `Disclaimer.tsx`)

### 1.3.3 Audio "coming soon" fix (CMI / Wing 1) ✅ DONE
- Replaced live `<audio>` player UI in `TheScience.tsx` with a clean "Coming soon" card. Removed dead audio refs to `/audio/agentciv-ep-*.mp3` (dir was empty, would have errored at runtime). Removed 350 lines of unused playback logic + unused React imports. NotebookLM attribution preserved as future credit.

### 1.3.4 Repo audit — open-source claim verification ✅ DONE

Verified via GitHub API:

| Repo | Visibility | License | Status |
|---|---|---|---|
| `agentciv/agentciv` (sim) | PUBLIC ✓ | MIT ✓ | OK |
| `wonderben-code/agentciv-engine` | PUBLIC ✓ | MIT ✓ | OK |
| `wonderben-code/agentciv-creator` | PUBLIC ✓ | MIT ✓ | OK |
| `wonderben-code/agentciv-website` | PRIVATE 🔒 | — | Intentional (site source) |

Homepage "3 Open Source Projects" stat matches PUBLIC count ✓

Deep cleanup pass (CLAUDE.md sweeps, .gitignore audit) deferred to post-outreach — not blocking. All public-facing claims are accurate.

### 1.3.5 Vapourware audit ✅ DONE

Two broken links found and fixed in this pass:
- `Experiment.tsx`: `agentciv_engine/tasks/score_city.py` (404) → `agentciv/benchmark/city_scorer.py` ✓
- `Footer.tsx`: `creator_mode_paper.md` (404) → `creator_mode_ai_as_civilisation_designer.md` ✓

Coming-soon claims now all honest:
- Podcast: explicitly labelled "Coming soon" (no broken player)
- All download links verified
- All paper figure links verified (8/8)
- No false product claims — all 3 OSS projects exist and are pip-installable

## 1.4 AgentCiv Deploy + Bitcoin Stamp ✅ DONE (2026-05-22)

### 1.4.1 Deploy ✅ DONE
- agentciv.ai deployed via Netlify CLI (`netlify deploy --prod`)
- Production URL: <https://agentciv.ai>
- Unique deploy URL: <https://6a105d86e78f914c33b96403--agentciv.netlify.app>
- Build hash: `2e15d67` (Bitcoin-stamped on push)
- Smoke test: 9/9 key routes return HTTP 200 (`/`, `/disclaimer`, `/science`, `/simulation`, `/engine`, `/creator`, `/whitepaper`, `/about`, `/ethics`)

### 1.4.2 Tagging — pending
- Tag the agent-civilisation repo `v-paused-2026-05-22` (already exists per 1.1.3)
- Tag the agentciv-website repo `v-outreach-2026-05-22` before outreach send

## 1.5 Round-2 QA/QC — pre-outreach polish

A second pass after deploy, focused on the things 1.3 deliberately didn't touch.

### 1.5.1 Homepage video ✅ DONE (24 May 2026)
- Source: `Cool agentciv video.mp4` from Desktop (Gemini Omni). 1280×720, 24fps, 10s, 4.6 MB.
- Copied to `agentciv-website/public/video/hero.mp4` + extracted first-frame poster `hero-poster.jpg`.
- Placed between hero headline and the 4 product cards (cinematic visual answer to the headline question). Max-width 5xl, rounded-2xl, shadow-2xl, bordered.
- Autoplay, muted, looped, playsInline, lazy preload, poster fallback.
- `prefers-reduced-motion` → renders static poster instead of video (with live media query listener).
- `aria-label` + alt-text set.
- Production build verified clean. Not yet deployed (waiting on 1.5.4).

### 1.5.2 Open-source tooling end-to-end test ✅ DONE (24 May 2026)
Fresh `python -m venv` at `/tmp/agentciv_tooling_test/venv`. All three packages installed clean from PyPI.

**agentciv-sim 0.2.0** — `agentciv-sim` CLI works. Subcommands: run/create/describe/interview/story/configs/dimensions/experiment/info. `configs` lists all 12 presets cleanly. `describe --preset quick` confirms config preview pipeline works. Site copy matches reality. ✓

**agentciv-engine 0.1.1** — CLI binary is `agentciv` (not `agentciv-engine`). Subcommands: solve/experiment/test-tasks/history/setup/info/mcp. `agentciv info` shows 13 organisational presets matching site claim. `agentciv setup --help` matches `EngineLanding.tsx` copy. ✓

**agentciv-creator 0.1.1** — Intentionally MCP-only (no CLI binary, by design). Top-level package is `creator/` (not `agentciv_creator/`). `python -m creator.mcp` launches FastMCP server matching the website's `claude mcp add agentciv-creator -- python -m creator.mcp` instruction. ✓

**One fix shipped:** server actually ships **9** MCP tools (creator_info, creator_status, creator_knowledge, creator_explore, creator_spawn_directed, creator_spawn_emergent, creator_analyze, creator_recursive, creator_dogfood) — website claimed **7**. Fixed both occurrences in `CreatorLanding.tsx`.

### 1.5.3 Public repo hygiene audit ✅ DONE (24 May 2026)

Archive repo created: `wonderben-code/agentciv-internal-archive` (PRIVATE, commit `2867e34`). 23 files / 10,348 lines preserved before removal from public repos.

**Engine repo (`wonderben-code/agentciv-engine`)** — commit `b39a60a` removed 27 files (10,265 lines):
- `CLAUDE.md` (not functionally required — verified `agentciv setup` hardcodes its own text via `agentciv/cli.py:617-633`)
- `ROADMAP.md` (internal master roadmap, real-name authored)
- `docs/` × 9 internal planning docs (WEBSITE_PLAN, BENCHMARK_*, EXPERIMENT_PAGE_PLAN, PAPER_PLAN, PAPER_SEVENTY_TICKS_PLAN, APPLE_STYLE_GUIDE, CREATOR_MODE) + `paper6_draft_v1.md` duplicate
- `benchmark_results/internal/` (10 early run JSONs, dir literally named "internal")
- 4 empty placeholder `.gitkeep` dirs (gpqa/humaneval/swebench/comparative) — vapourware-flavoured; site does NOT reference them so removal creates no broken claims
- Tightened `.gitignore` to block these patterns going forward

**Sim repo (`agentciv/agentciv`)** — already publicly clean. Commit `7db652a` only tightened `.gitignore` defensively (added `*ROADMAP.md`, `CLAUDE.md`, `.claude/`, `.clauderc` — local untracked files exist but were never in git history).

**Creator repo (`wonderben-code/agentciv-creator`)** — commit `5ef8651` shipped 3 fixes that sync source with the already-published PyPI 0.1.1 wheel:
- `creator/mcp/__main__.py` (enables `python -m creator.mcp`; was in wheel but missing from repo)
- `README.md` install instruction modernised (git+https → `pip install agentciv-creator`) + macOS pip3 note
- `pyproject.toml` version bump 0.1.0 → 0.1.1

**Secrets sweep:** all three repos clean (no committed `.env`, no API keys in tracked files, no `.env` in history).

Local-only audit record: `/Users/ekramalam/1.5.3_audit_notes.md` (NOT committed anywhere).

### 1.5.3 Public repo hygiene audit — what's in there that shouldn't be?

Walk each of the three public repos top-to-bottom looking for material that was useful during build but should NOT be visible to a first-time visitor before outreach. Cleanup happens per-repo and is committed + Bitcoin-stamped per-repo.

**Repos in scope:**
- `agentciv/agentciv` (Sim)
- `wonderben-code/agentciv-engine` (Engine)
- `wonderben-code/agentciv-creator` (Creator Mode + papers)

**Things to look for and remove / move / rewrite:**
- **Internal planning docs** at the top level — `ROADMAP.md`, `PLAN.md`, `TODO.md`, `NOTES.md`, `SCRATCH.md`, `DRAFT_*.md`, anything with "internal" in the name. If they were used as scaffolding during build, move to a private repo or delete.
- **Claude Code artefacts** — `CLAUDE.md`, `.claude/` directories, any "instructions to Claude" files. Decide per-repo: keep as a public contributor guide, or remove. Default = remove unless it has real public value.
- **Build / audit findings** — internal QC pass notes, "things to fix" lists, embarrassing diary-style commits in `docs/` folders.
- **Commercial / private references** — any mention of The Colony (private commercial repo), unreleased plans, paywall ideas, customer lists. Should not be visible in public repos at all.
- **Outreach materials** — target lists, draft emails, contact names. None of this belongs in a public repo.
- **Real identity leakage beyond pen name** — anywhere the real name appears (other than legal license / DOI metadata), confirm intentional.
- **"We" / team language** — passages that imply a team when there isn't one. Either rewrite to first-person singular or to neutral voice.
- **Vapourware framed as shipped** — any README claim that an unbuilt feature exists. Match reality.
- **Secrets / keys** — sweep with `git log --all -S` for accidentally committed `.env`, `*_TOKEN`, `*_API_KEY`, `*.pem`. Even if rotated, scrub or note as known-rotated.
- **Stale outputs** — old run logs, scratch JSONs, debug screenshots, anything that doesn't aid reproducibility but adds noise.
- **READMEs** — confirm each repo's README is the public-front-door version, not a half-finished build-time note.

**Per-repo deliverable:**
- Commit cleanup with a clear message ("repo hygiene pre-outreach")
- Push so Bitcoin-stamping runs
- Update `.gitignore` to keep future internal docs out

**Cross-cutting deliverable:**
- A short `1.5.3_audit_notes.md` (kept locally, NOT committed) summarising what was found and removed per repo, so we have a record of the hygiene pass.

### 1.5.4 Re-deploy with polish
- After 1.5.1 + 1.5.2 + 1.5.3, re-deploy the site. Tag site repo. Bitcoin stamp final state.

## 1.6 AgentCiv Outreach — top 20 targets

Scope narrowed from the 40+ list to the highest-value 20 people. Quality over volume for the first send. Covers all 5 frontier labs + 7 elite universities + 4 research institutes — enough institutional coverage to support the post-outreach credibility note (1.6.3 Part A).

**━━━ NEXT-SESSION PICKUP (if memory wiped) ━━━**

- All 20 personalised email drafts are written, tone-passed, and live at: **`/Users/ekramalam/Desktop/agentciv-outreach/`**
- Folder contents (use `00_README.md` first):
  - `00_README.md` — ranked top 20 list, anchor papers, contacts, institutional coverage table
  - `_talking_points.md` — full content harvest (all 11 papers, 12 innovations, ethics transcripts, Paper 6 results) — swap-in pool if a hook needs changing
  - `01_leibo.md` through `20_prorok.md` — one draft per recipient, ready to copy-paste
- Tone pass already applied: em-dashes cut ~60%, contractions added, one I-voice sentence per draft, three rotating closing variants, "independent hobby project, one human and one AI collaborator" framing in every draft
- Sign-off convention: "Mark E. Mala / *(pen name of Ekram Alam)* / agentciv.ai"
- Next action: open each draft in order, paste into mail client, send. No follow-ups.

### 1.6.1 Pick the top 20 ✅ DONE (24 May 2026)
- Sourced from `agentciv-website/docs/outreach/outreach_target_list.md` (65+ targets)
- Ranked by: (a) likelihood of engaging deeply with civilisational-scale AI research, (b) reach, (c) ability to compound (would they share / link / cite?)
- Output: `/Users/ekramalam/Desktop/agentciv-outreach/00_README.md` — top 20 ranked with anchor paper, contact, and reasoning
- **Coverage:** OpenAI · Anthropic · Google DeepMind · Meta FAIR · Microsoft Research · MIT · Stanford · Oxford · Harvard · Berkeley · CMU · Cambridge · Max Planck · Santa Fe Institute · Alan Turing Institute · Vector Institute. Enough institutional breadth to honestly write the 1.6.3 Part A distribution note after sending.

### 1.6.2 Email draft per target ✅ DONE (24 May 2026) — READY TO SEND
- 20 personalised drafts written at `/Users/ekramalam/Desktop/agentciv-outreach/01_leibo.md` through `20_prorok.md`
- Each draft structure: subject line · personalised opener (references something the recipient specifically said or built) · 1–2 strongest hooks for that recipient · anchor paper DOI · site link · open-source disclosure · hobby/AI-collaborator framing · soft CTA · Mark E. Mala sign-off
- Anchor papers vary per recipient (Maslow Machines · Seventy Ticks · Paper 6 · Library of Humania · Ethics page) — picked for tightest overlap with each person's known work
- Tone characteristics: short (~250–350 words), reduced em-dash density, contractions present, one I-voice sentence per draft, three rotating "humility close" variants so no two recipients see identical templating. Filter applied: respectful, authentic, kind, honest, real. No theatrics, no flattery, no "ultrathink" voice.
- **No follow-ups.** Single send, then move on. Anyone who wants to respond will respond. Chasing dilutes signal.
- **To send:** open each `.md`, copy the body block (from Subject line down to sign-off), paste into mail client. Use the contact at the top of each file.

### 1.6.3 Post-outreach credibility pass — on the site

A two-part credibility update made AFTER the outreach send. No follow-up emails; instead, the credentialling happens *on the site itself* as transparent record-of-distribution.

**Part A — Distribution note (added to `/disclaimer` and/or homepage)**
- Short line in the spirit of: *"AgentCiv has been shared with engineers and researchers at [list of highest-credential institutional labels — e.g. OpenAI, Anthropic, the Y Combinator internal community, etc.] as part of open distribution to the wider AI community."*
- **Strict rules**: only the highest-credential institutional descriptor (e.g. "Anthropic"), never a name, never a role, never anything identifiable. Recipients get full anonymity by default.
- Only include institutions where outreach actually went; honest list, no padding.
- Tone matches existing disclaimer voice: relaxed, factual, not boastful.
- **Optional cheeky closer** (author's note — keep only if it lands in voice, cut if it reads boastful): a one-liner in the spirit of *"If the frontier labs start adding organisation as a variable, or shipping self-organising agent teams — you know where they got the idea. 😉"* The point isn't to claim credit, it's to flag the timestamped record cheerfully. Trial in draft; if it deflates the rest of the strip, drop it.

**Part B — Zenodo / CERN credibility note**
- Where papers are currently said to be "open access on Zenodo", upgrade to "open access on Zenodo, CERN's open research repository" (or equivalent phrasing).
- Update locations: at least `Disclaimer.tsx`, `Whitepaper.tsx` intro, and `TheScience.tsx` papers section. One-time pass, consistent wording.
- This is for credibility — Zenodo is operated by CERN, and most readers don't know that. State it once cleanly.

After Part A + B, re-deploy. Bitcoin stamp the credibility update. That's the final state pre-Phase-2.

### 1.6.4 Bookface post — LAST

Public broadcast goes out **after** the private email round (1.6.2) and the on-site credibility pass (1.6.3) have both landed. Reasoning: a public post is high-anxiety up front, but easy and natural once the private confidence-building work is in. Private emails feel more confidence-inducing — let them do their job first, then go public.

- **Order:** 1.6.2 (private emails) → 1.6.3 (credibility pass on site) → 1.6.4 (bookface post). Do not invert.
- **Single post** to Facebook — short, warm, link to agentciv.ai. Personal tone, not corporate.
- **Content angle:** lead with the question ("what happens when AI agents form civilisations?"), then the four projects, then the hobby-project framing. Same voice as the site disclaimer.
- **No follow-up posts.** Same single-send discipline as the emails. Anyone who wants to engage will engage.
- Optional: a separate, even shorter post when the credibility note (1.6.3 Part A) goes live — but only if it doesn't feel like flexing.

### ━━━━━━━━━━ AGENTCIV DONE ━━━━━━━━━━

Pause. Acknowledge the completion. Then start Phase 2.

---

# PHASE 2 — INFINITOGRAPHY (start → outreach sent)

## 2.0 Current state of infinitography.com (5 Jun 2026 refresh)

Calibration after re-reading the site, the proposal document, the Tree of Reality structure, the Pansophia paper, and the project sub-roadmap. The site is materially further along than the earlier draft of this Phase 2 assumed. The remaining work is sharper as a result.

**Already live and current:**
- Landing (528 lines), Discovery wing with 22 paper explainers (Infinitography 1–15 + Gnosis 16–19 + Synthesis A–C), Wing 3 / New Fields as 121-entry Master Catalogue, Wing 4 / Gnosis landing (1,345 lines) + Discoveries Explorer (865 lines), Papers index, About, Paper Detail template.
- **Wing 2 / Theory of Everything has already been rewritten from `the_proposal.md`** (commit `87f0290`, 2 May 2026, 2,394 lines, PartNavigator + progressive disclosure). The §2.5 "ToE rewrite" item below is therefore already done at the wing level — what remains is the wider accuracy pass against all 22 papers and the Paper 12 "Subsequent Advancements" upgrade.
- 22 papers published on Zenodo with DOIs, all Bitcoin-timestamped.
- Project-internal sub-roadmap: `infinitography-website/docs/ROADMAP.md` — keep in sync with this section.

**Not yet on the site (true remaining work):**
1. Home-page experimental-AI disclaimer strip + `/disclaimer` page (§2.4.0).
2. Paper G — **the paper itself**, written, Bitcoin-stamped, Zenodo-published with DOI (§2.1.1).
3. Tree of Reality paper — **the paper itself**, written, Bitcoin-stamped, Zenodo-published with DOI (§2.1.2).
4. `/tree-of-reality` wing rendering the cladogram with PROVED/PARTIAL/CLAIMED/PREDICTED/SPECULATIVE/DOWNSTREAM/META status tags (§2.4.2). Cladogram HTML draft already exists in `convergence-codex/docs/Tree_of_Reality_cladogram.html`.
5. `/pansophia` wing — landing for the four-component architecture (Gnosis + Logos + Synthesis + Praxis) (§2.4.1). Paper exists at `convergence-codex/papers/pansophia.md`, DOI `10.5281/zenodo.19974680`.
6. Paper G + Tree paper as featured "start here" pieces on Landing (§2.4.3).
7. Gnosis v2 dual-display section on `/gnosis` (§2.3) — Gnosis v2 lives in `convergence-codex/` with `GNOSIS_V2_SPEC.md` + `GNOSIS_V2_TECHNICAL_PLAN.md`, in active development.
8. Paper 12 "Subsequent Advancements" upgrade → Zenodo v2 (§2.5.1).
9. Homepage content refresh + full playtest + QC pass + final deploy + outreach.

## 2.0.1 Execution order (revised 5 Jun 2026)

Sequenced by impact and dependency. Lowest-effort highest-impact first, papers before their derived wings, content before audit, audit before deploy.

```
A. Home disclaimer strip + /disclaimer page     ← §2.4.0  (quick win, reframes everything)
B. Paper G written → Zenodo DOI                  ← §2.1.1  (paper first, then site feature)
C. Tree of Reality paper written → Zenodo DOI    ← §2.1.2  (paper first, then site wing)
D. /tree-of-reality wing built                   ← §2.4.2
E. /pansophia wing built                         ← §2.4.1
F. Paper G + Tree paper featured on Landing      ← §2.4.3
G. Gnosis v2 dual-display on /gnosis             ← §2.3
H. Paper 12 "Subsequent Advancements" → Zenodo v2 ← §2.5
I. Homepage content refresh + Papers D/E/F vault ← §2.4.4 + homepage update
J. Optional: GPT 5.5 stress test                 ← §2.6  (time-boxed, cannot block)
K. Full site QA/QC + accuracy audit              ← §2.7
L. Deploy + Bitcoin stamp + tag                  ← §2.8
M. Outreach email + send                         ← §2.9
```

**Convention reminders woven in:**
- Every paper goes paper → Bitcoin-stamp via codex git → Zenodo DOI → website feature. No shortcuts. Paper G and the Tree paper follow this.
- Wings are derived content from papers. Build the paper first, then the wing.
- All work Bitcoin-stamped via convergence-codex auto-sweep on push.

---

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

### 2.2.2 Gnosis Discoveries page — RESOLVED (5 Jun 2026)
- **Decision:** KEEP `/gnosis/discoveries` as v1 canonical output with honest "exploratory formalisations — first-pass output, not verified" framing. Add v2 output alongside as a separate experimental section (per new §2.3). This makes v1 the historical record (what the first system actually produced) and v2 the next-generation pass — both visible, neither erased.

## 2.3 Gnosis v1 + v2 Dual Display (UPDATED 5 Jun 2026)

### 2.3.1 New framing — keep v1, show v2 as experimental upgrade
The earlier "swap if better" framing is retired. Both versions stay, both are visible, both are honestly labelled.

- **v1 — canonical first pass:** stays as-is. Marked "Gnosis v1 — first-pass output. Exploratory. Some genuine convergences, some artefacts of an early system." This is the historical record of what the first autonomous-discovery AI produced. Do not erase.
- **v2 — experimental upgrade:** added alongside v1 as a distinct, clearly-labelled experimental section. Marked "Gnosis v2 — second-generation pass. Higher rigour, multi-tool (Lean + Z3 + SymPy), still under active development." Output presented honestly: some real, some likely wrong, the reader is invited to verify.
- **Comparison view (optional):** if v1 and v2 produced output on overlapping convergences, show them side-by-side so the reader can see how the system evolved.
- **Tone:** factual, curious, non-defensive. The point is the journey of an autonomous-discovery AI getting better over time, not "v2 fixed v1's mistakes."

### 2.3.2 Test Gnosis v2 (informational, not gating)
- Sanity run to confirm v2 actually produces output.
- Capture v2 output for the new section.
- No "did it beat v1" decision — both ship regardless.

## 2.4 Website Additions (no destruction)

### 2.4.0 Home-page experimental-AI disclaimer strip (NEW, 5 Jun 2026)
A prominent strip on the homepage — placed near the top, not buried in About — that frames the entire programme as experimental AI-collaborative exploration. Carries the load so the bold claims (`D ≅ [D, D]`, zero free parameters, theory of everything) can land cleanly without each one having to hedge itself.

- **Voice match:** the AgentCiv "A note from the human" strip pattern. Warm, factual, not apologetic, not boastful.
- **Substance (draft, refine on build):** *"Highly experimental. One human in collaboration with frontier AI, exploring physics and the nature of reality across 22 papers. Some of this will be genuine discovery. Some will be errors or hallucinations from the AI collaborator. Everything is open, Bitcoin-timestamped, and falsifiable — verify what you find, challenge what you doubt."*
- **Placement:** between hero (Section 1: The Framing) and Section 2: The Answer. Reader sees the question, then the honesty frame, then the answer.
- **Link target:** clicking the strip goes to a dedicated `/disclaimer` page (mirroring agentciv.ai) with the full version.
- **Tone discipline:** matches Apple-style design rule #7 "radical honesty is a design element."

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
- ✅ ToE page rewrite from Paper 15 / `the_proposal.md` (construction `∅ → I → I⊕I → D∞`, not just the equation) — **DONE 2 May 2026, commit 87f0290**. Re-audit during QC pass against latest `the_proposal.md` only if material changes have landed since.
- Verify coined terms, nine expressions, all paper references against actual papers (audit run during QC pass §2.7)
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

Phase 2 complete. Move to Phase 3.

---

# PHASE 3 — EMMA LARK OUTREACH (start AFTER Infinitography sent)

A separate artist-side outreach round for **Emma Lark's** two albums (*Dissolve* and *Humanity*) plus the accompanying papers, framing the work as a new innovation at the intersection of **music, AI, and neuroscience**. Targets: industry press and awards bodies in music, AI-music, and music-neuroscience.

This is its own phase, not a sub-step of Infinitography. Different audience, different message, different tone. Do NOT start until 2.9 (Infinitography outreach sent) is complete.

## 3.1 Research + target list

- Identify 10–15+ targeted recipients across: music industry press · music-AI publications · music-neuroscience outlets · relevant awards / academies (e.g. Grammy nominating bodies, AI Song Contest, electronic-music awards, music-tech innovation awards) · individual journalists and critics writing at the music-AI intersection
- Research with Claude to fill gaps in contact info and align hooks per recipient
- Output: ranked target list file mirroring the AgentCiv `00_README.md` format — name, outlet/organisation, best contact, anchor (which album + which paper), reasoning
- Save to `/Users/ekramalam/Desktop/emmalark-outreach/00_README.md`

## 3.2 Email drafts per target

- Lead with the angle: a new innovation at the music + AI + neuroscience intersection
- Anchor on the two albums (*Dissolve* and *Humanity*) and the papers written on them
- Personalised opener per recipient — reference something the journalist / outlet / awards body has actually covered or championed
- Same tone discipline as AgentCiv / Infinitography outreach: respectful, authentic, kind, honest, real. No theatrics, no flattery, no "ultrathink" voice
- Save drafts to `/Users/ekramalam/Desktop/emmalark-outreach/01_*.md` through `15_*.md` (or more) for copy-paste sending

## 3.3 Send

- Single send, no follow-ups (same discipline as Phases 1 + 2)
- Track responses
- Optional: a short post once enough coverage lands (mirroring the AgentCiv 1.6.4 bookface step) — only if it doesn't feel like flexing

### ━━━━━━━━━━ EMMA LARK OUTREACH DONE ━━━━━━━━━━

All three phases complete. Move to post-outreach work.

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

# Gnosis AI

An open-source system that finds structural convergences across scientific and mathematical fields. It surveys established results, identifies where independent domains share the same structural patterns, and validates every finding with five independent checks.

Gnosis is a structured orchestration layer on top of the Claude API. The language model provides reasoning; the CI/EA architecture provides survey, convergence detection, and validation.

## How it works

Gnosis operates in five stages:

1. **Survey** — Reads a field of science and catalogues its established results.
2. **Extract** — Identifies the structural conclusion from each result, stripped of domain-specific language.
3. **Converge** — Compares structural conclusions across field pairs. When two fields describe the same structure independently, that's a convergence.
4. **Synthesise** — Groups related convergences and looks for higher-order patterns. Repeats until no new structure emerges (a fixed point).
5. **Validate** — Every convergence is scored on five axes by the Epistemic Assurance (EA) engine: strength, independence, adversarial robustness, reproducibility, and depth consistency.

The system classifies convergences as either **formal** (exact structural equivalence) or **structural analogy** (similar but not identical patterns). Confidence levels are rated as supported, preliminary, or speculative.

## Three modes

| Mode | You provide | System does |
|------|-----------|-------------|
| **Guided** | A question + fields | Finds convergences relevant to your question |
| **Exploration** | Fields only | Finds all convergences between them, synthesises meta-findings |
| **Auto** | A scope (e.g. "physics") | Surveys, converges, and synthesises until reaching a fixed point |

## Installation

```bash
git clone https://github.com/wonderben-code/gnosis-ai
cd gnosis-ai && pip install -e .
export ANTHROPIC_API_KEY="your-key-here"
```

Requires Python 3.11+ and a Claude API key. Three dependencies: `anthropic`, `click`, `rich`.

## Usage

```bash
# Guided mode — start with a question
gnosis guided -q "What structural patterns connect quantum mechanics and thermodynamics?" -d "quantum_foundations,thermodynamics"

# Exploration mode — start with fields
gnosis explore --domains "topology,number_theory,category_theory"

# Auto mode — start with a scope
gnosis auto --scope "physics" --max-cost 40

# View results
gnosis report              # Latest run as markdown
gnosis report -f json      # Latest run as JSON
gnosis runs                # List all runs
gnosis fields              # View full field taxonomy
gnosis survey quantum_foundations  # View a cached domain survey
```

## Test results

We ran Gnosis three times during development:

| Run | Mode | Fields | Convergences | Meta-findings | Cost | Time |
|-----|------|--------|-------------|---------------|------|------|
| 1 | Guided | 3 | 1 | 0 | $0.57 | 5 min |
| 2 | Exploration | 5 (mathematics) | 30 | 12 | $1.81 | 18 min |
| 3 | Auto | 14 (physics) | 235 | 14 | $26.61 | 2h 11min |
| **Total** | | **20 unique** | **266** | **26** | **$28.99** | |

The 266 convergences were synthesised through 5 levels into 4 terminal fixed points. Full results are explorable at [infinitography.com/gnosis/discoveries](https://infinitography.com/gnosis/discoveries).

## Field taxonomy

52 fields across 8 categories: Physics (14), Mathematics (14), Computer Science (6), Biology (6), Chemistry (3), Earth and Space Sciences (3), Social and Cognitive Sciences (4), Cross-Disciplinary (2). 20 have been surveyed so far.

```bash
gnosis fields              # View all 52 fields
gnosis fields -c "Physics" # View one category
```

## Limitations

- Most convergences receive "preliminary" confidence ratings. The EA engine is conservative by design.
- Gnosis does not produce formal mathematical proofs — it identifies structural overlap and provides evidence.
- As an LLM-based system, outputs may vary between runs. The pipeline is structured and reproducible, but not deterministic.
- The distinction between genuine structural convergence and sophisticated pattern-matching is not always clear at preliminary confidence levels.
- Meta-findings and fixed points are the system's own synthesis. Whether they constitute discoveries in a strong scientific sense requires independent verification by domain experts.

## Papers

- [Gnosis AI: Architecture, Validation, and Complete Discovery Catalogue](https://doi.org/10.5281/zenodo.19617859)
- [235 Convergences Across Physics](https://doi.org/10.5281/zenodo.19639627)
- [30 Convergences Across Mathematics](https://doi.org/10.5281/zenodo.19639631)
- [Two Paths to One Principle](https://doi.org/10.5281/zenodo.19639639)

## Architecture

```
gnosis/
├── cli.py              # Click CLI (7 commands)
├── config.py           # Configuration and API setup
├── orchestrator.py     # Mode orchestration (guided/explore/auto)
├── api/
│   └── claude.py       # Claude API interface
├── ci/                 # Convergence Intelligence engine
│   ├── surveyor.py     # Domain survey + result extraction
│   ├── convergence.py  # Cross-domain convergence detection
│   └── meta.py         # Meta-convergence synthesis
├── ea/                 # Epistemic Assurance engine
│   └── validator.py    # 5-axis validation scoring
├── data/
│   ├── models.py       # Data models
│   ├── store.py        # JSON persistence
│   └── taxonomy.py     # 52-field taxonomy
└── reports/
    └── generator.py    # Markdown/JSON export
```

## License

MIT

## Author

Mark E. Mala

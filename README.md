# AstroBench

**Open-source LLM benchmark using real astrophysics reasoning problems.**

AstroBench is the first open LLM evaluation suite built from quantitative astrophysics problems — drawn from cosmology, general relativity, stellar structure, exoplanet science, orbital mechanics, and data analysis. No trivia. No multiple choice. Pure quantitative reasoning with reference solutions graded automatically.

## Why does this exist?

Current LLM benchmarks (MMLU, GSM8K, HumanEval) measure fluency or coding, not genuine scientific reasoning. Astrophysicists evaluate models by whether they can do physics correctly, not just fluently. AstroBench makes that evaluation open, reproducible, and auditable.

## Problem coverage

- **18 hand-tagged problems** across 10 categories
- **Difficulty tiers**: easy / medium / hard
- **Graded**: substring + normalized exact + normalized-sequence similarity scoring, per-problem thresholds
- **Expendable via YAML**: drop `problems/<category>.yaml` to extend — schema validated on load

## Quick start

```bash
git clone https://github.com/Brighton-Lyrax/astrobench.git
cd astrobench
python3 -m venv .venv311 && source .venv311/bin/activate
pip install -e ".[dev]"

# 1. Inspect the problem set
astrobench problems

# 2. Run locally with Ollama
astrobench run --provider local --model llama3 --show

# 3. Run with OpenAI
astrobench run --provider openai --model gpt-4o --show -o result.json
```

Expected output:
```
[==========] 18 problems | 10 categories | Provider: local
[========]   6 / 18 passed  |  Score: 0.31
[cosmology  ] 12.5%
[stellar    ] 45.2%
[orbital    ] 10.0%
...
```

## CLI reference

```bash
astrobench problems [--category COSMOLOGY] [--difficulty hard]
astrobench run  --provider <local|openai|anthropic>  --model <id>
               [--categories A B]  [--difficulty easy|medium|hard]
               [-o result.json]  [--show]
astrobench categories
astrobench submit <url> [--provider ...] [--model ...]
```

## Benchmark design

| Dimension | AstroBench |
|---|---|
| Style | Open-response quantitative reasoning |
| Length | 50–1500 words per problem (multi-step derivations) |
| Grader | Exact-substring, normalized-exact, fuzz-match(retries) |
| Reference solutions | Curated references, not crowdsourced |
| Incentive to cheat | Very low — answers aren’t on StackExchange |
| Community extension | New categories via new YAML files |
| Runner | Local (ollama) + cloud (OpenAI, Anthropic) |

## Sponsor this project

AstroBench is community infrastructure. Consider sponsoring:

- **Model vendors** (OpenAI, Anthropic, Google, Mistral): verified benchmark coverage
- **Compute sponsors** (Lambda, RunPod, CoreWeave): hosted open leaderboard
- **Defense / national labs**: reproducible AI evaluation methodology
- **Individuals**: GitHub Sponsors for problem authoring + grader engineering

### Sponsor tier targets

| Tier | Target | Ask |
|---|---|---|
| Compute | Any GPU cloud | $2K free compute for hosted leaderboard |
| Benchmark grant | AI safety grant orgs | $5–10K for expanded problem set + paper release |
| Model access API | OpenAI, Anthropic | Priority model IDs for benchmark-curated runs |
| Ind. sponsors | Individual researchers | GitHub Sponsors / kofi |

### Brand hook

> "The benchmark your model has to actually *do* physics to pass."

Ideal sponsor pitches:
- Post a paper/poster at NeurIPS/ICML/MLSys on "LLM scientific reasoning gap"
- Host public leaderboard with hard-capped model IDs (cache-bust)
- Mention sponsors by tier in README; partner with versioned problem releases (v0.1 March 2026)

## Roadmap

- [ ] v0.2: Auto problem generator (LaTeX-to-problem YAML pipeline)
- [ ] v0.3: Structured multi-part answer rubric with partial credit
- [ ] v0.4: Public leaderboard with model-api keyless Cloudflare-protected submit
- [ ] v0.5: Derived supplements — HSF-style physics curriculum grading
- [ ] v1.0: Paper release at NeurIPS or NeurIPS workshops

## Contributing

```bash
git clone ...
git checkout -b add-gen-rel-problems
# Edit problems/astrophysics.yaml
astrobench problems --category gr
astrobench run --show -o local.json
git commit -m "Add 3 new GR derivation problems"
```

Schema can be extended with new keys (`author`, `license`, `source`, `tags`). See `problems/astrophysics.yaml`.

## License

MIT

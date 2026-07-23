# Contributing to AstroBench

## Adding new problems

1. Fork and clone the repo.
2. Edit or create files in `problems/`. Use the YAML schema in `problems/astrophysics.yaml` as a template.
3. Run validation:
   python3 -c "from astrobench.problems import load_problems; load_problems()"
4. Open a PR with a clear description of the new problems and their scientific source.

## Running the benchmark

```bash
astrobench problems
astrobench run --provider local --model llama3 --show
```

## Sponsor tokens

If you believe a sponsor wants to include a problem set derived from their internal corpora, open a sponsor-track issue first — funded problem vetting is required before merge.

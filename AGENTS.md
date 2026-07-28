# Project Rules

## Product

STD Statistical Studio is a browser-based statistical procedure engine.

The current product baseline is v0.6. Do not rebuild from or restore v0.5 unless the user explicitly requests a historical recovery.

## Architecture

- Final distribution must remain a standalone HTML file.
- The canonical source is `src/std_statistical_studio.html`.
- Development source may be modularized under `src/`.
- Do not migrate to React, Vue, Angular, or a backend.
- SheetJS is the only approved runtime dependency unless explicitly authorized.
- `python scripts/build.py` must keep `dist/std_statistical_studio.html` and `docs/index.html` synchronized.

## Statistical integrity

- Statistics must be deterministic JavaScript.
- Never convert missing values to zero.
- Never invent units or specifications.
- Every procedure requires input validation.
- Every procedure returns Result IR.
- Every analysis records excluded rows and warnings.
- Effect size and confidence interval should accompany hypothesis tests when applicable.
- Statistical significance is not causality.
- Capability analysis must disclose process stability status.
- Regression must include residual diagnostics.
- Post-hoc tests must adjust for multiple comparisons.

## LLM boundary

LLM may map schema, recommend procedure plans, localize labels, and narrate already-computed results.
LLM must not calculate statistics.

## Git

- Make small, focused commits.
- Run self-tests before commit.
- Do not mix unrelated procedures in one commit.
- Keep a working `dist/std_statistical_studio.html`.
- Update `docs/index.html` after a stable change.
- Do not publish a release when verification fails.

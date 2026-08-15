# STD Statistical Studio

STD Statistical Studio is a standalone, browser-based statistical procedure engine for Excel and CSV data.

It converts user columns to an STD schema, validates the selected statistical procedure, performs deterministic JavaScript calculations, renders charts, and records Result IR plus an Audit Trail.

## Live application

[Open STD Statistical Studio](https://kdeppaei.github.io/STD-Statistical-Studio/)

## Current baseline

- Product version: v0.6
- Engine version: 0.6.0
- Procedures: 39
- Distribution: one standalone HTML file
- Runtime framework: Vanilla HTML, CSS, and JavaScript
- Approved runtime dependency: SheetJS for Excel import

## Run locally

Open either file directly in a modern browser:

- `dist/std_statistical_studio.html`
- `docs/index.html`

CSV and built-in demonstration data work without SheetJS. Excel import requires access to the SheetJS CDN retained from the existing product.

## Build

```powershell
python scripts/build.py
```

The build copies the canonical v0.6 source to:

- `dist/std_statistical_studio.html`
- `docs/index.html`

and verifies that the two release files are byte-identical.

## Verify

```powershell
python tests/verify_release.py
```

In the application, run:

```text
Developer → Statistical Self-test
```

The current release reports `PASS 18 / FAIL 0`.

## Repository layout

```text
.
├─ AGENTS.md
├─ README.md
├─ CHANGELOG.md
├─ docs/
│  ├─ index.html
│  ├─ CODEX_STD_Statistical_Studio_v0_6_SPEC.md
│  ├─ STD_SCHEMA.md
│  ├─ STATISTICAL_RULES.md
│  └─ TEST_REPORT_v0_6.md
├─ src/
│  └─ std_statistical_studio.html
├─ scripts/
│  └─ build.py
├─ tests/
│  └─ verify_release.py
└─ dist/
   └─ std_statistical_studio.html
```

## Statistical and LLM boundaries

- Statistical values are calculated only by deterministic JavaScript.
- Missing values are never silently converted to zero.
- Specifications and units are never invented.
- Significant results are not narrated as causality.
- LLM output is limited to mapping, planning, localization, and narration of already-calculated results.

See [STATISTICAL_RULES.md](docs/STATISTICAL_RULES.md) for implementation notes and known numerical limitations.

## License

[MIT](LICENSE)

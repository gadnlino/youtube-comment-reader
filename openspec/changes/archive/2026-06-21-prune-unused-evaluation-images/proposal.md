## Why

The `evaluation/` tree contains **~176 PNG/JPEG artifacts** plus scattered CSV/JSON/TXT backing data, while the **actual monography (docx)** uses a wider set of figures and tables than the older `TEXTO_AVALIACAO_MONOGRAFIA.md` draft (which listed only 6 figures). The author has now uploaded **7 docx screenshots** (3 tables + 4 figures) confirming the real thesis asset set. Duplicate timestamp runs, superseded charts, and orphaned copies still inflate the repo. A **wide, author-confirmed keep-list** is needed before archiving everything else.

## What Changes

- Use a **docx-only keep-list**: the **7 assets from the thesis Word document** (Tabela 1–4, Figura 23–26 from author uploads)—**not** the older `TEXTO_AVALIACAO_MONOGRAFIA.md` figure set (`multiple_sets_*`, API PT charts, Tabela 2 as a protected asset).
- Keep-list closure includes backing **TXT/CSV/JSON** and **generating scripts** for those 7 docx assets only.
- **Archive all Portuguese-labelled figure outputs** (`*_pt.png`, `*pt_*.png`, old `*_pt` graph names)—do not keep PT visual assets.
- **Archive entire** `evaluation/02_graphs/english/` and `evaluation/02_graphs/portuguese/` folders (superseded by docx Fig 25–26); replace with a flat `02_graphs/` manifest layout for docx assets only.
- Build inventory of all images under `evaluation/`; classify as **keep**, **keep-backing**, or **prune**.
- Match uploaded screenshots to repo files (filename, visual layout, numeric values).
- **Archive** (not delete) prune candidates under `evaluation/06_archived/pruned_figures/<YYYY-MM>/`.
- Consolidate canonical copies under `evaluation/02_graphs/` with `MANIFEST.md` indexed by docx figure/table number.
- **Regenerate or import missing** assets (e.g. `e2e_test_results_table_20251102.png`, API PT charts from older draft if still needed).
- Update active guides to dereference pruned paths; **verify generating scripts still run** after cleanup.
- **Out of scope**: Hard-deleting archived assets; modifying the Word docx; pruning CSV/JSON that backs a kept table/figure.

## Capabilities

### New Capabilities

- `evaluation-figure-inventory`: Wide keep-list rules for monography figures, table exports, backing data, inventory format, reference tracing, archive placement, and post-cleanup script smoke checks.

### Modified Capabilities

- `evaluation-layout`: Curated assets under `02_graphs/` (figures + table PNGs + manifest); pruned assets under `06_archived/pruned_figures/`.

## Impact

- **Primary**: ~176 images; restructured `evaluation/02_graphs/` (no `english/`/`portuguese/` subfolders); new `02_graphs/MANIFEST.md`.
- **Archived**: all `*_pt*` figure PNGs (~30+ outside `06_archived/`); 10 files in `02_graphs/english/` + `portuguese/`; markdown-draft-only figures (`multiple_sets_*`, language-analysis PT charts).
- **Kept domains**: `model_analysis/`, `model_comparison/`, `api_load_testing/consolidated_graphs/`, `scripts/01_model_evaluation/`, `scripts/02_api_performance/`, `scripts/graphs/`.
- **Secondary**: Guides referencing old figure sets; duplicate timestamp PNGs across `scripts/graphs/` and `model_analysis/graphs/`.
- **Author input**: Seven uploaded docx screenshots (June 2026) seed the wide keep-list.

## 1. Inventory and planning

- [x] 1.1 Generate a deduplicated inventory of all `.py` files under `evaluation/` (compare basenames across `scripts/`, `model_analysis/scripts/`, `04_scripts/`, `api_load_testing/scripts/`, `model_comparison/scripts/`)
- [x] 1.2 Generate a list of all loose markdown/txt files directly under `evaluation/` and assign each a target folder per the design taxonomy
- [x] 1.3 Resolve open question on `model_comparison/scripts/` — decide merge vs catalog-only pointer and document decision in `design.md` Open Questions section

## 2. Shared path constants

- [x] 2.1 Create `evaluation/scripts/_paths.py` with constants for `EVAL_ROOT`, `REPORTS`, `GRAPHS`, `DATA`, `MODEL_RESULTS`, `MODEL_GRAPHS`, `API_RESULTS`, `API_GRAPHS`, `ARCHIVED`
- [x] 2.2 Add a short docstring at top of `_paths.py` explaining import usage from category scripts

## 3. Consolidate model evaluation scripts

- [x] 3.1 Copy unique scripts from `evaluation/model_analysis/scripts/` into `evaluation/scripts/01_model_evaluation/` (skip duplicates; keep newer/more complete version)
- [x] 3.2 Update merged scripts to import output paths from `_paths.py` instead of hard-coded `model_analysis/` strings where feasible
- [x] 3.3 Move `evaluation/model_analysis/scripts/` contents to `evaluation/06_archived/2025-11_duplicate_scripts/model_analysis_scripts/` with a README pointing to canonical location
- [x] 3.4 Leave a stub `evaluation/model_analysis/scripts/README.md` redirecting to `evaluation/scripts/01_model_evaluation/`

## 4. Consolidate API performance scripts

- [x] 4.1 Merge `evaluation/04_scripts/generators/` into `evaluation/scripts/02_api_performance/generators/`
- [x] 4.2 Merge `evaluation/04_scripts/tests/*.py` and `evaluation/api_load_testing/scripts/*.py` into `evaluation/scripts/02_api_performance/` (dedupe by basename)
- [x] 4.3 Update merged scripts to use `_paths.py` for `api_load_testing/` output directories
- [x] 4.4 Archive emptied `04_scripts/` and `api_load_testing/scripts/` under `evaluation/06_archived/legacy_scripts/` with redirect READMEs

## 5. Relocate analysis documents

- [x] 5.1 Move thesis/guide markdown from `evaluation/` root to `05_guides/` (`GUIA_*.md`, `TEXTO_AVALIACAO_MONOGRAFIA.md`, etc.)
- [x] 5.2 Move report-style markdown to `01_reports/` or `model_analysis/reports/` (`RELATORIO_*`, `DATASETS_*`, `ANALISE_*`, `ARGUMENTO_*`, `IMPACTO_*`, `API_*`)
- [x] 5.3 Move `MUDANCAS_FINAIS_RESUMO.txt` to `06_archived/`
- [x] 5.4 Merge or cross-link overlapping guides (`GUIA_SCRIPTS_AVALIACAO.md` vs `GUIA_COMPLETO_SCRIPTS_AVALIACAO.md` vs `scripts/README.md`) — keep one primary guide, archive redundant copy with pointer

## 6. Script catalog and entry-point docs

- [x] 6.1 Create `evaluation/scripts/CATALOG.md` with entries for all Python scripts (model, api-performance, api-e2e, model-comparison) plus root deployment shell scripts
- [x] 6.2 Rewrite `evaluation/README.md` to reflect hybrid layout, link to catalog, and remove stale references to pre-consolidation paths
- [x] 6.3 Update `evaluation/scripts/README.md` to align with canonical layout and link to `CATALOG.md`
- [x] 6.4 Add a "Repository layout" section to root `README.md` distinguishing `/scripts/` (deploy) from `/evaluation/scripts/` (analysis)
- [x] 6.5 Update `05_guides/ORGANIZACAO_ARQUIVOS.md` and `05_guides/ONDE_ESTA_TUDO.md` to match final structure (or archive if fully superseded by new README)

## 7. Fix cross-references

- [x] 7.1 Grep for `evaluation/(api_load_testing|04_scripts|model_analysis/scripts)/` across repo and update paths in `01_reports/`, `05_guides/`, and key model_analysis docs
- [x] 7.2 Update references in `packages/frontend/integration_test/` docs that cite old evaluation script paths
- [x] 7.3 Add "Former location" notes in `CATALOG.md` for any moved script paths cited in thesis documents

## 8. Verification

- [x] 8.1 Smoke-run one script from `evaluation/scripts/01_model_evaluation/` and confirm outputs land in `model_analysis/results/` or `graphs/`
- [x] 8.2 Smoke-run one script from `evaluation/scripts/02_api_performance/` and confirm outputs land in documented `api_load_testing/` folder
- [x] 8.3 Confirm no `.md` analysis files remain at `evaluation/` root except `README.md`
- [x] 8.4 Confirm no duplicate script basenames exist outside `06_archived/`

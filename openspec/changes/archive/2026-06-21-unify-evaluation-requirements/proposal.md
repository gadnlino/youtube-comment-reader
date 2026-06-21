## Why

Evaluation and analysis scripts under `evaluation/` depend on a scattered set of third-party Python packages, but dependency installation is documented inconsistently: inline `pip install` lists in READMEs, an embedded requirements block in methodology guides, and a single co-located `requirements.txt` under `model_comparison/scripts/`. Several guides already instruct `pip install -r requirements.txt` even though no canonical file exists at the evaluation level, which makes setup error-prone for reproducing thesis results.

## What Changes

- Add a **single canonical `evaluation/requirements.txt`** that covers **all** third-party dependencies used by canonical evaluation scripts—including heavy packages such as `datasets`, `transformers`, `accelerate`, and `torch`—so one install command is sufficient.
- **Audit imports** across canonical script trees (`evaluation/scripts/`, `evaluation/model_comparison/`, and referenced legacy paths) to derive the dependency set; exclude archived duplicates unless they introduce unique packages.
- **Pin versions** where the repo already documents them (e.g., model-comparison `accelerate==0.28.0`, methodology guide pins) and use compatible unpinned entries elsewhere when pins are not justified.
- **Group packages with comments** in the unified file (e.g., core ML, API load testing, Hugging Face stack) for readability—without splitting into separate install files.
- **Update READMEs and guides** across `evaluation/` so every active document points to `pip install -r evaluation/requirements.txt` (or the correct relative path) instead of inline package lists, broken `requirements.txt` references, or per-script install hints.
- **Deprecate or redirect** the nested `evaluation/model_comparison/scripts/requirements.txt` to the canonical file (symlink, re-export comment, or removal after migration)—avoid maintaining two divergent lists.
- **Out of scope**: Lambda production dependencies (`packages/lambdas/sentiment_analysis/requirements.txt`), Flutter E2E tooling, and re-running evaluations.

## Capabilities

### New Capabilities

- `evaluation-dependencies`: Canonical Python dependency manifest(s), install instructions, and documentation rules for all evaluation/analysis scripts under `evaluation/`.

### Modified Capabilities

<!-- No existing openspec/specs/ capabilities to modify -->

## Impact

- **Primary**: New `evaluation/requirements.txt`; `evaluation/model_comparison/scripts/requirements.txt`.
- **Documentation (active files to update):**
  - Entry points: `evaluation/README.md`, `evaluation/scripts/README.md`, `evaluation/model_comparison/README.md`, `evaluation/api_load_testing/README.md`, `evaluation/scripts/03_api_e2e/README.md`
  - Methodology guides: `evaluation/05_guides/MODEL_EVALUATION_METHODOLOGY.md`, `API_EVALUATION_METHODOLOGY.md`, `API_EVALUATION_GUIDE.md`, `E2E_FUNCTIONALITY_TESTING_METHODOLOGY.md`
  - Reports: `evaluation/01_reports/TESTING_METHODOLOGY.md`, `RELATORIO_VALIDACAO_INDEPENDENTE_SENTIMENT140.md`
  - Domain READMEs: `evaluation/scripts/02_api_performance/benchmarks/API_README.md`, `E2E_README.md`, `evaluation/api_load_testing/docs/README_MAX_TPS.md`
  - Legacy paths still cited: `evaluation/04_scripts/tests/API_README.md`, `E2E_README.md`
  - Shell/script hints: `run_max_tps_test.sh` error messages; Python error strings in validation scripts that say `pip install datasets`
  - Notebook: `evaluation/model_comparison/notebooks/youtube_comments_sentiment_analysis_comparison.ipynb` (`%pip install` cell)
  - **Archived** (`06_archived/`): one-line pointer only, no full rewrite
- **Related change**: Complements `organize-scripts-and-analysis` (layout/catalog) without requiring it to land first.
- **Developer workflow**: One venv + one `pip install -r evaluation/requirements.txt` for all evaluation scripts (including Hugging Face and load-test deps).

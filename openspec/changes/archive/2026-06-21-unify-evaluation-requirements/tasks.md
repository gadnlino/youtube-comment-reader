## 1. Dependency audit

- [x] 1.1 Grep third-party imports in `evaluation/scripts/`, `evaluation/model_comparison/`, and `evaluation/scripts/03_api_e2e/`; produce a deduplicated package list (exclude stdlib and local modules)
- [x] 1.2 Cross-check against inline install lists in `evaluation/scripts/README.md`, `evaluation/05_guides/MODEL_EVALUATION_METHODOLOGY.md`, and `evaluation/model_comparison/scripts/requirements.txt`; confirm full set includes Hugging Face stack (`datasets`, `transformers`, `accelerate`, `torch`)

## 2. Requirements file

- [x] 2.1 Create `evaluation/requirements.txt` with the full package set: pandas, numpy, scikit-learn, matplotlib, seaborn, scipy, requests, langdetect, kagglehub, nltk, textblob, locust, datasets, transformers, accelerate==0.28.0, torch — grouped with header comments and Python version note
- [x] 2.2 Replace `evaluation/model_comparison/scripts/requirements.txt` with a pointer comment to `../../requirements.txt` (no divergent package list)

## 3. Documentation updates — entry points

- [x] 3.1 Add a Setup section to `evaluation/README.md` (venv, `pip install -r requirements.txt`, large-deps note for `torch`, NLTK VADER download)
- [x] 3.2 Update `evaluation/scripts/README.md` — replace all inline `pip install` blocks with canonical install
- [x] 3.3 Update `evaluation/model_comparison/README.md` — point to `../requirements.txt`
- [x] 3.4 Update `evaluation/api_load_testing/README.md` — replace inline package lists and locust-only installs
- [x] 3.5 Update `evaluation/scripts/03_api_e2e/README.md` — replace `pip install requests` with canonical install

## 4. Documentation updates — guides and reports

- [x] 4.1 Update `evaluation/05_guides/MODEL_EVALUATION_METHODOLOGY.md` — fix `requirements.txt` references and embedded requirements block
- [x] 4.2 Update `evaluation/05_guides/API_EVALUATION_METHODOLOGY.md` — fix all `pip install -r requirements.txt` references
- [x] 4.3 Update `evaluation/05_guides/API_EVALUATION_GUIDE.md` — fix requirements path
- [x] 4.4 Update `evaluation/05_guides/E2E_FUNCTIONALITY_TESTING_METHODOLOGY.md` — replace `pip install requests`
- [x] 4.5 Update `evaluation/01_reports/TESTING_METHODOLOGY.md` — fix requirements path
- [x] 4.6 Update `evaluation/01_reports/RELATORIO_VALIDACAO_INDEPENDENTE_SENTIMENT140.md` — replace inline install lists

## 5. Documentation updates — domain READMEs, scripts, and notebook

- [x] 5.1 Update `evaluation/scripts/02_api_performance/benchmarks/API_README.md` and `E2E_README.md`
- [x] 5.2 Update `evaluation/api_load_testing/docs/README_MAX_TPS.md`
- [x] 5.3 Legacy `evaluation/04_scripts/tests/` READMEs already archived under `06_archived/2025-10_reorg_scripts/`; `04_scripts/README.md` points to canonical paths
- [x] 5.4 Update `run_max_tps_test.sh` error messages in `scripts/02_api_performance/` and `api_load_testing/scripts/` to reference `evaluation/requirements.txt`
- [x] 5.5 Update missing-dependency messages in `validate_with_airespucrs_pt.py` and `validate_with_tweets_pt.py`
- [x] 5.6 Update `%pip install` cell in `model_comparison/notebooks/youtube_comments_sentiment_analysis_comparison.ipynb`
- [x] 5.7 Add one-line pointer in `06_archived/2025-11_superseded_guides/README.md`

## 6. Verification

- [x] 6.1 Grep active `evaluation/` (exclude `06_archived/`) for stale `pip install` patterns; confirm only canonical path remains
- [x] 6.2 Fresh venv: `pip install -r evaluation/requirements.txt` succeeds; core imports verified (locust imports cleanly in isolation; avoid importing after torch in one process)
- [x] 6.3 Run `python -m py_compile` on one representative script per category (`01_model_evaluation`, `02_api_performance`, `model_comparison/scripts`)

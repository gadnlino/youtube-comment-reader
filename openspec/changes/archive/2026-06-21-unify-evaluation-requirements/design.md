## Context

Evaluation Python scripts live under several trees (`evaluation/scripts/`, `evaluation/model_comparison/`, legacy `evaluation/04_scripts/`). Setup instructions today are fragmented:

| Source | Install guidance |
|--------|------------------|
| `evaluation/scripts/README.md` | Three different inline `pip install` lists by category |
| `evaluation/05_guides/MODEL_EVALUATION_METHODOLOGY.md` | Embedded requirements block with pins; instructs `pip install -r requirements.txt` |
| `evaluation/05_guides/API_EVALUATION_METHODOLOGY.md` | `pip install -r requirements.txt` (file missing at cited path) |
| `evaluation/model_comparison/scripts/requirements.txt` | Partial list: pandas, scikit-learn, transformers, accelerate, kagglehub, datasets |
| Various READMEs | Ad-hoc `pip install locust`, `pip install datasets`, etc. |

Only one requirements file exists today (`evaluation/model_comparison/scripts/requirements.txt`). It omits packages used elsewhere (`requests`, `locust`, `scipy`, `langdetect`, `nltk`, `textblob`, `matplotlib`, `seaborn`).

Canonical script scope (per `organize-scripts-and-analysis` and `evaluation/scripts/CATALOG.md`):

- `evaluation/scripts/01_model_evaluation/` — model metrics, language analysis, validation
- `evaluation/scripts/02_api_performance/` — HTTP benchmarks, Locust load tests, graph generators
- `evaluation/model_comparison/scripts/` — TF-IDF, SVM, VADER, TextBlob comparisons
- `evaluation/scripts/03_api_e2e/` — minimal (`requests` only; covered by core set)

Archived scripts under `evaluation/06_archived/` are excluded from the audit except to confirm no unique packages are missed.

## Goals / Non-Goals

**Goals:**

- Provide `evaluation/requirements.txt` as the single primary install entry point.
- Cover **all** third-party imports for canonical scripts in one install—including `datasets`, `transformers`, `accelerate`, and `torch`.
- Align READMEs and methodology guides with the canonical path.
- Eliminate duplicate/conflicting requirement lists.

**Non-Goals:**

- Pin every package to exact versions unless already documented for reproducibility.
- Manage Lambda runtime deps (`packages/lambdas/sentiment_analysis/requirements.txt`).
- Manage Flutter/Dart test tooling.
- Automate dependency scanning in CI (could be a follow-up).
- Re-run evaluations to validate numerical outputs after dependency updates.

## Decisions

### 1. File location: `evaluation/requirements.txt`

**Decision:** Place the canonical file at `evaluation/requirements.txt` (not repo root, not nested under `scripts/`).

**Rationale:** Evaluation is a self-contained workspace; `evaluation/README.md` is the entry point. Keeps evaluation deps separate from app/Lambda deps.

**Alternatives considered:**
- Repo-root `requirements-dev.txt` — mixes evaluation with other tooling; rejected.
- Per-category files only (`requirements-model.txt`, etc.) — more installs for users; rejected as primary path.

### 2. Structure: single unified file

**Decision:** Use one file only — **`evaluation/requirements.txt`** — containing the full dependency set. No separate optional or extras file.

```bash
pip install -r evaluation/requirements.txt
```

Packages are grouped with comments for readability (e.g., `# Model evaluation`, `# API load testing`, `# Hugging Face / transformers`), but all are installed by default.

**Rationale:** Users reproducing thesis evaluation work should not need to discover or install a second requirements file. One command must run every canonical script.

**Alternatives considered:**
- Core + optional extras file — rejected; user preference is full install by default.
- PEP 621 `[project.optional-dependencies]` in `pyproject.toml` — no existing pyproject; out of scope.

### 3. Full dependency set (derived from import audit)

**Decision:** Unified file includes:

```
# Core data / ML / visualization
pandas
numpy
scikit-learn
matplotlib
seaborn
scipy

# HTTP / API testing
requests
locust

# NLP / sentiment
langdetect
kagglehub
nltk
textblob

# Hugging Face / transformer experiments
datasets
transformers
accelerate==0.28.0
torch
```

**Rationale:** Matches the union of imports across all canonical script trees. Stdlib modules (`json`, `csv`, `statistics`, etc.) are excluded.

**Note:** `statsmodels` appears in `MODEL_EVALUATION_METHODOLOGY.md` but is not imported by canonical scripts — omit unless audit finds usage; document omission in README.

### 4. Version pinning strategy

**Decision:** Mixed approach:

- **Pin** where already documented: e.g. `accelerate==0.28.0`; consider adopting methodology-guide pins for core ML stack if they still resolve on current Python 3.11+.
- **Leave unpinned** for widely used packages (`pandas`, `numpy`, `requests`, `locust`) unless pin conflicts arise during smoke test.

**Rationale:** Thesis reproducibility matters for model-comparison experiments; full pinning of every package is high maintenance and was never enforced repo-wide.

**Alternatives considered:**
- Full lock file (`requirements.lock` via pip-tools) — best reproducibility but heavy; defer unless requested.

### 5. Migrate `model_comparison/scripts/requirements.txt`

**Decision:** Replace contents with a one-line comment pointing to `../../requirements.txt`, or delete and update README only.

**Rationale:** Avoid two sources of truth. Prefer comment-only stub (not symlink) for cross-platform compatibility on Windows.

### 6. Documentation updates

**Decision:** Grep `evaluation/` for `pip install` and `requirements.txt`; update every **active** README and guide to use the canonical install. Replace inline package lists and broken `pip install -r requirements.txt` paths with:

```bash
pip install -r evaluation/requirements.txt
```

Use relative paths where the doc lives inside `evaluation/` (e.g. `../requirements.txt` from `scripts/README.md`, `../../requirements.txt` from nested READMEs).

**Files to update (checklist):**

| Category | Files |
|----------|-------|
| Entry points | `evaluation/README.md`, `scripts/README.md`, `model_comparison/README.md`, `api_load_testing/README.md`, `scripts/03_api_e2e/README.md` |
| Methodology | `05_guides/MODEL_EVALUATION_METHODOLOGY.md`, `API_EVALUATION_METHODOLOGY.md`, `API_EVALUATION_GUIDE.md`, `E2E_FUNCTIONALITY_TESTING_METHODOLOGY.md` |
| Reports | `01_reports/TESTING_METHODOLOGY.md`, `RELATORIO_VALIDACAO_INDEPENDENTE_SENTIMENT140.md` |
| Domain READMEs | `scripts/02_api_performance/benchmarks/API_README.md`, `E2E_README.md`, `api_load_testing/docs/README_MAX_TPS.md` |
| Legacy (still linked) | `04_scripts/tests/API_README.md`, `E2E_README.md` |
| Scripts / notebooks | `scripts/02_api_performance/run_max_tps_test.sh`, `api_load_testing/scripts/run_max_tps_test.sh`; error messages in `validate_with_airespucrs_pt.py`, `validate_with_tweets_pt.py`; `%pip` cell in `model_comparison/notebooks/youtube_comments_sentiment_analysis_comparison.ipynb` |

**Embedded requirements blocks:** In `MODEL_EVALUATION_METHODOLOGY.md`, replace the inline `requirements.txt` example block with a pointer to the canonical file (or sync content and note "see `evaluation/requirements.txt`").

**Archived:** `06_archived/` guides — add at most a one-line note that setup moved to `evaluation/requirements.txt`; do not rewrite historical content.

**Verification:** After edits, `rg 'pip install' evaluation/ --glob '!06_archived/**'` should show only the canonical command (plus venv/setup context), not ad-hoc package lists.

### 7. Verification approach

**Decision:** After creating files, run import smoke checks:

```bash
python -c "import pandas, numpy, sklearn, matplotlib, seaborn, scipy, requests, langdetect, kagglehub, nltk, textblob, locust, datasets, transformers, torch"
```

Optionally run `python -m py_compile` on one script per category. Full script execution requires API keys/data — out of scope for dependency validation.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Unpinned core deps drift and break scripts | Document Python version (3.10+); smoke-test imports after install; add pins incrementally if breaks reported |
| `torch` install is platform-specific and large (~2 GB) | Document in README that install may take several minutes; note CPU default from PyPI; GPU builds are user-managed |
| Guides still reference old inline lists after partial update | Grep for `pip install pandas` and `requirements.txt` across `evaluation/` during implementation |
| `nltk` requires post-install data download (VADER) | Document `python -m nltk.downloader vader_lexicon` in README (existing model_comparison scripts already assume this) |
| Locust not needed for model-only work | Acceptable; core file stays unified; users who never load-test still get locust installed (~small overhead) |

## Migration Plan

1. Audit canonical script imports (automated grep or script).
2. Create `evaluation/requirements.txt` with the full dependency set.
3. Stub or remove nested `model_comparison/scripts/requirements.txt`.
4. Update entry-point READMEs and primary methodology guides.
5. Grep for stale install instructions; fix high-traffic docs only.
6. Smoke-test `pip install` in a fresh venv.

**Rollback:** Delete new files and revert doc edits; no runtime impact on application code.

## Open Questions

1. **Python version floor:** Confirm minimum Python (likely 3.10 or 3.11) and note in `evaluation/README.md`.
2. **Adopt methodology pins wholesale:** Whether to copy pins from `MODEL_EVALUATION_METHODOLOGY.md` into the unified file or stay unpinned for flexibility.
3. **`torch` CPU vs GPU:** Default PyPI `torch` is CPU-only on most platforms; document if GPU-specific index URLs are needed for transformer notebooks.

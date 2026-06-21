# Step 1 — Scripts Audit

**Date:** 2026-06-21  
**Scope:** 73 `.py` files across 8 folders (+ 1 e2e script)  
**Machine-readable:** `audit-scripts.json`

## Summary

| Bucket | Count | Action |
|--------|------:|--------|
| Byte-identical duplicates | 21 pairs (42 files) | Archive non-canonical copy |
| Canonical (already in `evaluation/scripts/`) | 28 | Keep in place |
| Unique — must move to canonical tree | 17 | Move (see below) |
| Unique — keep co-located | 7 | `model_comparison/scripts/` — catalog only |
| E2E Python (legacy) | 1 | Move to `scripts/03_api_e2e/` or archive |

**No differing duplicate copies** were found (0 files need merge/diff review).

## Canonical priority (when duplicates exist)

1. `evaluation/scripts/01_model_evaluation/`
2. `evaluation/scripts/02_api_performance/`
3. `evaluation/scripts/03_api_e2e/`
4. `evaluation/model_comparison/scripts/` (never duplicated elsewhere)
5. `evaluation/04_scripts/tests/` or `generators/`
6. `evaluation/model_analysis/scripts/` ← archive duplicates
7. `evaluation/api_load_testing/scripts/` ← archive duplicates

---

## A. Model evaluation scripts

### Already canonical (`scripts/01_model_evaluation/`) — 18 files, KEEP

| Script | Purpose (from header) | Writes to |
|--------|----------------------|-----------|
| `analyze_video_language.py` | Video language profile | `model_analysis/results/`, `graphs/` |
| `compare_metrics_vs_benchmark.py` | Metrics vs benchmark | `model_analysis/results/` |
| `generate_confusion_matrix.py` | Confusion matrix PNG | `model_analysis/graphs/` |
| `generate_language_analysis_graphs.py` | Language analysis graphs (EN) | `model_analysis/graphs/` |
| `generate_language_analysis_graphs_pt.py` | Language analysis graphs (PT) | `model_analysis/graphs/` |
| `generate_metrics_comparison_table.py` | Metrics comparison table/chart | `model_analysis/graphs/` |
| `generate_sentiment_distribution_by_language.py` | Sentiment by language | `model_analysis/graphs/` |
| `generate_twitter_airline_graphs.py` | Twitter airline validation graphs | `scripts/01_model_evaluation/graphs/` |
| `generate_validation_graphs.py` | Independent validation graphs | `scripts/01_model_evaluation/graphs/` |
| `language_impact_analysis.py` | Linguistic bias analysis | `model_analysis/results/`, `graphs/` |
| `multilingual_sentiment_analysis.py` | Multilingual sentiment | `model_analysis/results/`, `graphs/` |
| `pre_filter_working_videos.py` | Pre-filter API-working videos | `model_analysis/data/` |
| `validate_model_accuracy_with_dataset.py` | Accuracy vs ground truth | `model_analysis/results/` |
| `validate_with_airespucrs_pt.py` | AiresPucrs PT validation | `scripts/01_model_evaluation/results/` |
| `validate_with_app_reviews_pt.py` | App reviews PT validation | `scripts/01_model_evaluation/results/` |
| `validate_with_imdb_reviews.py` | IMDB validation | `scripts/01_model_evaluation/results/` |
| `validate_with_tweets_pt.py` | Tweets PT validation | `scripts/01_model_evaluation/results/` |
| `validate_with_twitter_airline.py` | Twitter airline validation | `scripts/01_model_evaluation/results/` |

### Move from `model_analysis/scripts/` → `scripts/01_model_evaluation/` — 6 unique

| Script | Purpose | Writes to |
|--------|---------|-----------|
| `evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py` | Kaggle amitzala labeled eval | `model_analysis/results/`, `graphs/` |
| `generate_consolidated_distribution_analysis.py` | Consolidated distribution | `model_analysis/graphs/` |
| `plot_tfidf_lr_selection_vs_kaggle_amitzala.py` | Selection vs Kaggle comparison | `model_analysis/graphs/` |
| `validate_model_distribution.py` | Distribution validation (small set) | `model_analysis/results/` |
| `validate_model_distribution_multiple_sets.py` | Multi-set distribution validation | `model_analysis/results/` |
| `validate_model_distribution_vs_benchmark.py` | Distribution vs benchmark | `model_analysis/results/` |

### Archive from `model_analysis/scripts/` — 11 identical duplicates

`analyze_video_language.py`, `compare_metrics_vs_benchmark.py`, `generate_confusion_matrix.py`, `generate_language_analysis_graphs.py`, `generate_language_analysis_graphs_pt.py`, `generate_metrics_comparison_table.py`, `generate_sentiment_distribution_by_language.py`, `language_impact_analysis.py`, `multilingual_sentiment_analysis.py`, `pre_filter_working_videos.py`, `validate_model_accuracy_with_dataset.py`

---

## B. API performance scripts

### Already canonical (`scripts/02_api_performance/`) — 10 files, KEEP

| Script | Purpose |
|--------|---------|
| `common.py` | Shared HTTP/metrics utilities |
| `comments.py` | Comments endpoint tests |
| `videos.py` | Videos endpoint tests |
| `stability.py` | Temporal stability test |
| `run_all.py` | Run all API tests |
| `locust_test.py` | Basic Locust load test |
| `locust_max_tps.py` | Max TPS Locust test |
| `generate_consolidated_graphs.py` | Consolidated graphs |
| `generate_locust_graphs.py` | Locust result graphs |
| `generate_e2e_test_table.py` | E2E results table |

### Move from `04_scripts/` → `scripts/02_api_performance/` — 10 unique

| Script | Target subfolder | Writes to |
|--------|------------------|-----------|
| `generate_academic_graphs.py` | `generators/` | `api_load_testing/*.png` (hard-coded) |
| `generate_academic_graphs_pt.py` | `generators/` | `api_load_testing/*_pt.png` (hard-coded) |
| `batch_size_analysis.py` | `benchmarks/` | `api_load_testing/batch_size_*` |
| `extended_benchmark.py` | `benchmarks/` | `api_load_testing/` |
| `heavy_load_test.py` | `benchmarks/` | `api_load_testing/` |
| `multi_video_benchmark.py` | `benchmarks/` | `api_load_testing/multi_video_*` |
| `performance_benchmark.py` | `benchmarks/` | `api_load_testing/` |
| `quick_test.py` | `benchmarks/` | `api_load_testing/` |
| `locustfile.py` | `benchmarks/` | Locust output |
| `config_template.py` | `benchmarks/` | (config only) |

### Archive from `api_load_testing/scripts/` — 10 identical duplicates

All files in that folder duplicate `scripts/02_api_performance/`.

---

## C. Model comparison — KEEP IN PLACE (7 files)

Co-located with notebooks and results. Catalog pointer only; do not move.

| Script | Purpose |
|--------|---------|
| `comprehensive_model_comparison.py` | Full model comparison run |
| `vader_classification_report.py` | VADER report |
| `textblob_classification_report.py` | TextBlob report |
| `tfidf_logistic_classification_report.py` | TF-IDF+LR report |
| `svm_classification_report.py` | SVM report |
| `fix_nltk_ssl.py` | NLTK SSL fix utility |
| `nltk_setup.py` | NLTK setup utility |

---

## D. E2E Python (legacy)

| File | Current location | Verdict |
|------|------------------|---------|
| `e2e_functionality_test.py` | `e2e_functionality_testing/` | Move to `scripts/03_api_e2e/` **or** archive — Flutter E2E is canonical in `packages/frontend/integration_test/` |

Referenced incorrectly as `04_scripts/tests/e2e_functionality_test.py` in some docs (file is not there today).

---

## E. Post-consolidation script tree

```
evaluation/scripts/
├── _paths.py                          # NEW — shared path constants
├── CATALOG.md                         # NEW — human index
├── README.md                          # UPDATE — single doc entry
├── 01_model_evaluation/               # 24 scripts (18 + 6 moved)
├── 02_api_performance/                # 10 scripts (canonical Locust suite)
│   ├── generators/                    # 2 from 04_scripts/generators
│   └── benchmarks/                    # 8 from 04_scripts/tests
├── 03_api_e2e/                        # e2e_functionality_test.py (optional)
└── (model_comparison stays at evaluation/model_comparison/scripts/)
```

**Do not move** PNG/CSV/JSON outputs in v1 — scripts hard-code `api_load_testing/` and `model_analysis/` output paths.

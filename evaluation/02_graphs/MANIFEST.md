# Thesis figure inventory (docx-only)

Canonical paths for the **seven assets** embedded in the thesis Word document (Tabela 1–4, Figura 23–26). Markdown-draft figures (`multiple_sets_*`, language-analysis charts, PT API charts) are **not** on this list and were archived to `evaluation/06_archived/pruned_figures/2026-06/`.

Machine-readable inventory: [`inventory.json`](inventory.json).

## Keep-list

| Docx | Type | Canonical path | Generator | Backing data |
|------|------|----------------|-----------|--------------|
| **Tabela 1** | Word table (TXT export) | [`../model_comparison/results/comprehensive_model_comparison.txt`](../model_comparison/results/comprehensive_model_comparison.txt) | [`../model_comparison/scripts/comprehensive_model_comparison.py`](../model_comparison/scripts/comprehensive_model_comparison.py) | Model comparison inputs under `evaluation/model_comparison/` |
| **Tabela 3** | Word table (Locust metrics) | Regenerate via generator; reference PNG archived | [`../scripts/02_api_performance/generate_consolidated_graphs.py`](../scripts/02_api_performance/generate_consolidated_graphs.py) | Locust CSV/JSON under `evaluation/api_load_testing/` |
| **Tabela 4** | Word table (E2E PNG) | [`tables/tabela-4_e2e_test_results_table.png`](tables/tabela-4_e2e_test_results_table.png) | [`../scripts/02_api_performance/generate_e2e_test_table.py`](../scripts/02_api_performance/generate_e2e_test_table.py) | Embedded `TESTES` list in script (no external CSV) |
| **Figura 23** | Per-class metrics chart | [`figures/figura-23_metrics_per_class_youtube_comments_with_labeled.png`](figures/figura-23_metrics_per_class_youtube_comments_with_labeled.png) | [`../scripts/01_model_evaluation/evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py`](../scripts/01_model_evaluation/evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py) | [`../model_analysis/results/metrics_tfidf_lr_amitzala_youtube-comments-with-labeled_20260317_230701.csv`](../model_analysis/results/metrics_tfidf_lr_amitzala_youtube-comments-with-labeled_20260317_230701.csv) |
| **Figura 24** | Selection vs Kaggle bar chart | [`figures/figura-24_tfidf_lr_selection_vs_kaggle_amitzala.png`](figures/figura-24_tfidf_lr_selection_vs_kaggle_amitzala.png) | [`../scripts/01_model_evaluation/plot_tfidf_lr_selection_vs_kaggle_amitzala.py`](../scripts/01_model_evaluation/plot_tfidf_lr_selection_vs_kaggle_amitzala.py) | Kaggle AmitZala CSV + selection metrics (see script docstring) |
| **Figura 25** | Locust dashboard (part 1) | [`figures/figura-25_consolidated_graphs_part1.png`](figures/figura-25_consolidated_graphs_part1.png) | [`../scripts/02_api_performance/generate_consolidated_graphs.py`](../scripts/02_api_performance/generate_consolidated_graphs.py) | Locust run data under `evaluation/api_load_testing/` |
| **Figura 26** | Locust dashboard (part 2) | [`figures/figura-26_consolidated_graphs_part2.png`](figures/figura-26_consolidated_graphs_part2.png) | same as Figura 25 | same as Figura 25 |

### Source lineage (canonical copies)

| Docx figure | Original repo filename (archived after copy) |
|-------------|---------------------------------------------|
| Figura 23 | `metrics_per_class_tfidf_lr_amitzala_youtube-comments-with-labeled_20260317_230701.png` |
| Figura 24 | `tfidf_lr_selection_vs_kaggle_amitzala_20260621_172335.png` (newest of two runs; older copy archived) |
| Figura 25 / 26 | `consolidated_graphs_part1.png`, `consolidated_graphs_part2.png` |
| Tabela 4 | Regenerated 2026-06-21 (`generate_e2e_test_table.py`); replaces missing `e2e_test_results_table_20251102.png` |

## Regeneration

From repo root, with `pip install -r evaluation/requirements.txt`:

```bash
# Tabela 1 (TXT)
python evaluation/model_comparison/scripts/comprehensive_model_comparison.py

# Tabela 3–4, Figura 25–26
python evaluation/scripts/02_api_performance/generate_consolidated_graphs.py
python evaluation/scripts/02_api_performance/generate_e2e_test_table.py

# Figura 23 (requires labeled YouTube comments dataset + trained model)
python evaluation/scripts/01_model_evaluation/evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py

# Figura 24 (requires Kaggle AmitZala CSV paths configured in script)
python evaluation/scripts/01_model_evaluation/plot_tfidf_lr_selection_vs_kaggle_amitzala.py
```

After regeneration, copy new PNG outputs into `figures/` or `tables/` using the canonical filenames above.

## Excluded from keep-list (archived)

- All `*_pt*` figure PNGs and `02_graphs/english/`, `02_graphs/portuguese/` (10 curated EN/PT performance figures)
- Markdown-draft figures: `multiple_sets_*`, language-analysis charts (`language_neutral_bias_*`, etc.)
- Sentiment140 / IMDB validation report charts
- Duplicate timestamp runs (e.g. older `tfidf_lr_selection_vs_kaggle_amitzala_*`)

Archive location: [`../06_archived/pruned_figures/2026-06/`](../06_archived/pruned_figures/2026-06/) — see [`README.md`](../06_archived/pruned_figures/2026-06/README.md).

## Verification (2026-06-21)

- All five generator scripts pass `py_compile`.
- `generate_e2e_test_table.py` smoke-run produces Tabela 4 PNG (embedded test data).
- Other generators require external inputs documented above; canonical PNGs preserved under `figures/` and `tables/`.
- Author-uploaded docx screenshots matched by content: Figura 24 (59.5% vs 52.9%), Figura 25/26 (TPS / success / response panels), Figura 23 (per-class bars), Tabela 4 (8 E2E rows).

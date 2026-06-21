## 1. Docx-only keep-list

- [x] 1.1 Seed `evaluation/02_graphs/MANIFEST.md` from docx assets only: Tabela 1–4, Figura 23–26 (see design.md)
- [x] 1.2 Add keep-backing closure: CSV/JSON/TXT + generator scripts for those seven assets only
- [x] 1.3 Resolve duplicate timestamps (keep latest `tfidf_lr_selection_vs_kaggle_amitzala_*`; mark older copies prune)
- [x] 1.4 Mark all `*_pt*` figure PNGs and markdown-draft figures (`multiple_sets_*`, language-analysis PT charts) as prune

## 2. Inventory

- [x] 2.1 Enumerate all images under `evaluation/` with keep / keep-backing / prune status
- [x] 2.2 Enumerate backing data files linked from manifest
- [x] 2.3 Write `evaluation/02_graphs/inventory.json` (or markdown table) with docx ref, references, generator columns
- [x] 2.4 Flag missing assets: `e2e_test_results_table_20251102.png`, API PT PNGs (if on keep-list)

## 3. Regenerate or import missing assets

- [x] 3.1 Run `generate_e2e_test_table.py` for Tabela 4 PNG (or import from author upload)
- [x] 3.2 Confirm Figura 23 canonical copy: `metrics_per_class_tfidf_lr_amitzala_youtube-comments-with-labeled_20260317_230701.png`
- [x] 3.3 Confirm Figura 25/26: `consolidated_graphs_part1.png`, `consolidated_graphs_part2.png` (sync copies under `scripts/02_api_performance/graphs/` if needed)

## 4. Consolidate canonical copies

- [x] 4.1 Copy kept figures to `evaluation/02_graphs/figures/` and table PNGs to `evaluation/02_graphs/tables/`
- [x] 4.2 Finalize `MANIFEST.md` with docx numbers, paths, generators, backing data
- [x] 4.3 Update `TEXTO_AVALIACAO_MONOGRAFIA.md` if paths change (optional alignment with docx numbering)

## 5. Archive prune candidates

- [x] 5.1 Create `evaluation/06_archived/pruned_figures/2026-06/` + README
- [x] 5.2 `git mv` prune-candidate PNGs (outside keep closure) into archive with inventory sidecar
- [x] 5.3 Archive entire `evaluation/02_graphs/english/` and `evaluation/02_graphs/portuguese/` folders (10 files)
- [x] 5.4 Archive all prune-candidate `*_pt*` figure PNGs under `evaluation/` (exclude `06_archived/` already archived)

## 6. Guides and references

- [x] 6.1 Update active guides referencing pruned figures (`LANGUAGE_ANALYSIS_GRAPHS_GUIDE.md`, `FINAL_MULTILINGUAL_EVALUATION_SUMMARY.md`, etc.)
- [x] 6.2 Grep active `evaluation/` for broken image links post-archive

## 7. Script verification

- [x] 7.1 `py_compile` on kept generators: `plot_tfidf_lr_selection_vs_kaggle_amitzala.py`, `evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py`, `comprehensive_model_comparison.py`, `generate_consolidated_graphs.py`, `generate_e2e_test_table.py`
- [x] 7.2 Smoke-run generators where inputs exist (or document required inputs in manifest)
- [x] 7.3 Author review: uploaded screenshots match canonical paths in manifest

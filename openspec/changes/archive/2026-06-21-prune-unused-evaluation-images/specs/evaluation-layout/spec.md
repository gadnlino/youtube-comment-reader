## ADDED Requirements

### Requirement: Curated monography assets live under 02_graphs

Kept docx figures and table PNG exports SHALL be indexed in `evaluation/02_graphs/MANIFEST.md` with flat subfolders `figures/` and `tables/`. The legacy subfolders `02_graphs/english/` and `02_graphs/portuguese/` SHALL be archived in full.

#### Scenario: Docx figure canonical path

- **WHEN** Figura 24 is on the keep-list
- **THEN** `MANIFEST.md` SHALL document its path under `evaluation/02_graphs/figures/` (or the single canonical domain path if not copied)

#### Scenario: Docx table sources documented

- **WHEN** Tabela 1 (model comparison) is on the keep-list
- **THEN** `MANIFEST.md` SHALL link to `model_comparison/results/comprehensive_model_comparison.txt` and the generating script

### Requirement: Pruned figures archive location

Bulk-removed evaluation images SHALL be stored under `evaluation/06_archived/pruned_figures/<YYYY-MM>/` with README linking to `02_graphs/MANIFEST.md`.

#### Scenario: Archived duplicate timestamp run

- **WHEN** an older `tfidf_lr_selection_vs_kaggle_amitzala_*` PNG is pruned
- **THEN** it SHALL appear under `pruned_figures/` with inventory noting which canonical copy replaced it

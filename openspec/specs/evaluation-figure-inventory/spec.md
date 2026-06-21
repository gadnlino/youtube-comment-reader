# evaluation-figure-inventory

Docx-only thesis figure keep-list, inventory, and prune/archive rules for evaluation PNG assets.

## Requirements

### Requirement: Docx-only keep-list exists

The repository SHALL maintain a keep-list at `evaluation/02_graphs/MANIFEST.md` covering **only** the seven thesis docx assets (Tabela 1–4, Figura 23–26), their backing data files, and generating scripts—not markdown-draft figures or Portuguese-labelled figure outputs.

#### Scenario: Keep-list matches uploaded docx set

- **WHEN** the author confirms the docx asset set
- **THEN** the keep-list SHALL contain exactly those seven logical assets plus backing/generator closure

#### Scenario: Markdown draft figures excluded

- **WHEN** `TEXTO_AVALIACAO_MONOGRAFIA.md` references figures not in the docx (e.g. `multiple_sets_*`, API PT charts)
- **THEN** those PNGs SHALL NOT be on the keep-list and MAY be archived

#### Scenario: Portuguese figure outputs excluded

- **WHEN** an evaluation PNG filename contains a Portuguese asset marker (e.g. `_pt.png`, `_pt_`, `viés_linguistico_pt`)
- **THEN** it SHALL NOT be on the keep-list unless it is the canonical copy of a docx figure (none currently are)

#### Scenario: Backing data closure

- **WHEN** a kept figure or table is reproduced from CSV, JSON, or TXT
- **THEN** those source files SHALL be marked `keep-backing` and MUST NOT be archived

### Requirement: Full asset inventory before pruning

Before pruning, an inventory SHALL enumerate every image under `evaluation/` plus backing files linked from the keep-list, with columns: path, type (figure | table-png | data | script), keep status, docx ref, references, generator.

#### Scenario: Duplicate timestamp copies

- **WHEN** multiple PNGs represent the same logical figure (e.g. two `tfidf_lr_selection_vs_kaggle_amitzala_*` runs)
- **THEN** the inventory SHALL designate one canonical copy as keep and mark others prune

#### Scenario: Table PNG missing from disk

- **WHEN** Tabela 4 (E2E results table image) is on the keep-list but absent from the repo
- **THEN** the inventory SHALL mark it missing and block bulk prune until regenerated or imported

### Requirement: Upload matching uses content not filename alone

Matching uploaded screenshots to repo files SHALL use docx figure/table numbers, chart titles, and numeric values—not filename alone.

#### Scenario: Figura 24 matched by metrics

- **WHEN** an upload shows selection 59.5% vs Kaggle evaluation 52.9%
- **THEN** the keep-list SHALL reference `plot_tfidf_lr_selection_vs_kaggle_amitzala.py` output and related CSV/TXT sources

#### Scenario: Figura 25 matched by dashboard layout

- **WHEN** an upload shows three panels titled TPS por Usuários, Taxa de Sucesso, Tempo de Resposta
- **THEN** the keep-list SHALL reference `consolidated_graphs_part1.png` from `generate_consolidated_graphs.py`

### Requirement: Pruned assets are archived not deleted

Assets not on the wide keep-list or its backing/generator closure SHALL be moved to `evaluation/06_archived/pruned_figures/<YYYY-MM>/`. Hard deletion SHALL require explicit author confirmation.

#### Scenario: Bulk archive excludes keep closure

- **WHEN** pruning executes
- **THEN** no kept figure, table PNG, backing CSV/JSON/TXT, or generator script is moved to archive

### Requirement: Generating scripts remain runnable after cleanup

Scripts that produce kept assets SHALL still compile and run (or document required inputs) after the archive pass.

#### Scenario: Post-cleanup smoke test

- **WHEN** pruning completes
- **THEN** `plot_tfidf_lr_selection_vs_kaggle_amitzala.py`, `generate_consolidated_graphs.py`, `generate_e2e_test_table.py`, `comprehensive_model_comparison.py`, and `evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py` SHALL pass `py_compile` and documented minimal run checks

### Requirement: Active guides updated after prune

Active guides outside `06_archived/` that reference pruned figure paths SHALL be updated to point to canonical `02_graphs/` paths, regeneration instructions, or an archive note.

#### Scenario: Guide cited archived language-analysis chart

- **WHEN** a guide links to a PNG moved to `pruned_figures/`
- **THEN** the guide SHALL be updated within the same change

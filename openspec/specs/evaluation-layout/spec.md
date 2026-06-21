# evaluation-layout

Canonical directory structure and placement rules for evaluation artifacts.

## Requirements

### Requirement: Canonical evaluation directory structure

The repository SHALL organize all evaluation artifacts under `evaluation/` using a hybrid layout: numbered folders for curated artifacts and domain folders for workflow outputs.

#### Scenario: Researcher opens evaluation root

- **WHEN** a contributor lists the `evaluation/` directory
- **THEN** they SHALL find `01_reports/`, `02_graphs/`, `03_data/`, `05_guides/`, `06_archived/`, `scripts/`, `model_analysis/`, `model_comparison/`, and `api_load_testing/` with roles documented in `evaluation/README.md`

#### Scenario: No loose analysis reports at evaluation root

- **WHEN** the organization change is complete
- **THEN** no thesis or analysis markdown files (except `README.md`) SHALL remain directly under `evaluation/`; they SHALL live in `01_reports/`, `05_guides/`, or domain `reports/` subfolders

#### Scenario: Researcher opens curated thesis figures

- **WHEN** a contributor reads `evaluation/README.md` for the role of `02_graphs/`
- **THEN** it SHALL describe `MANIFEST.md`, `figures/`, and `tables/` as the docx keep-list layout and SHALL NOT describe active `english/` or `portuguese/` subfolders as current locations

### Requirement: Numbered evaluation subfolders document themselves

Folders `evaluation/01_reports/`, `evaluation/02_graphs/`, `evaluation/03_data/`, and `evaluation/05_guides/` SHALL each include a `README.md` summarizing contents and pointing to key entry documents.

#### Scenario: Researcher opens reports folder

- **WHEN** they list `evaluation/01_reports/`
- **THEN** they SHALL find a README naming `FINAL_EVALUATION_REPORT.md`, `INDEX.md`, and `TESTING_METHODOLOGY.md` as primary entry points

### Requirement: Single canonical location for runnable evaluation scripts

All runnable Python evaluation scripts SHALL reside under `evaluation/scripts/`, categorized as `01_model_evaluation/`, `02_api_performance/`, or `03_api_e2e/`.

#### Scenario: Contributor searches for a model validation script

- **WHEN** they look for scripts such as `compare_metrics_vs_benchmark.py` or `validate_model_accuracy_with_dataset.py`
- **THEN** exactly one canonical copy SHALL exist under `evaluation/scripts/01_model_evaluation/` (not duplicated under `model_analysis/scripts/` or `04_scripts/`)

#### Scenario: Contributor searches for API load-test scripts

- **WHEN** they look for scripts such as `locust_max_tps.py` or `run_all.py`
- **THEN** exactly one canonical copy SHALL exist under `evaluation/scripts/02_api_performance/` (not duplicated under `api_load_testing/scripts/` or `04_scripts/tests/`)

### Requirement: Output folders remain domain-scoped

Generated results SHALL remain in domain output directories: `model_analysis/{results,graphs,reports,data}/`, `api_load_testing/{results,graphs,consolidated_graphs}/`, and `model_comparison/{results,scripts}/` as applicable, with paths documented in the script catalog.

#### Scenario: Model script writes results

- **WHEN** a model evaluation script completes successfully
- **THEN** JSON/CSV outputs SHALL be written to `evaluation/model_analysis/results/` (or a subdirectory documented in the catalog) and graphs to `evaluation/model_analysis/graphs/`

#### Scenario: API performance script writes results

- **WHEN** an API performance script completes successfully
- **THEN** raw test outputs SHALL be written under `evaluation/api_load_testing/results/` or a documented run folder under `api_load_testing/`

### Requirement: Legacy material is archived not deleted

Superseded folders and duplicate script copies SHALL be moved to `evaluation/06_archived/` with a README describing what replaced them.

#### Scenario: Legacy script folder retired

- **WHEN** `04_scripts/` or duplicate script directories are superseded
- **THEN** their contents SHALL appear under `evaluation/06_archived/legacy_scripts/` (or similar) with a pointer README to the canonical `evaluation/scripts/` location

### Requirement: Deployment scripts are distinct from evaluation scripts

Deployment shell scripts SHALL live under `infra/` and SHALL be referenced separately from evaluation Python scripts in repository documentation. Root `/scripts/` SHALL NOT remain the canonical deploy location.

#### Scenario: New contributor distinguishes script folders

- **WHEN** they read the root `README.md`
- **THEN** they SHALL see a clear distinction between `infra/` (deploy/build) and `evaluation/scripts/` (research and testing)

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

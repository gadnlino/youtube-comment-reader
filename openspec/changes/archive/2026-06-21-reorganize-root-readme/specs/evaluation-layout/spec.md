## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: Numbered evaluation subfolders document themselves

Folders `evaluation/01_reports/`, `evaluation/02_graphs/`, `evaluation/03_data/`, and `evaluation/05_guides/` SHALL each include a `README.md` summarizing contents and pointing to key entry documents.

#### Scenario: Researcher opens reports folder

- **WHEN** they list `evaluation/01_reports/`
- **THEN** they SHALL find a README naming `FINAL_EVALUATION_REPORT.md`, `INDEX.md`, and `TESTING_METHODOLOGY.md` as primary entry points

## MODIFIED Requirements

### Requirement: Deployment scripts are distinct from evaluation scripts

Deployment shell scripts SHALL live under `infra/` and SHALL be referenced separately from evaluation Python scripts in repository documentation. Root `/scripts/` SHALL NOT remain the canonical deploy location.

#### Scenario: New contributor distinguishes script folders

- **WHEN** they read the root `README.md`
- **THEN** they SHALL see a clear distinction between `infra/` (deploy/build) and `evaluation/scripts/` (research and testing)

# script-catalog

Discoverable index of runnable evaluation and deployment scripts.

## Requirements

### Requirement: Script catalog document exists

The repository SHALL include `evaluation/scripts/CATALOG.md` listing every runnable evaluation script and root deployment script with category, purpose, working directory, primary inputs, and output locations.

#### Scenario: Contributor finds how to run model validation

- **WHEN** they open `evaluation/scripts/CATALOG.md`
- **THEN** they SHALL find an entry for model evaluation scripts including the command to run and where JSON/PNG outputs are written

#### Scenario: Contributor finds deployment scripts

- **WHEN** they open `evaluation/scripts/CATALOG.md` or the root README layout section
- **THEN** they SHALL find entries for `scripts/build-and-push-sentiment-image.sh` and `scripts/deploy-with-sentiment.sh` under a "Deployment" category separate from evaluation Python scripts

### Requirement: Catalog is linked from evaluation entry point

`evaluation/README.md` SHALL link to `evaluation/scripts/CATALOG.md` and `evaluation/scripts/README.md` as the primary navigation for runnable scripts.

#### Scenario: Researcher starts from evaluation README

- **WHEN** they open `evaluation/README.md`
- **THEN** a "Scripts" or equivalent section SHALL link to the catalog within one click

### Requirement: Each catalog entry includes minimum metadata

Every catalog entry SHALL include: script filename, category (`model`, `api-performance`, `api-e2e`, `deployment`, or `model-comparison`), one-line purpose, recommended working directory, and output directory.

#### Scenario: Catalog entry completeness check

- **WHEN** a reviewer inspects any row in `CATALOG.md`
- **THEN** all five metadata fields (filename, category, purpose, working directory, output directory) SHALL be present

### Requirement: Deprecated script paths are documented

When a script moves from a legacy path, the catalog SHALL record the old path under a "Former location" note until the next major documentation revision.

#### Scenario: User follows old documentation path

- **WHEN** they consult `CATALOG.md` after a script consolidation
- **THEN** they SHALL find the former path (e.g., `evaluation/model_analysis/scripts/compare_metrics_vs_benchmark.py`) mapped to the canonical path (`evaluation/scripts/01_model_evaluation/compare_metrics_vs_benchmark.py`)

### Requirement: Flutter E2E tests are indexed externally

The catalog SHALL include a section pointing to `packages/frontend/integration_test/` for Flutter integration tests, with a link to that folder's README if present.

#### Scenario: Contributor needs frontend E2E scripts

- **WHEN** they search the catalog for end-to-end UI tests
- **THEN** they SHALL find a dedicated section referencing `packages/frontend/integration_test/` rather than a duplicate under `evaluation/`

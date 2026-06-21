## MODIFIED Requirements

### Requirement: Script catalog document exists

The repository SHALL include `evaluation/scripts/CATALOG.md` listing every runnable evaluation script and deployment script with category, purpose, working directory, primary inputs, and output locations.

#### Scenario: Contributor finds how to run model validation

- **WHEN** they open `evaluation/scripts/CATALOG.md`
- **THEN** they SHALL find an entry for model evaluation scripts including the command to run and where JSON/PNG outputs are written

#### Scenario: Contributor finds deployment scripts

- **WHEN** they open `evaluation/scripts/CATALOG.md` or the root README layout section
- **THEN** they SHALL find an entry for `infra/deploy-with-sentiment.sh` under a "Deployment" category separate from evaluation Python scripts

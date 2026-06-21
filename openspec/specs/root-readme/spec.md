# root-readme

Structure and content rules for the repository root orientation page.

## Requirements

### Requirement: Root README identifies the project

The repository root `README.md` SHALL open with the project name and a one-sentence description of the YouTube Comment Reader system (mobile app, sentiment API backend, and evaluation material for academic assessment).

#### Scenario: New visitor opens the repository on GitHub

- **WHEN** a reader views the root `README.md`
- **THEN** they SHALL see what the product does before any folder table or command block

### Requirement: Root README provides audience-based quick start

The root `README.md` SHALL include a "Começar rápido" (or equivalent) section with separate entry points for: Flutter application setup, mobile E2E tests, backend deployment, and Python evaluation setup.

#### Scenario: Developer wants to run the mobile app

- **WHEN** they read the quick-start section
- **THEN** they SHALL find a path to `packages/frontend/` with at least `flutter pub get` or a link to that package README

#### Scenario: Researcher wants to run evaluation scripts

- **WHEN** they read the quick-start section
- **THEN** they SHALL find `pip install -r evaluation/requirements.txt` and a link to `evaluation/README.md`

#### Scenario: Operator wants to deploy the backend

- **WHEN** they read the quick-start section
- **THEN** they SHALL find `npm run deploy:dev` and a link to `infra/README.md`

### Requirement: Root README maps top-level directories to folder READMEs

The root `README.md` SHALL contain a repository map table where each row links to or names the folder's `README.md` for: `packages/`, `infra/`, `stacks/`, `evaluation/`, and `openspec/`.

#### Scenario: Contributor distinguishes deploy from evaluation scripts

- **WHEN** they read the repository map
- **THEN** `infra/` SHALL be described as deployment/infrastructure and `evaluation/scripts/` as research Python scripts (root `/scripts/` SHALL NOT appear as a current path)

### Requirement: Root README indexes documentation instead of duplicating it

The root `README.md` SHALL link to folder READMEs and key indexes (`evaluation/02_graphs/MANIFEST.md`, `evaluation/scripts/CATALOG.md`) rather than copying full folder inventories.

#### Scenario: Reader needs thesis figure locations

- **WHEN** they follow documentation links from the root README
- **THEN** they SHALL reach folder READMEs or `MANIFEST.md` without stale references to archived `02_graphs/english/` or `02_graphs/portuguese/` folders

### Requirement: Root README length stays scannable

The root `README.md` SHALL remain a single orientation page: target length under 120 lines and SHALL NOT embed full per-folder detail or the complete script catalog.

#### Scenario: Maintainer reviews README scope

- **WHEN** the reorganized README is complete
- **THEN** detailed folder contents SHALL live in child `README.md` files linked from the root

## ADDED Requirements

### Requirement: Major folders have orientation READMEs

Each major repository folder listed in the root README map SHALL contain a `README.md` that explains the folder's purpose, its immediate contents, and links to child or related READMEs.

#### Scenario: Contributor opens packages tree

- **WHEN** they list `packages/`
- **THEN** they SHALL find `packages/README.md` describing `frontend/` and `lambdas/` with links to each package README

#### Scenario: Contributor opens infrastructure folder

- **WHEN** they list `infra/`
- **THEN** they SHALL find `infra/README.md` documenting deployment scripts and prerequisites (Docker, AWS CLI, model file)

#### Scenario: Contributor opens evaluation numbered folder

- **WHEN** they open `evaluation/01_reports/`, `evaluation/02_graphs/`, `evaluation/03_data/`, or `evaluation/05_guides/`
- **THEN** each SHALL contain a `README.md` describing that folder's role and key files (not only a bare file listing)

### Requirement: Folder READMEs use a consistent minimum structure

Each folder README created or updated by this change SHALL include sections equivalent to: purpose, contents (table or list), how to use, and see-also links.

#### Scenario: Maintainer reviews a new folder README

- **WHEN** they open any README created under `packages/`, `infra/`, `stacks/`, or evaluation numbered subfolders
- **THEN** they SHALL find purpose and contents sections before deep methodology or historical detail

### Requirement: Folder READMEs link hierarchically

Child folder READMEs SHALL link to their parent README; the root README SHALL link to each major folder README without duplicating full child contents.

#### Scenario: Reader navigates from root to thesis figures

- **WHEN** they follow links root → `evaluation/README.md` → `02_graphs/README.md`
- **THEN** they SHALL reach `02_graphs/MANIFEST.md` within two clicks from `evaluation/README.md`

### Requirement: Application package README replaces boilerplate

`packages/frontend/README.md` SHALL describe the YouTube Comment Reader Flutter app (pages, API usage, theming entry point, integration tests link) and SHALL NOT remain the default Flutter template text alone.

#### Scenario: Developer opens frontend package README

- **WHEN** they read `packages/frontend/README.md`
- **THEN** they SHALL find project-specific setup and pointers to `integration_test/README.md`

### Requirement: Folder READMEs avoid stale evaluation paths

Evaluation folder READMEs SHALL NOT describe archived layouts as current (e.g. active `02_graphs/english/` or `02_graphs/portuguese/` folders).

#### Scenario: Reader checks figure location in 02_graphs README

- **WHEN** they read `evaluation/02_graphs/README.md`
- **THEN** it SHALL reference `MANIFEST.md`, `figures/`, and `tables/` as the docx keep-list layout

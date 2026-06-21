## Why

The repository has grown through multiple evaluation phases (October 2025 reorganization, November 2025 script consolidation, and ongoing model-analysis work), leaving overlapping folder structures, duplicate scripts, and analysis documents scattered at the `evaluation/` root. This makes it hard to find the canonical script to run, know where outputs land, or navigate documentation for the monograph. A single, documented layout is needed before further evaluation work accumulates more drift.

## What Changes

- Establish a **canonical evaluation layout** that subsumes the numbered folders (`01_reports`–`06_archived`) and the newer domain folders (`scripts/`, `model_analysis/`, `model_comparison/`, `api_load_testing/`).
- **Consolidate duplicate Python scripts** (e.g., shared names in `evaluation/scripts/01_model_evaluation/` and `evaluation/model_analysis/scripts/`) into one canonical location per script category, with symlinks or deprecation notices where backward compatibility is required.
- **Relocate loose analysis documents** from `evaluation/*.md` (e.g., `GUIA_SCRIPTS_AVALIACAO.md`, `TEXTO_AVALIACAO_MONOGRAFIA.md`, `ARGUMENTO_GENERALIZACAO_MODELO_SELECIONADO.md`) into the appropriate numbered or domain subfolders.
- **Merge overlapping README/guide files** into a small set of entry-point documents (`evaluation/README.md`, per-domain READMEs, and `05_guides/`).
- **Clarify root `scripts/`** (deployment shell scripts) vs `evaluation/` scripts with a short root README section or pointer.
- Update **cross-references** in reports and guides that still point to pre-reorganization paths (e.g., `evaluation/api_load_testing/*.py` when copies also live under `04_scripts/tests/`).
- **Archive** superseded folders and duplicate outputs under `06_archived/` rather than deleting historical artifacts needed for the thesis.
- **BREAKING**: Relative paths in Python scripts and markdown links will change; any external bookmarks or hard-coded paths outside the repo must be updated.

## Capabilities

### New Capabilities

- `evaluation-layout`: Canonical directory structure, naming conventions, and placement rules for reports, data, graphs, scripts, and archived material under `evaluation/`.
- `script-catalog`: Discoverable index of all runnable scripts (evaluation Python, load tests, deployment shell scripts) with category, purpose, working directory, inputs, and output locations.

### Modified Capabilities

<!-- No existing openspec/specs/ capabilities to modify -->

## Impact

- **Primary**: `evaluation/` (all subfolders, ~50 markdown files, ~60+ Python scripts, CSV/JSON/PNG artifacts).
- **Secondary**: Root `scripts/` (2 deployment shell scripts), root `README.md`.
- **Cross-references**: `packages/frontend/integration_test/` docs that cite `evaluation/04_scripts/tests/`.
- **Out of scope for this change**: Application source code (`packages/frontend`, `packages/lambdas`), OpenSpec changes unrelated to documentation layout, and re-running evaluations to regenerate results.

## Context

The `evaluation/` tree currently mixes three organizational schemes:

1. **Numbered layout** (`01_reports`–`06_archived`) from the October 2025 reorganization — still documented in `evaluation/README.md` and `05_guides/ORGANIZACAO_ARQUIVOS.md`.
2. **Domain layout** (`model_analysis/`, `model_comparison/`, `api_load_testing/`, `scripts/`) added during November 2025+ work — partially documented in `evaluation/scripts/README.md` and domain READMEs.
3. **Legacy copies** in `04_scripts/` and loose markdown at `evaluation/` root — overlapping with domain folders and creating duplicate Python files (14+ scripts share names between `scripts/01_model_evaluation/` and `model_analysis/scripts/`).

Root `scripts/` holds only deployment shell scripts (`build-and-push-sentiment-image.sh`, `deploy-with-sentiment.sh`), unrelated to evaluation but easily confused with `evaluation/scripts/`.

Constraints:
- Thesis/monograph artifacts must remain accessible; nothing is deleted, only moved or archived.
- Scripts embed hard-coded relative paths (e.g., `evaluation/api_load_testing/` in `04_scripts/generators/generate_academic_graphs.py`).
- Frontend E2E tests live in `packages/frontend/integration_test/` and are referenced from evaluation docs.

## Goals / Non-Goals

**Goals:**

- One canonical folder per concern: reports, guides, raw data, curated graphs, runnable scripts, and archived material.
- Single source of truth for each Python script category (model, API performance, model comparison).
- A navigable script catalog linked from `evaluation/README.md`.
- Updated cross-references in key entry-point documents.
- Clear separation between deployment scripts (`/scripts`) and evaluation scripts (`/evaluation/scripts`).

**Non-Goals:**

- Re-running evaluations or regenerating PNG/CSV/JSON outputs.
- Refactoring script internals beyond path updates.
- Moving Flutter integration tests out of `packages/frontend/`.
- Consolidating binary/image assets across all historical runs (only organize structure and references).

## Decisions

### 1. Hybrid layout: numbered folders for artifacts, domain folders for workflows

**Decision:** Keep `01_reports`, `02_graphs`, `03_data`, `05_guides`, `06_archived` for *outputs and documentation*. Use `evaluation/scripts/` as the *only* canonical location for runnable Python scripts, subdivided by category:

```
evaluation/
├── 01_reports/          # All final reports (including relocated root *.md reports)
├── 02_graphs/           # Curated thesis figures (english/ + portuguese/)
├── 03_data/             # Canonical CSV/JSON inputs and summarized outputs
├── 05_guides/           # Methodology and navigation guides
├── 06_archived/         # Superseded folders, duplicate scripts, old graph dumps
├── scripts/
│   ├── 01_model_evaluation/
│   ├── 02_api_performance/
│   └── 03_api_e2e/      # Python E2E helpers only (Flutter stays in packages/frontend)
├── model_analysis/      # results/, graphs/, reports/, data/ ONLY (no scripts/)
├── model_comparison/    # results/, scripts/ (comparison-specific), docs
└── api_load_testing/    # results/, graphs/, teste_*/ raw Locust runs ONLY (no scripts/)
```

**Rationale:** Numbered folders match existing thesis navigation; domain output folders preserve historical result paths referenced in monograph text. Scripts in one tree avoid "which copy do I run?" confusion.

**Alternative considered:** Flatten everything into numbered folders only — rejected because `model_analysis/results/` contains 100+ timestamped files and is already cited in docs.

### 2. Canonical script location: `evaluation/scripts/`

**Decision:** Merge unique scripts from `model_analysis/scripts/` into `evaluation/scripts/01_model_evaluation/`. Merge `api_load_testing/scripts/` and `04_scripts/tests/` + `04_scripts/generators/` into `evaluation/scripts/02_api_performance/` (generators as `02_api_performance/generators/` subfolder). Move `model_comparison/scripts/` content under `evaluation/scripts/01_model_evaluation/comparison/` or keep as sibling `evaluation/model_comparison/scripts/` with catalog entries pointing to canonical paths — prefer **catalog pointer** if scripts are tightly coupled to comparison notebooks.

**Rationale:** `evaluation/scripts/README.md` already documents this structure; extend rather than replace.

**Alternative considered:** Keep scripts co-located with outputs — rejected; duplicates already caused drift.

### 3. Deprecation via archive, not deletion

**Decision:** After consolidation, move emptied legacy script folders to `06_archived/legacy_scripts/` with a `README.md` explaining replacements. Leave stub README files in old locations for one release cycle pointing to new paths.

**Rationale:** Preserves git history context and thesis evidence paths.

### 4. Document taxonomy for loose root markdown

**Decision:** Relocate files using this mapping:

| Current location | Target |
|------------------|--------|
| `TEXTO_AVALIACAO_MONOGRAFIA.md`, `GUIA_*`, thesis drafts | `05_guides/` |
| `RELATORIO_*`, `DATASETS_*`, `ANALISE_*`, `ARGUMENTO_*`, `IMPACTO_*` | `01_reports/` or `model_analysis/reports/` (model-specific) |
| `API_EVALUATION_GUIDE.md`, `API_PERFORMANCE_TEST_RESULTS.md` | `01_reports/` (duplicates merge into existing reports where overlap exists) |
| `MUDANCAS_FINAIS_RESUMO.txt` | `06_archived/` |

**Rationale:** Reduces root clutter while keeping semantic grouping.

### 5. Script catalog as generated + curated index

**Decision:** Maintain `evaluation/scripts/CATALOG.md` (human-curated table) plus optional `scripts/generate_catalog.py` that scans `*.py` headers for docstrings. Root `README.md` gets a "Repository layout" section linking `scripts/` (deploy) vs `evaluation/` (analysis).

**Alternative considered:** Auto-only catalog — rejected; many scripts lack consistent docstrings.

### 6. Path resolution in scripts

**Decision:** Introduce a small shared helper `evaluation/scripts/_paths.py` with constants for `EVAL_ROOT`, `MODEL_RESULTS`, `API_RESULTS`, etc. Update scripts incrementally to import from it instead of string literals.

**Rationale:** Prevents future drift; minimal abstraction (one module, no package).

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Broken hard-coded paths in scripts after moves | Update paths in same PR; smoke-run one script per category |
| Broken markdown links in thesis PDF sources | Grep for `evaluation/` paths; update top 20 referenced files first |
| Duplicate results if both old and new output dirs exist | Document canonical output dirs in catalog; archive old script folders |
| Large diff noise from moving binaries | Move markdown/scripts first; batch PNG moves separately or leave outputs in place with catalog notes |
| Confusion between `/scripts` and `/evaluation/scripts` | Root README table + `evaluation/README.md` banner |

## Migration Plan

1. **Inventory** — List all `.py` files, dedupe by basename, mark canonical copy.
2. **Create `_paths.py`** — Define canonical directory constants.
3. **Merge scripts** — Copy unique scripts to `evaluation/scripts/`, update imports/paths.
4. **Relocate docs** — Move root markdown per taxonomy table; merge duplicate guides.
5. **Update entry points** — Rewrite `evaluation/README.md`, `evaluation/scripts/README.md`, root `README.md`.
6. **Create `CATALOG.md`** — Full script index with run instructions.
7. **Archive legacy** — Move `04_scripts/`, empty `model_analysis/scripts/`, `api_load_testing/scripts/` to `06_archived/`.
8. **Fix references** — Grep-update paths in `01_reports/`, `05_guides/`, frontend integration_test docs.
9. **Verify** — Run one script from each category; confirm outputs land in documented folders.

**Rollback:** Git revert; archived folders remain in `06_archived/` if partial migration.

## Open Questions (resolved)

- **`model_comparison/scripts/`**: Keep co-located with notebooks/results; catalog pointer only (no merge).
- **Thesis PDF frozen paths**: Stub READMEs left at `model_analysis/scripts/`, `api_load_testing/scripts/`, and `04_scripts/` pointing to canonical paths.
- **`api_load_testing/teste_1`–`teste_4`**: Not renamed in v1; outputs stay in place.

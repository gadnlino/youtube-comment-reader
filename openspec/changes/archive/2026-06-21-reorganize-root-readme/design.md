## Context

**Agreed documentation model:**

```
README.md (raiz)           ← orientação + links
├── packages/README.md
│   ├── frontend/README.md
│   └── lambdas/README.md
├── infra/README.md        ← deploy (substitui /scripts/)
├── stacks/README.md
└── evaluation/README.md   ← índice da avaliação
    ├── 01_reports/README.md
    ├── 02_graphs/README.md   → aponta para MANIFEST.md
    ├── 03_data/README.md
    ├── 05_guides/README.md
    ├── 06_archived/README.md (já existe)
    ├── scripts/README.md
    ├── model_analysis/README.md
    ├── api_load_testing/README.md
    └── model_comparison/README.md
```

**Deploy today:** `npm run deploy:dev` → `scripts/deploy-with-sentiment.sh` (Docker + ECR + CDK). `build-and-push-sentiment-image.sh` is a subset—archive. `scripts/perf/` is empty.

**Language:** Portuguese for README bodies; filesystem paths in English.

## Goals / Non-Goals

**Goals:**

- Any contributor opening a major folder finds a README explaining purpose, contents, and “what to read next”.
- Root README stays under ~120 lines; depth lives in child READMEs.
- Eliminate root `/scripts/` vs `evaluation/scripts/` confusion via `infra/`.
- All READMEs reflect post-prune layout (`02_graphs/MANIFEST.md`, archived figures).

**Non-Goals:**

- README in every leaf folder (`teste_1/`, `results/`, `graphs/` output dirs).
- Rewriting `ONDE_ESTA_TUDO.md` or full report bodies.
- `openspec/README.md` unless trivial one-liner (optional).
- Deleting deploy capability—only relocate and dedupe.

## Decisions

### 1. Root README sections (unchanged intent)

Title → O que é → Começar rápido → Mapa (links to folder READMEs) → Documentação.

Quick start deploy block: `npm run deploy:dev` → `infra/README.md`.

### 2. Folder README minimum template

Each major folder README SHALL include:

| Section | Content |
|---------|---------|
| **Propósito** | One paragraph |
| **Conteúdo** | Table or bullet list of immediate children |
| **Como usar** | Commands or “see parent/child README” |
| **Ver também** | Links to related READMEs |

Target length: **30–80 lines** per folder (evaluation domain READMEs may be slightly longer).

### 3. Folders that get READMEs in this change

| Path | Action |
|------|--------|
| `README.md` | Rewrite |
| `packages/README.md` | **Create** |
| `packages/frontend/README.md` | **Replace** boilerplate |
| `packages/lambdas/README.md` | **Create** |
| `infra/README.md` | **Create** |
| `stacks/README.md` | **Create** (brief: CDK stack role) |
| `evaluation/README.md` | **Expand** (full evaluation map + links to children) |
| `evaluation/01_reports/README.md` | **Create** |
| `evaluation/02_graphs/README.md` | **Create** (→ MANIFEST) |
| `evaluation/03_data/README.md` | **Create** |
| `evaluation/05_guides/README.md` | **Create** |
| `evaluation/06_archived/README.md` | **Update** if paths stale |
| `evaluation/model_analysis/README.md` | **Refresh** |
| `evaluation/api_load_testing/README.md` | **Verify** (recent edits) |
| `evaluation/model_comparison/README.md` | **Verify** |
| `evaluation/scripts/README.md` | **Verify** links |

**Skip:** `evaluation/04_scripts/` (redirect stub OK), `api_load_testing/teste_*`, output-only `graphs/`/`results/` README stubs unless already useful.

### 4. Deploy relocation

```
scripts/deploy-with-sentiment.sh  →  infra/deploy-with-sentiment.sh
scripts/build-and-push-sentiment-image.sh  →  infra/archive/ (archived, README note)
scripts/perf/  →  delete (empty)
scripts/  →  remove folder when empty
package.json deploy:dev  →  bash infra/deploy-with-sentiment.sh
CATALOG.md  →  update deployment rows
```

**Rationale:** `infra/` signals infrastructure/deploy; no name clash with evaluation scripts.

### 5. Orphan root `graphs/`

If `graphs/e2e_test_results_table_*.png` still exists at repo root, move to `evaluation/06_archived/pruned_figures/2026-06/` or delete duplicate; document in `evaluation/02_graphs/README.md` that canonical E2E table is under `02_graphs/tables/`.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| README proliferation / drift | Root map lists canonical READMEs; child READMEs link up/down |
| Broken links after `scripts/` removal | Grep `scripts/deploy` and `scripts/build` across repo in verification task |
| Frontend README scope creep | Cover app structure + links to integration_test; not full widget docs |

## Migration Plan

1. Create `infra/`, move deploy script, update `package.json`.
2. Archive build-only script, remove empty `scripts/`.
3. Write root README, then folder READMEs top-down (packages → evaluation children).
4. Update CATALOG deployment entries.
5. Grep for broken links and stale `english/`/`portuguese/` references in new READMEs.

## Open Questions

None blocking—user confirmed hierarchical README model and `infra/` over root `/scripts/`.

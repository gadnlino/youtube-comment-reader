# Step 2 — Root Markdown Audit

**Date:** 2026-06-21  
**Scope:** 12 files at `evaluation/` root (+ `README.md` stays)

## Summary

| Verdict | Count | Files |
|---------|------:|-------|
| KEEP at root | 1 | `README.md` (rewrite as entry point) |
| MOVE to `01_reports/` | 4 | Reports with results / analysis |
| MOVE to `05_guides/` | 5 | Monograph drafts & navigation guides |
| MERGE then ARCHIVE | 2 | Overlapping script guides |
| ARCHIVE | 1 | Change log txt |

---

## File-by-file decisions

### `README.md` (112 lines) — **KEEP at root, REWRITE**

- **Role:** Entry point / folder map
- **Problem:** Still lists `04_scripts/` as canonical; contradicts `scripts/README.md`
- **Referenced by:** Implicit (folder navigation)
- **Verdict:** Rewrite after consolidation; link to `scripts/CATALOG.md`

---

### `GUIA_COMPLETO_SCRIPTS_AVALIACAO.md` (993 lines) — **MERGE → ARCHIVE**

- **Role:** Comprehensive monograph reference for all script categories (includes model_comparison §0)
- **Overlap:** Superset of `GUIA_SCRIPTS_AVALIACAO.md` and `scripts/README.md`; cites `model_analysis/scripts/` and `api_load_testing/scripts/` as "original" locations
- **Referenced by:** `RELATORIO_VALIDACAO_INDEPENDENTE_SENTIMENT140.md`, `model_comparison/README.md`, self-citation for monograph
- **Verdict:** Extract unique content (model_comparison §0 detail) into `scripts/CATALOG.md` + `scripts/README.md`; move file to `06_archived/guides/GUIA_COMPLETO_SCRIPTS_AVALIACAO.md`; add stub redirect at old path if thesis cites it

---

### `GUIA_SCRIPTS_AVALIACAO.md` (312 lines) — **MERGE → ARCHIVE**

- **Role:** Shorter monograph script reference
- **Overlap:** Subset of GUIA_COMPLETO; duplicates `scripts/README.md` structure
- **Referenced by:** Self-citation only
- **Verdict:** Merge any unique monograph citation text into `scripts/README.md`; archive to `06_archived/guides/`

---

### `TEXTO_AVALIACAO_MONOGRAFIA.md` (430 lines) — **MOVE → `05_guides/`**

- **Role:** Draft prose for thesis evaluation section (3 pillars: model, API, frontend)
- **Referenced by:** `MUDANCAS_FINAIS_RESUMO.txt`
- **Verdict:** `05_guides/TEXTO_AVALIACAO_MONOGRAFIA.md`

---

### `GUIA_INSERCAO_FIGURAS_FINAL.md` (178 lines) — **MOVE → `05_guides/`**

- **Role:** Figure insertion guide for monograph (9 figures, paths into `model_analysis/graphs/`)
- **Referenced by:** `MUDANCAS_FINAIS_RESUMO.txt`
- **Verdict:** `05_guides/GUIA_INSERCAO_FIGURAS_FINAL.md`

---

### `RELATORIO_VALIDACAO_INDEPENDENTE_SENTIMENT140.md` (844 lines) — **MOVE → `01_reports/`**

- **Role:** Independent multi-dataset validation report (Twitter, IMDB, AiresPucrs)
- **Referenced by:** Links to `DATASETS_VALIDACAO_INDEPENDENTE.md`, `ARGUMENTO_GENERALIZACAO_MODELO_SELECIONADO.md`, `GUIA_COMPLETO`
- **Verdict:** `01_reports/RELATORIO_VALIDACAO_INDEPENDENTE_SENTIMENT140.md`

---

### `DATASETS_VALIDACAO_INDEPENDENTE.md` (265 lines) — **MOVE → `01_reports/`**

- **Role:** Dataset research notes for independent validation
- **Referenced by:** `RELATORIO_VALIDACAO_INDEPENDENTE_SENTIMENT140.md`
- **Verdict:** `01_reports/DATASETS_VALIDACAO_INDEPENDENTE.md` (paired with report above)

---

### `ANALISE_DATASETS_ALTERNATIVOS.md` (172 lines) — **MOVE → `01_reports/`**

- **Role:** Analysis of alternative PT datasets (ARIA UFPB, etc.)
- **Referenced by:** None found (supporting research doc)
- **Verdict:** `01_reports/ANALISE_DATASETS_ALTERNATIVOS.md`

---

### `ARGUMENTO_GENERALIZACAO_MODELO_SELECIONADO.md` (150 lines) — **MOVE → `01_reports/`**

- **Role:** Statistical generalization argument for monograph
- **Referenced by:** `GUIA_COMPLETO`, `model_comparison/README.md`, `RELATORIO_VALIDACAO`
- **Verdict:** `01_reports/ARGUMENTO_GENERALIZACAO_MODELO_SELECIONADO.md`

---

### `IMPACTO_DATASET_2_CLASSES.md` (147 lines) — **MOVE → `01_reports/`**

- **Role:** Explains 2-class vs 3-class dataset impact on metrics
- **Referenced by:** None found directly (supports validation reports)
- **Verdict:** `01_reports/IMPACTO_DATASET_2_CLASSES.md`

---

### `API_EVALUATION_GUIDE.md` (385 lines) — **MOVE → `05_guides/`**

- **Role:** English API evaluation framework (assignment doc)
- **Overlap:** Partial overlap with `05_guides/API_EVALUATION_METHODOLOGY.md` (848 lines, more detailed)
- **Referenced by:** `GUIA_SCRIPTS_AVALIACAO.md`
- **Verdict:** Move to `05_guides/API_EVALUATION_GUIDE.md`; add cross-link to `API_EVALUATION_METHODOLOGY.md`; consider merging later if content is redundant

---

### `API_PERFORMANCE_TEST_RESULTS.md` (337 lines) — **MOVE → `01_reports/`**

- **Role:** Oct 2025 API performance results (early test run)
- **Overlap:** Superseded in part by `01_reports/EXTENDED_API_PERFORMANCE_RESULTS.md`
- **Referenced by:** `01_reports/ASSIGNMENT_QUICK_REFERENCE.md`
- **Verdict:** `01_reports/API_PERFORMANCE_TEST_RESULTS.md` (historical report, keep for citation chain)

---

### `MUDANCAS_FINAIS_RESUMO.txt` (4384 bytes) — **ARCHIVE**

- **Role:** Change log / final summary notes
- **Verdict:** `06_archived/MUDANCAS_FINAIS_RESUMO.txt`

---

## Target root after cleanup

```
evaluation/
├── README.md                          ← only markdown at root
├── 01_reports/                        ← +6 reports from root
├── 05_guides/                         ← +3 guides from root
├── 06_archived/guides/                ← merged script guides
└── scripts/CATALOG.md + README.md     ← single script documentation entry
```

## Documentation hierarchy (post-merge)

| Need | Go to |
|------|-------|
| "Where is everything?" | `evaluation/README.md` |
| "How do I run a script?" | `evaluation/scripts/CATALOG.md` |
| "Script categories & deps" | `evaluation/scripts/README.md` |
| "Thesis draft text" | `05_guides/TEXTO_AVALIACAO_MONOGRAFIA.md` |
| "Figure paths for thesis" | `05_guides/GUIA_INSERCAO_FIGURAS_FINAL.md` |
| "Validation results" | `01_reports/RELATORIO_VALIDACAO_INDEPENDENTE_SENTIMENT140.md` |

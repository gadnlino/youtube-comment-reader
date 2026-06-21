# Step 3 — Cross-Reference Audit

**Date:** 2026-06-21  
**Scope:** References to legacy script paths and loose root markdown across the repo (excluding `openspec/changes/` planning files)

## Summary

| Legacy path pattern | Files referencing | Priority to update |
|--------------------|------------------:|-------------------|
| `04_scripts/` | 12 files | **High** — most stale after consolidation |
| `api_load_testing/scripts/` | 4 files | **High** — duplicates canonical tree |
| `model_analysis/scripts/` | 3 files | **Medium** — GUIA_COMPLETO only |
| Root `evaluation/*.md` (loose) | 8 cross-links | **Medium** — update when files move |
| Wrong e2e path (`04_scripts/tests/e2e_*`) | 3 files | **High** — path is incorrect today |

---

## A. References to `04_scripts/`

| File | Lines / context | Update to |
|------|-----------------|-----------|
| `evaluation/README.md` | Lists `04_scripts/` in structure + script sections | `evaluation/scripts/02_api_performance/` |
| `evaluation/scripts/README.md` | Points to `../../04_scripts/tests/` as complementary | `02_api_performance/benchmarks/` |
| `evaluation/GUIA_SCRIPTS_AVALIACAO.md` | § additional scripts at `04_scripts/tests/` | Archive file; fix in `scripts/CATALOG.md` |
| `evaluation/GUIA_COMPLETO_SCRIPTS_AVALIACAO.md` | § complementary scripts + methodology refs | Archive file; fix in `scripts/CATALOG.md` |
| `evaluation/05_guides/ORGANIZACAO_ARQUIVOS.md` | Entire reorg plan centers on `04_scripts/` | Rewrite or archive as historical |
| `evaluation/05_guides/API_EVALUATION_METHODOLOGY.md` | 6 script refs + `cd evaluation/04_scripts/tests` | `scripts/02_api_performance/benchmarks/` |
| `evaluation/05_guides/E2E_FUNCTIONALITY_TESTING_METHODOLOGY.md` | `04_scripts/tests/e2e_functionality_test.py` | `scripts/03_api_e2e/` or `e2e_functionality_testing/` |
| `packages/frontend/integration_test/docs/CRITICAL_USER_FLOWS_TEST_REPORT.md` | Cites `04_scripts/tests/e2e_functionality_test.py` | Correct path + note Flutter tests are canonical |

---

## B. References to `api_load_testing/scripts/`

| File | Context | Update to |
|------|---------|-----------|
| `evaluation/api_load_testing/README.md` | 5× `cd evaluation/api_load_testing/scripts` | `cd evaluation/scripts/02_api_performance` |
| `evaluation/GUIA_COMPLETO_SCRIPTS_AVALIACAO.md` | "Scripts originais" section | Remove; single canonical path |

**Note:** Many files reference `evaluation/api_load_testing/` for **data/results** (CSV, PNG, JSON) — those paths should **stay unchanged** in v1.

---

## C. References to `model_analysis/scripts/`

| File | Context | Update to |
|------|---------|-----------|
| `evaluation/GUIA_COMPLETO_SCRIPTS_AVALIACAO.md` | "Scripts originais" + `cd model_analysis/scripts` | `scripts/01_model_evaluation/` |
| `evaluation/model_analysis/README.md` | Likely references local scripts | Update to canonical path |

---

## D. References to loose root markdown (will break on move)

| Source file | Target cited | New path after Step 2 |
|-------------|--------------|----------------------|
| `RELATORIO_VALIDACAO_INDEPENDENTE_SENTIMENT140.md` | `evaluation/DATASETS_VALIDACAO_INDEPENDENTE.md` | `01_reports/DATASETS_VALIDACAO_INDEPENDENTE.md` |
| `RELATORIO_VALIDACAO_INDEPENDENTE_SENTIMENT140.md` | `evaluation/GUIA_COMPLETO_SCRIPTS_AVALIACAO.md` | `scripts/CATALOG.md` or archived stub |
| `RELATORIO_VALIDACAO_INDEPENDENTE_SENTIMENT140.md` | `evaluation/ARGUMENTO_GENERALIZACAO_MODELO_SELECIONADO.md` | `01_reports/ARGUMENTO_GENERALIZACAO_MODELO_SELECIONADO.md` |
| `model_comparison/README.md` | `evaluation/ARGUMENTO_GENERALIZACAO_MODELO_SELECIONADO.md` | `01_reports/...` |
| `model_comparison/README.md` | `evaluation/GUIA_COMPLETO_SCRIPTS_AVALIACAO.md` | `scripts/CATALOG.md` |
| `GUIA_COMPLETO_SCRIPTS_AVALIACAO.md` | `evaluation/ARGUMENTO_GENERALIZACAO_MODELO_SELECIONADO.md` | `01_reports/...` |
| `GUIA_SCRIPTS_AVALIACAO.md` | `evaluation/API_EVALUATION_GUIDE.md` | `05_guides/API_EVALUATION_GUIDE.md` |
| `01_reports/ASSIGNMENT_QUICK_REFERENCE.md` | `evaluation/API_PERFORMANCE_TEST_RESULTS.md` | `01_reports/API_PERFORMANCE_TEST_RESULTS.md` |
| `MUDANCAS_FINAIS_RESUMO.txt` | `TEXTO_AVALIACAO_MONOGRAFIA.md`, `GUIA_INSERCAO_FIGURAS_FINAL.md` | `05_guides/...` |

---

## E. References that are OK (no change needed)

| Pattern | Why OK |
|---------|--------|
| `evaluation/api_load_testing/` (data, graphs, teste_*) | Output location — keep in v1 |
| `evaluation/model_analysis/results/`, `graphs/` | Output location — keep in v1 |
| `evaluation/01_reports/*` | Already in numbered layout |
| `evaluation/02_graphs/*`, `03_data/*` | Already in numbered layout |
| `packages/frontend/integration_test/` | Correct location for Flutter E2E |
| `evaluation/model_comparison/scripts/` | Decision: keep co-located |

---

## F. Recommended update order (when implementing)

```
1. Create scripts/CATALOG.md + _paths.py          (new targets exist)
2. Move scripts (canonical tree populated)
3. Move markdown (new doc paths exist)
4. Update high-priority refs:
   - evaluation/README.md
   - evaluation/scripts/README.md
   - evaluation/api_load_testing/README.md
   - 05_guides/API_EVALUATION_METHODOLOGY.md
5. Update report cross-links (01_reports/, model_comparison/)
6. Archive ORGANIZACAO_ARQUIVOS.md or mark historical
7. Add redirect stubs at old paths if thesis PDF cites them
```

---

## G. Broken reference found today (pre-reorganization)

| Doc says | Reality |
|----------|---------|
| `04_scripts/tests/e2e_functionality_test.py` | File is at `e2e_functionality_testing/e2e_functionality_test.py` |
| `README.md` says scripts are in `04_scripts/` | Duplicates also in `scripts/02_api_performance/` |
| `GUIA_COMPLETO` says run from `model_analysis/scripts/` | Same scripts exist in `scripts/01_model_evaluation/` |

These confirm file-by-file audit was necessary before any bulk move.

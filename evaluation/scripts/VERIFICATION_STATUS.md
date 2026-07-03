# Estado da verificação dos scripts

Gerado em: 2026-06-21 (organize-scripts-and-analysis)

## Resumo

| Nível | Resultado |
|-------|-----------|
| L1 (py_compile) | 45/45 scripts canônicos OK |
| L3 offline (verificação pontual) | `generate_confusion_matrix.py` OK |
| Nomes duplicados fora de `06_archived/` | 0 |

## Verificações pontuais

| Script | CWD | L1 | L3 | Notas |
|--------|-----|----|----|-------|
| `01_model_evaluation/generate_confusion_matrix.py` | `01_model_evaluation/` | OK | OK | Grava PNG no diretório local / `model_analysis/graphs/` |
| `02_api_performance/generators/generate_academic_graphs_pt.py` | raiz do repo | OK | BACKLOG | Requer CSV em `03_data/csv/`; executar manualmente |
| `02_api_performance/common.py` | `02_api_performance/` | OK | SKIP-L4 | API em produção necessária para execução completa |

## Backlog (análise posterior)

Consulte [`VERIFICATION_BACKLOG.md`](VERIFICATION_BACKLOG.md) para scripts não reexecutados por completo (API live, Kaggle, testes de carga longos).

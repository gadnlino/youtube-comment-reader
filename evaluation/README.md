# Avaliação — YouTube Comment Reader

Ponto de entrada para relatórios, dados, scripts e material arquivado da avaliação.

## Estrutura

| Pasta | Finalidade |
|-------|------------|
| `01_reports/` | Relatórios finais e de apoio |
| `02_graphs/` | Figuras curadas para a monografia (english/ + portuguese/) |
| `03_data/` | CSV/JSON canónicos de entrada e resumos |
| `05_guides/` | Metodologia, rascunhos da monografia, navegação |
| `06_archived/` | Scripts e guias substituídos (ver índice interno) |
| `scripts/` | **Scripts Python canónicos** — comece em `scripts/CATALOG.md` |
| `model_analysis/` | **Saídas** da avaliação do modelo (results/, graphs/, data/) |
| `api_load_testing/` | **Saídas** dos testes de carga (results/, graphs/, teste_*/) |
| `model_comparison/` | Comparação de modelos (scripts co-localizados com notebooks) |

## Links rápidos

- **Índice de scripts:** [`scripts/CATALOG.md`](scripts/CATALOG.md)
- **Visão geral dos scripts:** [`scripts/README.md`](scripts/README.md)
- **Relatório final:** [`01_reports/FINAL_EVALUATION_REPORT.md`](01_reports/FINAL_EVALUATION_REPORT.md)
- **Metodologia:** [`01_reports/TESTING_METHODOLOGY.md`](01_reports/TESTING_METHODOLOGY.md)
- **Guia de navegação:** [`05_guides/ONDE_ESTA_TUDO.md`](05_guides/ONDE_ESTA_TUDO.md)
- **Texto da monografia:** [`05_guides/TEXTO_AVALIACAO_MONOGRAFIA.md`](05_guides/TEXTO_AVALIACAO_MONOGRAFIA.md)

## Executar scripts

```bash
# Avaliação do modelo (exemplo)
cd evaluation/scripts/01_model_evaluation
python generate_confusion_matrix.py

# Performance da API (exemplo)
cd evaluation/scripts/02_api_performance
python run_all.py
```

Scripts shell de implantação ficam na **raiz do repo** em `/scripts/` (não aqui). Ver `README.md` na raiz.

## Material arquivado

Duplicatas e guias antigos estão em `06_archived/` — ver [`06_archived/README.md`](06_archived/README.md).

# Backlog de verificação

Scripts que não foram totalmente reexecutados após a reorganização de 2026-06-21. L1 (sintaxe/compilação) passou em todos os scripts canônicos.

| Script | Nível | Causa provável | Bloqueia monografia? | Prioridade |
|--------|-------|----------------|----------------------|------------|
| `02_api_performance/run_all.py` | L4 | Requer API AWS em produção | Não (resultados arquivados) | Baixa |
| `02_api_performance/benchmarks/heavy_load_test.py` | L4 | Execução longa + API live | Não | Baixa |
| `01_model_evaluation/compare_metrics_vs_benchmark.py` | L2/L4 | Requer `working_videos_*.json` + API live | Não | Média |
| `01_model_evaluation/validate_with_*.py` | L4 | Datasets Kaggle + API live | Não | Média |
| `model_comparison/scripts/*.py` | L4 | Tempo de treino ML + dependências | Não | Baixa |
| `02_api_performance/generators/generate_academic_graphs_pt.py` | L3 | CSVs de entrada em `03_data/csv/` | Não (figuras em `02_graphs/`) | Média |

**Política:** Falhas aqui não bloqueiam a reorganização. Corrigir caminhos ou credenciais ao reexecutar avaliações.

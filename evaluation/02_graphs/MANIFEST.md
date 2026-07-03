# Inventário de figuras e tabelas da monografia (apenas docx)

Caminhos canônicos dos **sete ativos** embebidos no documento Word da monografia (Tabela 1–4, Figura 23–26). Figuras de rascunho em markdown (`multiple_sets_*`, gráficos de análise de idioma, gráficos PT da API) **não** estão nesta lista e foram arquivadas em `evaluation/06_archived/pruned_figures/2026-06/`.

Inventário legível por máquina: [`inventory.json`](inventory.json).

## Lista de ativos (keep-list)

| Docx | Tipo | Caminho canônico | Gerador | Dados de suporte |
|------|------|------------------|---------|------------------|
| **Tabela 1** | Tabela Word (exportação TXT) | [`../model_comparison/results/comprehensive_model_comparison.txt`](../model_comparison/results/comprehensive_model_comparison.txt) | [`../model_comparison/scripts/comprehensive_model_comparison.py`](../model_comparison/scripts/comprehensive_model_comparison.py) | Entradas de comparação em `evaluation/model_comparison/` |
| **Tabela 3** | Tabela Word (métricas Locust) | Regenerar via gerador; PNG de referência arquivado | [`../scripts/02_api_performance/generate_consolidated_graphs.py`](../scripts/02_api_performance/generate_consolidated_graphs.py) | CSV/JSON Locust em `evaluation/api_load_testing/` |
| **Tabela 4** | Tabela Word (PNG E2E) | [`tables/tabela-4_e2e_test_results_table.png`](tables/tabela-4_e2e_test_results_table.png) | [`../scripts/02_api_performance/generate_e2e_test_table.py`](../scripts/02_api_performance/generate_e2e_test_table.py) | Lista `TESTES` embutida no script (sem CSV externo) |
| **Figura 23** | Gráfico de métricas por classe | [`figures/figura-23_metrics_per_class_youtube_comments_with_labeled.png`](figures/figura-23_metrics_per_class_youtube_comments_with_labeled.png) | [`../scripts/01_model_evaluation/evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py`](../scripts/01_model_evaluation/evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py) | [`../model_analysis/results/metrics_tfidf_lr_amitzala_youtube-comments-with-labeled_20260317_230701.csv`](../model_analysis/results/metrics_tfidf_lr_amitzala_youtube-comments-with-labeled_20260317_230701.csv) |
| **Figura 24** | Barras seleção vs Kaggle | [`figures/figura-24_tfidf_lr_selection_vs_kaggle_amitzala.png`](figures/figura-24_tfidf_lr_selection_vs_kaggle_amitzala.png) | [`../scripts/01_model_evaluation/plot_tfidf_lr_selection_vs_kaggle_amitzala.py`](../scripts/01_model_evaluation/plot_tfidf_lr_selection_vs_kaggle_amitzala.py) | CSV Kaggle AmitZala + métricas de seleção (ver docstring do script) |
| **Figura 25** | Painel Locust (parte 1) | [`figures/figura-25_consolidated_graphs_part1.png`](figures/figura-25_consolidated_graphs_part1.png) | [`../scripts/02_api_performance/generate_consolidated_graphs.py`](../scripts/02_api_performance/generate_consolidated_graphs.py) | Dados Locust em `evaluation/api_load_testing/` |
| **Figura 26** | Painel Locust (parte 2) | [`figures/figura-26_consolidated_graphs_part2.png`](figures/figura-26_consolidated_graphs_part2.png) | igual à Figura 25 | igual à Figura 25 |

### Linhagem das fontes (cópias canônicas)

| Figura/tabela no docx | Nome original no repositório (arquivado após a cópia) |
|-----------------------|------------------------------------------------------|
| Figura 23 | `metrics_per_class_tfidf_lr_amitzala_youtube-comments-with-labeled_20260317_230701.png` |
| Figura 24 | `tfidf_lr_selection_vs_kaggle_amitzala_20260621_172335.png` (mais recente de duas execuções; cópia antiga arquivada) |
| Figura 25 / 26 | `consolidated_graphs_part1.png`, `consolidated_graphs_part2.png` |
| Tabela 4 | Regenerada em 2026-06-21 (`generate_e2e_test_table.py`); substitui o `e2e_test_results_table_20251102.png` em falta |

## Regeneração

Na raiz do repositório, com `pip install -r evaluation/requirements.txt`:

```bash
# Tabela 1 (TXT)
python3 evaluation/model_comparison/scripts/comprehensive_model_comparison.py

# Tabela 3, Figura 25–26
python3 evaluation/scripts/02_api_performance/generate_consolidated_graphs.py

# Tabela 4 (PNG canônico em tables/tabela-4_e2e_test_results_table.png)
python3 evaluation/scripts/02_api_performance/generate_e2e_test_table.py --thesis

# Figura 23 (requer dataset de comentários YouTube etiquetados + modelo treinado)
python3 evaluation/scripts/01_model_evaluation/evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py

# Figura 24 (requer caminhos do CSV Kaggle AmitZala configurados no script)
python3 evaluation/scripts/01_model_evaluation/plot_tfidf_lr_selection_vs_kaggle_amitzala.py
```

Após regenerar, copie os novos PNGs para `figures/` ou `tables/` com os nomes canônicos acima (exceto a Tabela 4 com `--thesis`, que já grava no caminho canônico).

## Excluídos da lista de ativos (arquivados)

- Todos os PNGs `*_pt*` e as pastas `02_graphs/english/`, `02_graphs/portuguese/` (10 figuras de performance EN/PT)
- Figuras de rascunho em markdown: `multiple_sets_*`, gráficos de análise de idioma (`language_neutral_bias_*`, etc.)
- Gráficos de relatórios de validação Sentiment140 / IMDB
- Execuções duplicadas com timestamp (ex.: `tfidf_lr_selection_vs_kaggle_amitzala_*` mais antigos)

Local do arquivo: [`../06_archived/pruned_figures/2026-06/`](../06_archived/pruned_figures/2026-06/) — ver [`README.md`](../06_archived/pruned_figures/2026-06/README.md).

## Verificação (2026-06-21)

- Os cinco scripts geradores passam em `py_compile`.
- `generate_e2e_test_table.py` em teste de fumaça produz o PNG da Tabela 4 (dados de teste embutidos).
- Os outros geradores exigem entradas externas documentadas acima; os PNGs canônicos estão preservados em `figures/` e `tables/`.
- Capturas do docx enviadas pelo autor conferidas por conteúdo: Figura 24 (59,5% vs 52,9%), Figura 25/26 (painéis TPS / sucesso / resposta), Figura 23 (barras por classe), Tabela 4 (8 linhas E2E).

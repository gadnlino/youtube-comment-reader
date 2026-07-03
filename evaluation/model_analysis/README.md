# Saídas da análise do modelo — `model_analysis/`

Resultados, gráficos, dados e relatórios das execuções de avaliação do **Pilar 1 — Modelo**.

## Propósito

Destino das saídas dos scripts em [`../scripts/01_model_evaluation/`](../scripts/CATALOG.md). Não execute scripts duplicados em `scripts/` (redirect) — use a árvore canônica.

## Conteúdo

| Subpasta | Finalidade |
|----------|------------|
| `data/` | JSON de entrada (working_videos, etc.) |
| `results/` | CSV/JSON das análises |
| `graphs/` | PNG gerados (maioria arquivada se não estiver no docx) |
| `reports/` | Relatórios em texto |
| `scripts/README.md` | Redirect para `../scripts/` |

Documentos de apoio: `FINAL_MULTILINGUAL_EVALUATION_SUMMARY.md`, `LANGUAGE_ANALYSIS_GRAPHS_GUIDE.md`, `TABELA_COMPARACAO_METRICAS.md`.

## Como usar

```bash
cd evaluation/scripts/01_model_evaluation
python compare_metrics_vs_benchmark.py   # exemplo
pip install -r ../../requirements.txt    # na raiz: evaluation/requirements.txt
```

## Figuras da monografia

- **Figura 23:** [`../02_graphs/figures/`](../02_graphs/figures/)
- **Figura 24:** [`../02_graphs/figures/`](../02_graphs/figures/) via `plot_tfidf_lr_selection_vs_kaggle_amitzala.py`
- Outros PNG em `graphs/`: fora da lista de ativos do docx — [`../02_graphs/MANIFEST.md`](../02_graphs/MANIFEST.md)

## Regenerar figuras e tabelas da monografia

Inventário completo (Tabela 1–4, Figuras 23–26): [`../02_graphs/MANIFEST.md`](../02_graphs/MANIFEST.md).

Pré-requisito (raiz do repositório):

```bash
pip install -r evaluation/requirements.txt
```

### Tabela 1 — Comparação dos modelos

Texto de referência em [`../model_comparison/results/comprehensive_model_comparison.txt`](../model_comparison/results/comprehensive_model_comparison.txt).

```bash
python3 evaluation/model_comparison/scripts/comprehensive_model_comparison.py
```

Entradas: dados e resultados sob `evaluation/model_comparison/`.

### Figura 23 — Métricas por classe (YouTube Comments with Labeled)

Gera o gráfico de precisão/recall/F1 por classe e o CSV de métricas em `results/`.

```bash
python3 evaluation/scripts/01_model_evaluation/evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py
```

Requisitos: dataset Kaggle *YouTube Comments with Labeled* e o modelo TF-IDF + Regressão Logística pré-treinado (caminhos no script).

Cópia canônica na monografia:

[`../02_graphs/figures/figura-23_metrics_per_class_youtube_comments_with_labeled.png`](../02_graphs/figures/figura-23_metrics_per_class_youtube_comments_with_labeled.png)

CSV de referência já presente:

[`results/metrics_tfidf_lr_amitzala_youtube-comments-with-labeled_20260317_230701.csv`](results/metrics_tfidf_lr_amitzala_youtube-comments-with-labeled_20260317_230701.csv)

Após regenerar, copie o PNG novo para o caminho canônico acima (se o script gravar em outro local, por exemplo `graphs/`).

### Figura 24 — Seleção vs avaliação no Kaggle AmitZala

Compara acurácia, precisão macro e F1 macro da etapa de seleção (`comprehensive_model_comparison.txt`) com a avaliação no CSV AmitZala.

```bash
# Usa o último CSV de métricas em results/, ou indique um arquivo:
python3 evaluation/scripts/01_model_evaluation/plot_tfidf_lr_selection_vs_kaggle_amitzala.py \
  --metrics-csv evaluation/model_analysis/results/metrics_tfidf_lr_amitzala_youtube-comments-with-labeled_20260317_230701.csv
```

Cópia canônica:

[`../02_graphs/figures/figura-24_tfidf_lr_selection_vs_kaggle_amitzala.png`](../02_graphs/figures/figura-24_tfidf_lr_selection_vs_kaggle_amitzala.png)

### Outros ativos da monografia (fora deste diretório)

| Ativo | Onde regenerar |
|--------|----------------|
| **Tabela 3**, **Figuras 25–26** | [`../api_load_testing/README.md`](../api_load_testing/README.md) — `generate_consolidated_graphs.py` |
| **Tabela 4** (E2E Flutter) | `python3 evaluation/scripts/02_api_performance/generate_e2e_test_table.py --thesis` |

## Ver também

- [`../README.md`](../README.md) — índice da avaliação
- [`../scripts/CATALOG.md`](../scripts/CATALOG.md) — scripts canônicos
- [`../06_archived/2025-11_duplicate_scripts/model_analysis_scripts/`](../06_archived/2025-11_duplicate_scripts/model_analysis_scripts/) — cópias antigas

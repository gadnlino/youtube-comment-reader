# Scripts de Análise e Validação do Modelo

Esta pasta contém todos os scripts relacionados à análise, validação e avaliação do modelo de classificação de sentimento (TF-IDF + Logistic Regression).

## Scripts Principais

### Validação de Métricas

- **`compare_metrics_vs_benchmark.py`**: Compara as métricas básicas (Accuracy, Precision, Recall, F1-Score) da validação atual com o benchmark inicial. Valida se o modelo mantém o desempenho observado durante a seleção.

- **`validate_model_accuracy_with_dataset.py`**: Valida a acurácia do modelo comparando predições da API com ground truth do dataset comentário por comentário.

### Validação de Distribuições

- **`validate_model_distribution_multiple_sets.py`**: Valida o viés sistemático do modelo usando múltiplos conjuntos aleatórios de vídeos (145 vídeos divididos em 5 conjuntos de 29). Compara distribuições de sentimento (ground truth vs predições).

- **`validate_model_distribution.py`**: Validação de distribuição para um conjunto menor de vídeos.

- **`validate_model_distribution_vs_benchmark.py`**: Compara a distribuição de sentimento observada na validação com a distribuição do benchmark inicial.

### Análise de Idioma

- **`language_impact_analysis.py`**: Analisa o impacto do idioma na classificação de sentimento, identificando viés linguístico.

- **`multilingual_sentiment_analysis.py`**: Análise detalhada de sentimento em múltiplos idiomas.

- **`analyze_video_language.py`**: Analisa o perfil de idioma dos vídeos.

### Geração de Visualizações

- **`generate_confusion_matrix.py`**: Gera matriz de confusão do modelo.

- **`generate_consolidated_distribution_analysis.py`**: Gera análises consolidadas de distribuição.

- **`generate_metrics_comparison_table.py`**: Gera tabela e gráfico comparando métricas do benchmark vs validação.

### Utilitários

- **`pre_filter_working_videos.py`**: Pré-filtra vídeos que funcionam com a API para uso nas validações.

## Como Usar

Todos os scripts assumem que você está executando a partir da pasta `evaluation/model_analysis/` ou `evaluation/`. Os arquivos de dados (CSV, JSON) podem estar em `api_load_testing/` ou na pasta atual.

### Exemplo:

```bash
cd evaluation/model_analysis
python compare_metrics_vs_benchmark.py
```

Ou:

```bash
cd evaluation
python model_analysis/compare_metrics_vs_benchmark.py
```

## Dependências

- `pandas`
- `numpy`
- `scikit-learn`
- `matplotlib`
- `seaborn`
- `requests`
- `scipy`

## Estrutura de Pastas

```
model_analysis/
├── data/              # Arquivos de entrada (working_videos, dataset_videos)
├── results/           # Resultados JSON das análises
├── graphs/            # Gráficos e visualizações geradas
└── *.py              # Scripts de análise
```

## Arquivos de Dados Necessários

- `youtube_comments_cleaned.csv`: Dataset com ground truth (geralmente em `../api_load_testing/`)
- `data/working_videos_*.json`: Lista de vídeos pré-filtrados (gerados por `pre_filter_working_videos.py`)
- `data/dataset_videos_*.json`: Listas de vídeos para validação específica

## Resultados

- **JSON**: Salvos em `results/` (métricas, validações, comparações)
- **Gráficos PNG**: Salvos em `graphs/` (comparações, distribuições, matrizes de confusão)

Os scripts automaticamente criam as pastas `data/`, `results/` e `graphs/` se não existirem.


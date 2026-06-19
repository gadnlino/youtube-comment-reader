# Experimento: 20k aleatório vs. 20k balanceado (⅓ por classe)

Objetivo: comparar as **mesmas métricas** da seleção de modelos em
`comprehensive_model_comparison.py`, usando:

1. **Amostra A (igual ao TCC atual):** 20.000 comentários com `sample` aleatório simples (`random_state=42`).
2. **Amostra B (estratificada por classe):** 20.000 comentários com **~⅓ por classe** (6.667 / 6.667 / 6.666 para negative, neutral, positive em ordem alfabética do rótulo normalizado).

Assim você vê se os números da tabela original mudiam muito com balanceamento **apenas** no subconjunto de 20k — útil para responder orientadoras e ajustar o texto do TCC.

## Pré-requisitos

- Mesmas dependências do script principal (`kagglehub`, `pandas`, `sklearn`, `nltk`, `textblob`).
- Download do dataset Kaggle `amaanpoonawala/youtube-comments-sentiment-dataset` na primeira execução.

## Como rodar

Na raiz do repositório:

```bash
python3 evaluation/model_comparison/balanced_20k_experiment/compare_random_vs_balanced_20k.py
```

Saída: arquivo em `evaluation/model_comparison/balanced_20k_experiment/results/` com tabela comparativa e distribuição das classes nas duas amostras.

## O que não muda entre A e B

- Thresholds VADER/TextBlob, TF-IDF (10k features, ngrams, etc.), LR e SVM, split **80/20** com `stratify` para ML.
- Transformers continuam sendo valores fixos do notebook (igual ao script original), apenas listados para referência no relatório gerado.

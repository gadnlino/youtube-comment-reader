# Comparação de Modelos — `model_comparison/`

Scripts e resultados da comparação de classificadores (**seleção do modelo** — Tabela 1 docx).

> **Ordem cronológica**: executado **antes** da avaliação do TF-IDF+LR selecionado. Ver [`../README.md`](../README.md).

## Propósito

## 📁 Estrutura de Pastas

```
model_comparison/
├── scripts/                          # Scripts Python de comparação
│   ├── tfidf_logistic_classification_report.py  # TF-IDF + LR (66.1% accuracy)
│   ├── vader_classification_report.py        # VADER (53.4% accuracy)
│   ├── textblob_classification_report.py     # TextBlob (48.8% accuracy)
│   ├── svm_classification_report.py          # TF-IDF + SVM (52.5% accuracy)
│   ├── fix_nltk_ssl.py                      # Utilitário NLTK
│   ├── nltk_setup.py                        # Setup NLTK
│   └── requirements.txt                     # Pointer to evaluation/requirements.txt
│
├── results/                          # Resultados das comparações
│   ├── tfidf_logistic_results.txt           # Resultados TF-IDF + LR
│   ├── vader_results_full_dataset.txt       # Resultados VADER
│   ├── textblob_results_full_dataset.txt    # Resultados TextBlob
│   └── svm_results_*.txt                    # Resultados SVM
│
├── notebooks/                        # Notebooks Jupyter
│   └── youtube_comments_sentiment_analysis_comparison.ipynb  # Transformers
│
├── README.md                         # Este arquivo
├── MODEL_COMPARISON_SUMMARY.md       # Resumo da comparação
└── README_VADER_ANALYSIS.md          # Análise específica do VADER
```

---

## 🎯 Objetivo

Comparar diferentes modelos de análise de sentimento para selecionar o melhor modelo para o sistema, incluindo:
- Modelos baseados em regras (VADER, TextBlob)
- Modelos de Machine Learning tradicional (TF-IDF + Logistic Regression, TF-IDF + SVM)
- Modelos Transformer (DeBERTa, Twitter-XLM-RoBERTa)
- Métricas de desempenho (Accuracy, F1-Score, tempo de processamento)
- Seleção do modelo final baseado em desempenho e viabilidade

---

## 🚀 Como Executar

### Pré-requisitos

From the repository root:

```bash
pip install -r evaluation/requirements.txt
```

**Configuração do NLTK (para VADER)**:
```bash
python fix_nltk_ssl.py
python -c "import nltk; nltk.download('vader_lexicon')"
```

### Executar Comparação Completa

```bash
cd evaluation/model_comparison/scripts
python comprehensive_model_comparison.py
```

### Executar Avaliação do Modelo Selecionado (Benchmark)

```bash
cd evaluation/model_comparison/scripts
python tfidf_logistic_classification_report.py
```

**Nota**: Este script estabelece o **benchmark** do modelo selecionado que será usado posteriormente na validação (`scripts/01_model_evaluation/compare_metrics_vs_benchmark.py`).

### Executar Testes Individuais

```bash
cd evaluation/model_comparison/scripts

# Testar cada modelo individualmente
python vader_classification_report.py
python textblob_classification_report.py
python svm_classification_report.py

# Testes rápidos (amostra menor)
python tfidf_logistic_quick_test.py
python vader_quick_test.py
python textblob_quick_test.py
python svm_quick_test.py
```

---

## 📊 Resultados

### Modelo Selecionado: TF-IDF + Logistic Regression

- **Accuracy**: 66.14%
- **F1-Score (Macro)**: 66.28%
- **Precision (Macro)**: 66.64%
- **Recall (Macro)**: 66.14%
- **Dataset Utilizado**: 1.032.225 comentários
- **Divisão Train/Test**: 80/20 (ao nível de comentários, `random_state=42`)
- **Tempo de Processamento**: ~100-200 segundos (dependendo do hardware)

### Comparação com Outros Modelos

| Modelo | Accuracy | F1 (Macro) | Velocidade | Tipo |
|--------|----------|------------|------------|------|
| VADER | ~53% | ~53% | Muito Rápido | Rule-based |
| TextBlob | ~50% | ~50% | Muito Rápido | Rule-based |
| TF-IDF + LR | **66.14%** | **66.28%** | Rápido | Traditional ML |
| TF-IDF + SVM | ~65% | ~65% | Médio | Traditional ML |
| Transformers | ~71-73% | ~71-73% | Lento | Deep Learning |

**Decisão**: TF-IDF + Logistic Regression foi selecionado por oferecer o melhor equilíbrio entre desempenho, velocidade e viabilidade de deploy em produção.

---

## ⚠️ Notas Importantes sobre a Divisão de Dados e Generalização

**Como a divisão foi feita na comparação de modelos**:
- O `train_test_split` foi feito ao nível de **comentários individuais** (não vídeos)
- Divisão: 80% treino / 20% teste, com `random_state=42` e `stratify=labels`
- Isso significa que comentários do mesmo vídeo podem estar tanto no treino quanto no teste
- Dataset completo: 1.032.225 comentários
  - Treino: ~825.780 comentários (80%)
  - Teste: ~206.445 comentários (20%)

**Por que esta divisão é adequada para comparação de modelos**:
- ✅ Testa a capacidade de classificar **comentários individuais**, que é o objetivo dos modelos
- ✅ Permite comparar modelos de forma justa usando a mesma divisão de dados
- ✅ É o método padrão para avaliação de modelos de classificação de texto

**Por que não invalida o argumento de generalização**:
- ✅ A **validação de generalização para vídeos diferentes** é feita **separadamente** nos scripts de `evaluation/scripts/01_model_evaluation/`
- ✅ A validação usa **vídeos completos diferentes** buscados via API em produção
- ✅ Os vídeos usados na validação são **diferentes** dos vídeos usados na comparação
- ✅ A maioria dos comentários nos vídeos de validação são **novos** e não foram vistos durante o treino/teste
- ✅ A validação testa o modelo em **produção real**, não no dataset local

**Conclusão**:
- A comparação de modelos (esta etapa) usa divisão ao nível de comentários para **comparar modelos entre si**
- A validação de generalização (próxima etapa) usa vídeos diferentes para **validar que o modelo generaliza para novos vídeos**
- Ambas as análises são válidas e complementares
- Veja `evaluation/01_reports/ARGUMENTO_GENERALIZACAO_MODELO_SELECIONADO.md` para argumentos detalhados sobre a relevância estatística

---

## 📚 Referências

- **Guia Completo**: `evaluation/scripts/CATALOG.md` (Seção 0)
- **Resumo da Comparação**: `MODEL_COMPARISON_SUMMARY.md`
- **Análise VADER**: `README_VADER_ANALYSIS.md`
- **Resultados Completos**: `results/comprehensive_model_comparison.txt`
- **Notebook Jupyter**: `notebooks/youtube_comments_sentiment_analysis_comparison.ipynb`

## Ver também

- [`../README.md`](../README.md) — índice da avaliação
- [`../02_graphs/MANIFEST.md`](../02_graphs/MANIFEST.md) — Tabela 1 (`comprehensive_model_comparison.txt`)

---

**Última Atualização**: Novembro 2025  
**Status**: ✅ Organização Completa


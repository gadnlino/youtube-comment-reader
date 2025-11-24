# Guia Completo - Scripts de Avaliação do YouTube Comment Reader

> **Documento de Referência Completo para Monografia**  
> Este guia consolida toda a documentação dos scripts utilizados nas avaliações do sistema, organizado por tipo de teste.

---

## 📋 Índice

0. [Comparação de Modelos de Análise de Sentimentos](#0-comparação-de-modelos-de-análise-de-sentimentos)
1. [Testes de Avaliação do Modelo Selecionado](#1-testes-de-avaliação-do-modelo-selecionado)
2. [Testes de Carga e Performance da API](#2-testes-de-carga-e-performance-da-api)
3. [Testes End-to-End do Frontend](#3-testes-end-to-end-do-frontend)

---

## 0. Comparação de Modelos de Análise de Sentimentos

> **⚠️ Ordem Cronológica**: Esta etapa foi executada **ANTES** da avaliação do modelo selecionado. Primeiro comparamos diferentes modelos para selecionar o melhor, depois avaliamos o modelo selecionado.

### 📍 Localização

**Scripts**: `evaluation/model_comparison/scripts/`  
**Resultados**: `evaluation/model_comparison/results/`  
**Notebooks**: `evaluation/model_comparison/notebooks/`  
**Documentação**: `evaluation/model_comparison/README.md`

### 🎯 Objetivo

Comparar diferentes modelos de análise de sentimento para selecionar o melhor modelo para o sistema, incluindo:
- Modelos baseados em regras (VADER, TextBlob)
- Modelos de Machine Learning tradicional (TF-IDF + Logistic Regression, TF-IDF + SVM)
- Modelos Transformer (DeBERTa, Twitter-XLM-RoBERTa)
- Métricas de desempenho (Accuracy, F1-Score, tempo de processamento)
- Seleção do modelo final baseado em desempenho e viabilidade

### 📁 Scripts Principais

> **⚠️ Importante**: Para reproduzir os resultados da Tabela 1 da monografia, execute os scripts individuais abaixo. Cada script gera os resultados específicos de um modelo usando o dataset completo (ou amostras grandes).

#### 1. TF-IDF + Logistic Regression (Modelo Selecionado)

**`tfidf_logistic_classification_report.py`**
- **Função**: Treina e avalia o modelo TF-IDF + Logistic Regression no dataset completo
- **Uso**: Estabelece o benchmark do modelo selecionado
- **Divisão de dados**: 80% treino / 20% teste (ao nível de comentários, `random_state=42`)
- **Dataset**: 1.032.225 comentários (dataset completo)
- **Resultados esperados**: 66.1% accuracy, 66.2% F1-Macro
- **Saída**: Métricas detalhadas, matriz de confusão, relatório de classificação
- **Execução**: 
  ```bash
  cd evaluation/model_comparison/scripts
  python tfidf_logistic_classification_report.py
  ```

#### 2. VADER (Rule-based)

**`vader_classification_report.py`**
- **Função**: Avalia o modelo VADER no dataset completo
- **Dataset**: 1.032.225 comentários (dataset completo)
- **Resultados esperados**: 53.4% accuracy, 52.9% F1-Macro
- **Execução**: 
  ```bash
  cd evaluation/model_comparison/scripts
  python vader_classification_report.py
  ```

#### 3. TextBlob (Rule-based)

**`textblob_classification_report.py`**
- **Função**: Avalia o modelo TextBlob no dataset completo
- **Dataset**: 1.032.225 comentários (dataset completo)
- **Resultados esperados**: 48.8% accuracy, 46.8% F1-Macro
- **Execução**: 
  ```bash
  cd evaluation/model_comparison/scripts
  python textblob_classification_report.py
  ```

#### 4. TF-IDF + SVM (Traditional ML)

**`svm_classification_report.py`**
- **Função**: Avalia o modelo TF-IDF + SVM
- **Dataset**: 50.000 comentários (amostra grande para treinamento mais rápido)
- **Resultados esperados**: 52.5% accuracy, 51.8% F1-Macro
- **Execução**: 
  ```bash
  cd evaluation/model_comparison/scripts
  python svm_classification_report.py
  ```

#### 5. Transformers (DeBERTa, Twitter-XLM-RoBERTa)

**Notebook**: `evaluation/model_comparison/notebooks/youtube_comments_sentiment_analysis_comparison.ipynb`
- **Função**: Análise de modelos Transformer
- **Resultados esperados**: 
  - DeBERTa-v3-small: 73.0% accuracy, 73.0% F1-Macro
  - Twitter-XLM-RoBERTa: 71.0% accuracy, 71.0% F1-Macro
- **Execução**: Abrir e executar o notebook Jupyter

### 🚀 Como Executar - Passo a Passo para Reproduzir a Tabela 1

> **📋 Objetivo**: Reproduzir os resultados da Tabela 1 - Comparação dos modelos de classificação de sentimento da monografia.

#### Pré-requisitos

```bash
# Instalar dependências
cd evaluation/model_comparison/scripts
pip install -r requirements.txt
pip install textblob nltk

# Configuração do NLTK (para VADER) - executar uma vez
python fix_nltk_ssl.py
python -c "import nltk; nltk.download('vader_lexicon')"
```

#### Passo a Passo para Reproduzir os Resultados

**1. TF-IDF + Logistic Regression (66.1% accuracy, 66.2% F1-Macro)**
```bash
cd evaluation/model_comparison/scripts
python tfidf_logistic_classification_report.py
```
- **Tempo estimado**: ~100-200 segundos
- **Resultado**: Salvo em `../results/tfidf_logistic_results.txt`
- **Dataset**: 1.032.225 comentários (dataset completo)
- **Divisão**: 80% treino / 20% teste ao nível de **comentários individuais** (não vídeos)
- **Nota**: Este script estabelece o **benchmark** do modelo selecionado que será usado posteriormente na validação (`compare_metrics_vs_benchmark.py`).
- **⚠️ Importante - Generalização**: A divisão ao nível de comentários significa que comentários do mesmo vídeo podem estar tanto no treino quanto no teste. Isso é adequado para **comparar modelos**, mas a **validação de generalização para vídeos diferentes** é feita posteriormente nos scripts de `scripts/01_model_evaluation/`, que usam vídeos completos diferentes via API em produção.

**2. VADER (53.4% accuracy, 52.9% F1-Macro)**
```bash
cd evaluation/model_comparison/scripts
python vader_classification_report.py
```
- **Tempo estimado**: ~100 segundos
- **Resultado**: Salvo em `../results/vader_results_full_dataset.txt`
- **Dataset**: 1.032.225 comentários (dataset completo)
- **Nota**: O script executa com diferentes tamanhos de amostra. O resultado do dataset completo é o que aparece na tabela.
- **⚠️ Importante**: Modelos rule-based (VADER, TextBlob) não fazem divisão train/test, pois não são modelos treinados. Eles são avaliados diretamente em todo o dataset.

**3. TextBlob (48.8% accuracy, 46.8% F1-Macro)**
```bash
cd evaluation/model_comparison/scripts
python textblob_classification_report.py
```
- **Tempo estimado**: ~95 segundos
- **Resultado**: Salvo em `../results/textblob_results_full_dataset.txt`
- **Dataset**: 1.032.225 comentários (dataset completo)
- **⚠️ Importante**: Modelos rule-based não fazem divisão train/test, pois não são modelos treinados.

**4. TF-IDF + SVM (52.5% accuracy, 51.8% F1-Macro)**
```bash
cd evaluation/model_comparison/scripts
python svm_classification_report.py
```
- **Tempo estimado**: Varia conforme hardware (usa 50k amostras)
- **Resultado**: Salvo em `../results/svm_results_*.txt`
- **Dataset**: 50.000 comentários (amostra grande para treinamento mais rápido)
- **Divisão**: 80% treino / 20% teste ao nível de **comentários individuais** (não vídeos)
- **⚠️ Importante - Generalização**: Ver nota do TF-IDF + Logistic Regression acima.

**5. Transformers (DeBERTa: 73.0%, Twitter-XLM-RoBERTa: 71.0%)**
- **Execução**: Abrir e executar o notebook Jupyter
  ```bash
  cd evaluation/model_comparison/notebooks
  jupyter notebook youtube_comments_sentiment_analysis_comparison.ipynb
  ```
- **Tempo estimado**: ~20-30 minutos por modelo (requer GPU recomendado)

#### Ordem Recomendada de Execução

1. **Primeiro**: Execute os modelos rule-based (VADER, TextBlob) - são mais rápidos
2. **Segundo**: Execute os modelos Traditional ML (TF-IDF + LR, TF-IDF + SVM)
3. **Terceiro**: Execute os Transformers (se tiver recursos computacionais)

#### Consolidação dos Resultados

Após executar todos os scripts, os resultados estarão em:
- `evaluation/model_comparison/results/` - Arquivos de texto com métricas detalhadas
- Os valores podem ser consolidados manualmente na tabela comparativa

### 📊 Resultados

#### Onde os Resultados são Salvos

- **Arquivos de texto**: Resultados são salvos em `evaluation/model_comparison/results/*.txt`
- **Arquivos Markdown**: Resumos em `evaluation/model_comparison/` (raiz)
- **Modelos salvos**: Modelos treinados são salvos como arquivos `.pkl` (se configurado, na pasta de scripts)

#### Resultados Principais Obtidos

**Modelo Selecionado: TF-IDF + Logistic Regression**

- **Accuracy**: 66.14%
- **F1-Score (Macro)**: 66.28%
- **Precision (Macro)**: 66.64%
- **Recall (Macro)**: 66.14%
- **Dataset Utilizado**: 1.032.225 comentários
- **Divisão Train/Test**: 80/20 (ao nível de comentários, `random_state=42`)
- **Tempo de Processamento**: ~100-200 segundos (dependendo do hardware)

**Comparação com Outros Modelos**:

| Modelo | Accuracy | F1 (Macro) | Velocidade | Tipo |
|--------|----------|------------|------------|------|
| VADER | ~53% | ~53% | Muito Rápido | Rule-based |
| TextBlob | ~50% | ~50% | Muito Rápido | Rule-based |
| TF-IDF + LR | **66.14%** | **66.28%** | Rápido | Traditional ML |
| TF-IDF + SVM | ~65% | ~65% | Médio | Traditional ML |
| Transformers | ~71-73% | ~71-73% | Lento | Deep Learning |

**Decisão**: TF-IDF + Logistic Regression foi selecionado por oferecer o melhor equilíbrio entre desempenho, velocidade e viabilidade de deploy em produção.

### ⚠️ Notas Importantes sobre a Divisão de Dados e Generalização

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
- ✅ A **validação de generalização para vídeos diferentes** é feita **separadamente** nos scripts de `scripts/01_model_evaluation/`
- ✅ A validação usa **vídeos completos diferentes** buscados via API em produção
- ✅ Os vídeos usados na validação são **diferentes** dos vídeos usados na comparação
- ✅ A maioria dos comentários nos vídeos de validação são **novos** e não foram vistos durante o treino/teste
- ✅ A validação testa o modelo em **produção real**, não no dataset local

**Conclusão**:
- A comparação de modelos (esta etapa) usa divisão ao nível de comentários para **comparar modelos entre si**
- A validação de generalização (próxima etapa) usa vídeos diferentes para **validar que o modelo generaliza para novos vídeos**
- Ambas as análises são válidas e complementares
- Veja `evaluation/ARGUMENTO_GENERALIZACAO_MODELO_SELECIONADO.md` para argumentos detalhados sobre a relevância estatística

### 📝 Notas Importantes

- Todos os scripts devem ser executados a partir da pasta `evaluation/model_comparison/scripts/`
- O dataset é baixado automaticamente usando `kagglehub` na primeira execução
- Os scripts são **reproduzíveis** - ao executá-los, novos resultados serão gerados
- O benchmark estabelecido aqui é usado posteriormente na validação do modelo

### 🔗 Referências Adicionais

- **Documentação principal**: `evaluation/model_comparison/README.md`
- **Resumo da comparação**: `evaluation/model_comparison/MODEL_COMPARISON_SUMMARY.md`
- **Resultados completos**: `evaluation/model_comparison/results/comprehensive_model_comparison.txt`
- **Análise VADER**: `evaluation/model_comparison/README_VADER_ANALYSIS.md`
- **Notebook Jupyter**: `evaluation/model_comparison/notebooks/youtube_comments_sentiment_analysis_comparison.ipynb`

---

## 1. Testes de Avaliação do Modelo Selecionado

### 📍 Localização

**Scripts**: `evaluation/scripts/01_model_evaluation/`  
**Dados e Resultados Completos**: `evaluation/model_analysis/`  
  - **Scripts originais**: `evaluation/model_analysis/scripts/`  
  - **Resultados**: `evaluation/model_analysis/results/`  
  - **Gráficos**: `evaluation/model_analysis/graphs/`  
  - **Logs**: `evaluation/model_analysis/logs/`  
  - **Relatórios**: `evaluation/model_analysis/reports/`  
**Resultados de Referência**: `evaluation/scripts/01_model_evaluation/results/` e `graphs/`

### 🎯 Objetivo

> **⚠️ Ordem Cronológica**: Esta etapa foi executada **DEPOIS** da comparação de modelos. Após selecionar o modelo TF-IDF + Logistic Regression, validamos seu desempenho em vídeos diferentes.

Avaliar e validar o modelo de classificação de sentimento (TF-IDF + Logistic Regression) **selecionado na etapa anterior**, incluindo:
- Acurácia do modelo comparado ao ground truth do dataset
- Métricas de desempenho (Accuracy, Precision, Recall, F1-Score)
- Análise de impacto do idioma na classificação
- Geração de visualizações (matriz de confusão, gráficos comparativos)

### 📁 Scripts Disponíveis

#### Validação de Métricas

**`compare_metrics_vs_benchmark.py`**
- **Função**: Compara as métricas básicas (Accuracy, Precision, Recall, F1-Score) da validação atual com o benchmark inicial
- **Valida**: Se o modelo mantém o desempenho observado durante a seleção
- **Uso**: Validação de desempenho do modelo
- **📊 Relevância Estatística**: 
  - Na comparação de modelos (`model_comparison/`), o `train_test_split` foi feito ao nível de **comentários individuais** (não vídeos), com `random_state=42` e `test_size=0.2` (80/20).
  - Este script seleciona **vídeos aleatoriamente diferentes** de `working_videos_*.json` (com `random.seed(42)`).
  - **A análise mantém relevância estatística** porque: (1) usa 145 vídeos diferentes (~72.500 comentários), (2) os vídeos são diferentes dos usados na comparação, (3) testa o modelo em produção via API, e (4) demonstra que o modelo mantém desempenho em vídeos diferentes, validando a capacidade de generalização.

**`validate_model_accuracy_with_dataset.py`**
- **Função**: Valida a acurácia do modelo comparando predições da API com ground truth do dataset
- **Valida**: Acurácia comentário por comentário
- **Uso**: Validação detalhada de acurácia
- **📊 Relevância Estatística**: 
  - Na comparação de modelos (`model_comparison/`), o `train_test_split` foi feito ao nível de **comentários individuais** (não vídeos), com `random_state=42` e `test_size=0.2` (80/20).
  - Este script de validação usa **vídeos completos diferentes** de `test_3_videos.json` ou `dataset_videos_for_accuracy_validation.json`.
  - **A análise mantém relevância estatística** porque: (1) os vídeos são diferentes dos usados na comparação, (2) a maioria dos comentários são novos, (3) testa o modelo em produção via API, e (4) demonstra generalização para vídeos diferentes, que é o objetivo principal da validação.

#### Análise de Idioma

**`language_impact_analysis.py`**
- **Função**: Analisa o impacto do idioma na classificação de sentimento
- **Identifica**: Viés linguístico do modelo
- **Uso**: Análise de viés por idioma

**`multilingual_sentiment_analysis.py`**
- **Função**: Análise detalhada de sentimento em múltiplos idiomas
- **Uso**: Análise multilíngue completa

**`analyze_video_language.py`**
- **Função**: Analisa o perfil de idioma dos vídeos
- **Uso**: Classificação de idioma dos vídeos

#### Geração de Visualizações

**`generate_confusion_matrix.py`**
- **Função**: Gera matriz de confusão do modelo
- **Saída**: Gráfico PNG da matriz de confusão
- **Uso**: Visualização de erros de classificação

**`generate_consolidated_distribution_analysis.py`**
- **Função**: Gera análises consolidadas de distribuição
- **Uso**: Análise consolidada de distribuições

**`generate_metrics_comparison_table.py`**
- **Função**: Gera tabela e gráfico comparando métricas do benchmark vs validação
- **Saída**: Tabela e gráfico PNG
- **Uso**: Comparação visual de métricas

**`generate_language_analysis_graphs.py`**
- **Função**: Gera gráficos de análise de idioma
- **Uso**: Visualização de análise de idioma

**`generate_language_analysis_graphs_pt.py`**
- **Função**: Gera gráficos de análise de idioma (versão em português)
- **Uso**: Visualização de análise de idioma em português

**`generate_sentiment_distribution_by_language.py`**
- **Função**: Gera gráficos de distribuição de sentimento por idioma
- **Uso**: Visualização de distribuição por idioma

#### Utilitários

**`pre_filter_working_videos.py`**
- **Função**: Pré-filtra vídeos que funcionam com a API para uso nas validações
- **Uso**: Preparação de dados para validação

### 🚀 Como Executar

#### Pré-requisitos

```bash
pip install pandas numpy scikit-learn matplotlib seaborn requests scipy
```

#### Executar um Script

```bash
# Navegar para a pasta dos scripts
cd evaluation/scripts/01_model_evaluation

# Executar um script específico
python compare_metrics_vs_benchmark.py
python validate_model_accuracy_with_dataset.py
python language_impact_analysis.py
python multilingual_sentiment_analysis.py
python generate_confusion_matrix.py
python generate_metrics_comparison_table.py
python generate_language_analysis_graphs_pt.py

# OU executar os scripts originais em model_analysis/scripts/
cd evaluation/model_analysis/scripts
python compare_metrics_vs_benchmark.py
# ... etc
```

#### Estrutura de Dados Necessários

Os scripts esperam encontrar os seguintes arquivos:

- **Dataset com ground truth**: `youtube_comments_cleaned.csv`
  - Localização típica: `../api_load_testing/` ou `../../03_data/csv/`
  - Contém os comentários com classificação de sentimento (ground truth)

- **Listas de vídeos**: Arquivos JSON
  - Localização típica: `../model_analysis/data/` ou `../../03_data/json/`
  - Exemplos: `working_videos_*.json`, `dataset_videos_*.json`

**Nota**: Os scripts tentam encontrar automaticamente os arquivos em diferentes locais. Se necessário, ajuste os caminhos nos scripts.

**⚠️ Importante - Separação de Dados e Relevância Estatística**: 

**Como a divisão foi feita na comparação de modelos (etapa anterior):**
- Na pasta `model_comparison/`, o `train_test_split` foi feito ao nível de **comentários individuais** (não vídeos)
- Divisão: 80% treino / 20% teste, com `random_state=42`
- Dataset completo: 1.032.225 comentários
  - Treino: ~825.780 comentários (80%)
  - Teste: ~206.445 comentários (20%)
- Isso significa que comentários do mesmo vídeo podem estar tanto no treino quanto no teste original

**Como a validação foi feita (esta etapa):**
- Os scripts de validação (`validate_model_accuracy_with_dataset.py` e `compare_metrics_vs_benchmark.py`) usam **vídeos completos diferentes** do dataset
- Os vídeos selecionados para validação são diferentes dos vídeos usados na comparação de modelos
- A validação testa o modelo em produção (via API), não no dataset local
- Vídeos testados: 145 vídeos diferentes
- Comentários buscados: ~72.500 comentários
- Comentários validados (matched): 917 comentários

**Relevância Estatística e Generalização:**
✅ **A análise mantém relevância estatística e o argumento de generalização é válido** pelos seguintes motivos:

1. **Vídeos Diferentes**: Os vídeos usados na validação são diferentes dos vídeos usados na comparação de modelos. Isso é o aspecto mais importante para demonstrar generalização - o modelo é testado em vídeos completamente novos.

2. **Validação em Produção**: A validação testa o modelo através da API em produção, não no dataset local. Isso valida o comportamento real do sistema.

3. **Maioria dos Comentários são Novos**: Mesmo que alguns comentários individuais de um vídeo possam ter estado no test set original (devido à divisão ao nível de comentários), a maioria dos comentários nos vídeos de validação são novos e não foram vistos durante o treino/teste.

4. **Treino ao Nível de Comentários**: O modelo foi treinado em comentários individuais, não em vídeos completos. Portanto, testar em vídeos completos diferentes ainda é uma validação válida de generalização.

5. **Amostra Maior e Mais Diversa**: A validação usa uma amostra maior (145 vídeos, ~72.500 comentários) e mais diversa, fornecendo evidência robusta de que o modelo mantém desempenho em vídeos diferentes.

**Conclusão**: A possível sobreposição parcial de alguns comentários individuais não invalida o argumento de que o modelo generaliza para vídeos diferentes, pois os vídeos são diferentes e a validação testa o modelo em um contexto de produção real.

**📚 Documento de Referência**: Para argumentos detalhados sobre a relevância estatística, consulte `evaluation/ARGUMENTO_GENERALIZACAO_MODELO_SELECIONADO.md`.

### 📊 Resultados

#### Onde os Resultados são Salvos

- **Arquivos JSON**: Resultados das análises são salvos em `evaluation/model_analysis/results/`
- **Gráficos PNG**: Visualizações são salvas em `evaluation/model_analysis/graphs/`
- **Logs**: Arquivos de log são salvos em `evaluation/model_analysis/logs/`
- **Relatórios TXT**: Relatórios de análise são salvos em `evaluation/model_analysis/reports/`
- **Resultados de Referência**: Cópias dos resultados mais recentes estão em `evaluation/scripts/01_model_evaluation/results/` e `graphs/`

#### Resultados Principais Obtidos

- **Acurácia do Modelo**: 66.14%
- **F1-Score**: 66.28%
- **Precision**: 66.64%
- **Recall**: 66.14%
- **Dataset Utilizado**: 1.032.225 comentários
- **Divisão Train/Test**: 80/20

#### Arquivos de Referência Disponíveis

Na pasta `evaluation/scripts/01_model_evaluation/`:

**Resultados (JSON)**:
- `results/metrics_comparison_benchmark_20251122_150310.json` - Comparação de métricas mais recente

**Gráficos (PNG)**:
- `graphs/confusion_matrix_reference.png` - Matriz de confusão do modelo
- `graphs/metrics_comparison_benchmark_20251122_151341.png` - Comparação de métricas

### 📝 Notas Importantes

- Todos os scripts assumem que você está executando a partir da pasta `evaluation/scripts/01_model_evaluation/` ou `evaluation/`
- Os arquivos de dados podem estar em diferentes locais - os scripts tentam encontrar automaticamente
- Os scripts criam automaticamente as pastas necessárias (`data/`, `results/`, `graphs/`) se não existirem
- Os scripts são **reproduzíveis** - ao executá-los, novos resultados serão gerados nas pastas originais

### 🔗 Referências Adicionais

- **Todos os resultados históricos**: `evaluation/model_analysis/results/` e `evaluation/model_analysis/graphs/`
- **Relatórios de avaliação**: `evaluation/01_reports/`
- **Dados brutos**: `evaluation/03_data/`

---

## 2. Testes de Carga e Performance da API

### 📍 Localização

**Scripts**: `evaluation/scripts/02_api_performance/`  
**Dados e Resultados Completos**: `evaluation/api_load_testing/`  
  - **Scripts originais**: `evaluation/api_load_testing/scripts/`  
  - **Resultados**: `evaluation/api_load_testing/results/`  
  - **Gráficos**: `evaluation/api_load_testing/graphs/`  
  - **Gráficos Consolidados**: `evaluation/api_load_testing/consolidated_graphs/`  
  - **Logs**: `evaluation/api_load_testing/logs/`  
  - **Documentação**: `evaluation/api_load_testing/docs/`  
**Resultados de Referência**: `evaluation/scripts/02_api_performance/results/` e `graphs/`

### 🎯 Objetivo

Avaliar o desempenho, escalabilidade e capacidade de carga da API intermediária do YouTube Comment Reader, incluindo:
- Tempo de resposta (média, mínimo, máximo, percentis P95, P99)
- Throughput (requisições por segundo - RPS/TPS)
- Comportamento sob carga (múltiplos usuários simultâneos)
- Estabilidade temporal (performance ao longo do tempo)
- Comparação cold start vs warm Lambda
- Impacto de diferentes tamanhos de lote (batch size)

### 📁 Scripts Disponíveis

#### Testes Básicos de Performance

**`common.py`**
- **Função**: Funções utilitárias compartilhadas
- **Contém**: Funções HTTP, cálculo de métricas, geração de gráficos
- **Uso**: Importado por outros scripts

**`videos.py`**
- **Função**: Testes de listagem de vídeos
- **Endpoint testado**: `/videos/search`
- **Métricas**: Tempo de resposta, taxa de sucesso
- **Uso**: Avaliar performance da busca de vídeos

**`comments.py`**
- **Função**: Testes de listagem de comentários
- **Endpoint testado**: `/comments`
- **Métricas**: Tempo de resposta, taxa de sucesso, impacto de batch size
- **Uso**: Avaliar performance do carregamento de comentários

**`stability.py`**
- **Função**: Teste de estabilidade temporal
- **Método**: Executa requisições ao longo do tempo para verificar degradação
- **Métricas**: Performance ao longo do tempo, tendências
- **Uso**: Avaliar estabilidade da API

**`run_all.py`**
- **Função**: Script principal que executa todos os testes
- **Executa**: `videos.py`, `comments.py`, `stability.py`
- **Gera**: Resumo executivo de todos os testes
- **Uso**: Executar bateria completa de testes

#### Testes de Carga com Locust

**`locust_test.py`**
- **Função**: Teste de carga básico usando Locust
- **Ferramenta**: Locust (framework Python para testes de carga)
- **Uso**: Simular múltiplos usuários simultâneos
- **Execução**: `locust -f locust_test.py --host=API_URL`

**`locust_max_tps.py`**
- **Função**: Teste de carga para encontrar TPS máximo
- **Objetivo**: Determinar o limite de throughput da API
- **Uso**: Encontrar capacidade máxima
- **Execução**: `locust -f locust_max_tps.py --host=API_URL`

**`run_max_tps_test.sh`**
- **Função**: Script shell para executar teste de TPS máximo
- **Uso**: Facilitar execução do teste de TPS máximo
- **Execução**: `./run_max_tps_test.sh`

#### Geração de Gráficos e Relatórios

**`generate_consolidated_graphs.py`**
- **Função**: Gera gráficos consolidados de todos os testes
- **Saída**: Gráficos PNG consolidados
- **Uso**: Visualização consolidada de resultados

**`generate_locust_graphs.py`**
- **Função**: Gera gráficos a partir dos resultados do Locust
- **Saída**: Gráficos PNG dos testes de carga
- **Uso**: Visualização de testes de carga

**`generate_e2e_test_table.py`**
- **Função**: Gera tabela de resultados dos testes E2E
- **Saída**: Tabela PNG
- **Uso**: Visualização de resultados E2E

### 🚀 Como Executar

#### Pré-requisitos

```bash
pip install requests matplotlib seaborn numpy pandas locust
```

#### Executar Todos os Testes

```bash
# Navegar para a pasta dos scripts
cd evaluation/scripts/02_api_performance

# Executar todos os testes e gerar resumo
python run_all.py

# OU executar os scripts originais em api_load_testing/scripts/
cd evaluation/api_load_testing/scripts
python run_all.py
```

#### Executar Testes Individuais

```bash
# Testes de vídeos
python videos.py

# Testes de comentários
python comments.py

# Teste de estabilidade
python stability.py
```

#### Testes de Carga com Locust

```bash
# Teste básico
locust -f locust_test.py --host=https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod

# Teste de TPS máximo
./run_max_tps_test.sh
# ou diretamente
locust -f locust_max_tps.py --host=https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod
```

#### Gerar Gráficos Consolidados

```bash
python generate_consolidated_graphs.py
```

### ⚙️ Configuração

Antes de executar os testes, é necessário configurar:

#### 1. URL da API

Edite o arquivo `common.py` e ajuste:

```python
API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod"
```

#### 2. Vídeos para Teste

Edite os arquivos `comments.py` e `videos.py` com IDs de vídeos apropriados:

```python
VIDEOS = {
    'poucos': {
        'id': 'VIDEO_ID_AQUI',  # Vídeo com < 100 comentários
        'name': 'Poucos Comentários (< 100)'
    },
    'medio': {
        'id': 'VIDEO_ID_AQUI',  # Vídeo com 300-800 comentários
        'name': 'Volume Intermediário (300-800)'
    },
    'muitos': {
        'id': 'VIDEO_ID_AQUI',  # Vídeo com > 1.500 comentários
        'name': 'Alto Volume (> 1.500)'
    }
}
```

#### 3. Parâmetros de Teste de Estabilidade

Edite o arquivo `stability.py`:

```python
TEST_ENDPOINT = '/video/comments'  # ou '/search'
TEST_PARAMS = {
    'videoId': 'VIDEO_ID_AQUI',  # Se usar /video/comments
    # ... outros parâmetros
}
DURATION_MINUTES = 60  # Duração do teste
```

### 📊 Resultados

#### Onde os Resultados são Salvos

- **Arquivos CSV**: Dados brutos dos testes são salvos em `evaluation/api_load_testing/results/`
- **Arquivos JSON**: Resumos estatísticos são salvos em `evaluation/api_load_testing/results/`
- **Gráficos PNG**: Visualizações são salvas em `evaluation/api_load_testing/graphs/` ou `evaluation/api_load_testing/consolidated_graphs/`
- **Relatórios HTML**: Relatórios do Locust são salvos em `evaluation/api_load_testing/results/`
- **Logs**: Arquivos de log são salvos em `evaluation/api_load_testing/logs/`
- **Resultados de Referência**: Cópias dos resultados mais recentes estão em `evaluation/scripts/02_api_performance/results/` e `graphs/`

#### Resultados Principais Obtidos

- **Tempo médio de resposta**: ~1.024ms
- **Throughput máximo**: ~10-15 TPS (Transactions Per Second)
- **Taxa de sucesso**: 100% (sob carga normal)
- **Suporte a usuários simultâneos**: 50-100 usuários
- **Percentis**: P95 ~3.800ms, P99 ~4.100ms

#### Arquivos de Referência Disponíveis

Na pasta `evaluation/scripts/02_api_performance/`:

**Resultados (JSON)**:
- `results/perf_summary_20251122_172250.json` - Resumo de performance mais recente

**Gráficos Consolidados (PNG)**:
- `graphs/consolidated_graphs_part1.png` - Gráficos consolidados parte 1
- `graphs/consolidated_graphs_part2.png` - Gráficos consolidados parte 2
- `graphs/consolidated_table_only.png` - Tabela consolidada
- `graphs/endpoint_comparison.png` - Comparação de endpoints
- `graphs/response_time_comparison.png` - Comparação de tempos de resposta
- `graphs/success_rate_comparison.png` - Comparação de taxas de sucesso
- `graphs/tps_comparison.png` - Comparação de TPS (Throughput)

### 📝 Scripts Adicionais

Existem scripts complementares em `evaluation/04_scripts/tests/` que fornecem testes mais específicos:

- **`extended_benchmark.py`**: Teste estendido com mais requisições (219 requisições)
- **`heavy_load_test.py`**: Teste de carga pesada (10.600 comentários)
- **`multi_video_benchmark.py`**: Benchmark com múltiplos vídeos
- **`batch_size_analysis.py`**: Análise de impacto do tamanho do lote
- **`performance_benchmark.py`**: Benchmark básico de performance
- **`quick_test.py`**: Teste rápido de verificação

Esses scripts podem ser executados diretamente de `evaluation/04_scripts/tests/` ou copiados para a pasta de scripts se necessário.

### 📝 Notas Importantes

- Os scripts são **reproduzíveis** - ao executá-los, novos resultados serão gerados nas pastas originais
- Os testes de carga com Locust requerem que a API esteja acessível
- Os testes podem levar vários minutos para completar, especialmente os testes de estabilidade
- Os resultados incluem timestamps para rastreabilidade

### 🔗 Referências Adicionais

- **Todos os resultados históricos**: `evaluation/api_load_testing/results/` e `evaluation/api_load_testing/graphs/`
- **Relatório de testes de carga**: `evaluation/api_load_testing/RELATORIO_TESTES_CARGA.md`
- **Relatórios de avaliação**: `evaluation/01_reports/`
- **Dados brutos**: `evaluation/03_data/`

---

## 3. Testes End-to-End do Frontend

### 📍 Localização

**Scripts**: `packages/frontend/integration_test/tests/` (na raiz do projeto, não em `evaluation/`)  
**Documentação**: `packages/frontend/integration_test/docs/`  
**README**: `packages/frontend/integration_test/README.md`

> **Nota Importante**: Os testes do frontend estão localizados na pasta do frontend do projeto, não na pasta de avaliação, pois fazem parte do código do aplicativo Flutter.

### 🎯 Objetivo

Validar a interface do usuário e o fluxo completo do aplicativo mobile Flutter, incluindo:
- Renderização real da interface gráfica
- Simulação de interações do usuário (taps, scrolls, text input)
- Navegação entre telas
- Funcionalidades (favoritos, filtros, etc.)
- Integração completa frontend → API → análise de sentimento
- Validação do fluxo completo do usuário no aplicativo mobile

### 📁 Scripts Disponíveis

#### Testes Principais

**`critical_user_flows_test.dart`**
- **Função**: Testa fluxos críticos do usuário
- **Testes**: 7 testes principais
- **Cobre**: Busca, carregamento, filtragem, favoritos, navegação
- **Uso**: Validação dos fluxos mais importantes

**`comprehensive_e2e_test.dart`**
- **Função**: Testes abrangentes do sistema
- **Testes**: 6 cenários
- **Cobre**: Funcionalidades principais
- **Uso**: Teste completo do sistema

**`extended_features_test.dart`**
- **Função**: Testa funcionalidades estendidas
- **Testes**: 6 testes
- **Cobre**: Favoritos, múltiplos filtros, ordenação
- **Uso**: Validação de funcionalidades avançadas

**`complete_all_features_test.dart`**
- **Função**: Cobertura completa de todas as funcionalidades
- **Testes**: 14 testes
- **Cobre**: Todas as funcionalidades do aplicativo
- **Uso**: Teste completo de cobertura

**`app_test.dart`**
- **Função**: Testes básicos do aplicativo
- **Testes**: 8 testes
- **Uso**: Testes iniciais e básicos

**`app_smoke_test.dart`**
- **Função**: Testes de smoke (verificação rápida)
- **Testes**: 4 testes
- **Uso**: Verificação rápida de funcionalidade básica

**`app_final_test.dart`**
- **Função**: Testes finais do aplicativo
- **Testes**: 5 testes
- **Uso**: Validação final antes de release

**`app_with_firebase_test.dart`**
- **Função**: Testes com integração Firebase
- **Testes**: 4 testes
- **Uso**: Validação de integração com Firebase

### 🚀 Como Executar

#### Pré-requisitos

1. **Flutter SDK** instalado (versão >= 3.1.5)
2. **Emulador Android/iOS** ou dispositivo físico conectado
3. **Dependências do projeto** instaladas

```bash
# Instalar dependências
cd packages/frontend
flutter pub get
```

#### Executar os Testes

##### Opção 1: Teste Rápido (sem device)

Para testar a lógica sem renderizar em device/emulador:

```bash
cd packages/frontend
flutter test integration_test/tests/app_test.dart
```

##### Opção 2: Teste Completo (com device/emulador)

Para rodar com renderização real em device ou emulador:

```bash
cd packages/frontend

# 1. Certifique-se de que um emulador está rodando ou device conectado
flutter devices

# 2. Execute os testes
flutter drive \
  --driver=test_driver/integration_test.dart \
  --target=integration_test/tests/app_test.dart
```

##### Opção 3: Teste em Device Específico

```bash
# Listar devices disponíveis
flutter devices

# Executar em device específico
flutter drive \
  --driver=test_driver/integration_test.dart \
  --target=integration_test/tests/app_test.dart \
  -d <device_id>
```

##### Opção 4: Executar Todos os Testes

```bash
cd packages/frontend
flutter test integration_test/tests/
```

### 📊 Resultados

#### Resultados Principais Obtidos

- **Cobertura**: 25+ funcionalidades testadas
- **Taxa de sucesso**: 90%+
- **Validação**: UI renderizada, interações do usuário, API, análise de sentimento, persistência

#### Cenários de Teste Implementados

1. **Busca de vídeos**: Busca e exibição de resultados
2. **Carregamento de comentários**: Com e sem análise de sentimento
3. **Filtragem por sentimento**: Positivo, negativo, neutro (validação de 100% de acurácia)
4. **Favoritos**: Adicionar/remover vídeos e comentários dos favoritos
5. **Navegação**: Navegação entre telas e tabs
6. **Tratamento de erros**: Comportamento com entradas inválidas
7. **Múltiplos filtros**: Filtros simultâneos
8. **Ordenação**: Ordenação por relevância e data

### 🛠️ Tecnologias Usadas

- **Flutter SDK**: Framework mobile multiplataforma
- **integration_test**: Pacote oficial do Flutter para testes E2E
- **WidgetTester**: Ferramenta para simular interações de usuário
- **Simulação de gestos**: Taps, scroll, text input
- **Renderização real**: Widgets são realmente renderizados

### 📝 Notas Importantes

- Os testes requerem um emulador ou dispositivo físico conectado para renderização real
- Os testes podem levar vários minutos para completar
- Os testes validam a integração completa: UI → API → Análise de Sentimento
- Os testes são **reproduzíveis** e podem ser executados em qualquer momento

### 🔗 Referências Adicionais

- **Documentação completa**: `packages/frontend/integration_test/README.md`
- **Relatórios de teste**: `packages/frontend/integration_test/docs/*_REPORT.md`
- **Guia de execução**: `packages/frontend/integration_test/docs/HOW_TO_RUN_TESTS.md`
- **Relatórios de avaliação**: `evaluation/01_reports/`

---

## 📚 Referências Gerais

### Estrutura de Pastas

```
evaluation/
├── model_comparison/                 # Scripts de comparação de modelos (ETAPA 0)
│   ├── scripts/                      # Scripts Python
│   ├── results/                      # Resultados (arquivos .txt)
│   ├── notebooks/                    # Notebooks Jupyter
│   └── README.md                     # Documentação
│
├── scripts/                          # Scripts organizados por categoria
│   ├── 01_model_evaluation/         # Scripts de avaliação do modelo selecionado (ETAPA 1)
│   │   ├── results/                 # Resultados de referência (JSON)
│   │   ├── graphs/                  # Gráficos de referência (PNG)
│   │   └── *.py                     # Scripts de avaliação
│   ├── 02_api_performance/          # Scripts de testes de carga/performance (ETAPA 2)
│   │   ├── results/                 # Resultados de referência (JSON)
│   │   ├── graphs/                  # Gráficos consolidados de referência (PNG)
│   │   └── *.py                     # Scripts de testes
│   └── README.md                     # Documentação consolidada
│
├── model_analysis/                   # Dados e resultados completos do modelo
│   ├── scripts/                     # Scripts Python originais
│   ├── results/                     # Resultados JSON
│   ├── graphs/                      # Gráficos PNG
│   ├── logs/                         # Arquivos de log
│   ├── reports/                      # Relatórios TXT
│   ├── data/                         # Dados de entrada (JSON)
│   └── README.md                     # Documentação
│
├── api_load_testing/                 # Dados e resultados completos da API
│   ├── scripts/                     # Scripts Python originais
│   ├── results/                     # Resultados CSV/JSON/HTML
│   ├── graphs/                      # Gráficos PNG
│   ├── consolidated_graphs/         # Gráficos consolidados
│   ├── logs/                         # Arquivos de log
│   ├── docs/                         # Documentação adicional
│   ├── teste_1/, teste_2/, etc.     # Resultados de testes específicos
│   └── README.md                     # Documentação
│
├── 01_reports/                       # Relatórios de avaliação
├── 02_graphs/                        # Gráficos finais (português/inglês)
└── 03_data/                          # Dados brutos consolidados

packages/frontend/integration_test/   # Testes E2E do frontend (Flutter) (ETAPA 3)
├── tests/                            # Scripts de teste Dart
├── docs/                             # Documentação e relatórios
└── README.md                         # Documentação principal
```

### Dependências Gerais

#### Para Scripts Python (Modelo e API)

```bash
pip install requests pandas numpy matplotlib seaborn scikit-learn scipy locust
```

#### Para Testes do Frontend

```bash
cd packages/frontend
flutter pub get
```

### 📖 Para a Monografia

Este guia pode ser referenciado na monografia como:

> "Os scripts de avaliação estão organizados em `evaluation/scripts/` e podem ser executados para reproduzir todos os resultados apresentados nesta monografia. A documentação completa está disponível em `evaluation/GUIA_COMPLETO_SCRIPTS_AVALIACAO.md`."

**Estrutura de Referência Sugerida**:

0. **Comparação de Modelos**: Scripts em `evaluation/model_comparison/`
1. **Avaliação do Modelo Selecionado**: Scripts em `evaluation/scripts/01_model_evaluation/`
2. **Avaliação de Performance**: Scripts em `evaluation/scripts/02_api_performance/`
3. **Testes E2E do Frontend**: Scripts em `packages/frontend/integration_test/`

Todos os scripts são **reproduzíveis** e podem ser executados para validar os resultados apresentados na monografia.

---

**Última Atualização**: Novembro 2025  
**Versão**: 1.0  
**Status**: ✅ Documentação Completa e Consolidada


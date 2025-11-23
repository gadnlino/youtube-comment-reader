# Guia de Referência - Scripts de Avaliação

> **Documento de Referência para Monografia**  
> Este documento serve como referência completa para todos os scripts utilizados nas avaliações do sistema YouTube Comment Reader.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura de Organização](#estrutura-de-organização)
3. [Avaliação do Modelo de Análise de Sentimentos](#1-avaliação-do-modelo-de-análise-de-sentimentos)
4. [Avaliação de Performance da API](#2-avaliação-de-performance-da-api)
5. [Testes End-to-End do Frontend](#3-testes-end-to-end-do-frontend)
6. [Como Referenciar na Monografia](#como-referenciar-na-monografia)

---

## Visão Geral

Este documento organiza e descreve todos os scripts utilizados para as avaliações do sistema YouTube Comment Reader, incluindo:

- ✅ Avaliação do modelo de análise de sentimentos
- ✅ Testes de carga e performance da API
- ✅ Testes end-to-end do frontend (Flutter)

Todos os scripts estão organizados de forma sistemática e são reproduzíveis, permitindo validação independente dos resultados apresentados na monografia.

---

## Estrutura de Organização

```
evaluation/
├── scripts/                          # Scripts organizados por categoria
│   ├── 01_model_evaluation/         # Scripts de avaliação do modelo
│   ├── 02_api_performance/          # Scripts de testes de carga/performance
│   └── README.md                     # Documentação geral dos scripts
│
├── model_analysis/                   # Dados e resultados da avaliação do modelo
│   ├── data/                        # Dados de entrada
│   ├── results/                     # Resultados JSON
│   └── graphs/                      # Gráficos gerados
│
├── api_load_testing/                 # Dados e resultados dos testes de carga
│   ├── results/                     # Resultados CSV/JSON
│   ├── graphs/                      # Gráficos gerados
│   └── consolidated_graphs/         # Gráficos consolidados
│
├── 01_reports/                       # Relatórios de avaliação
├── 02_graphs/                        # Gráficos finais (português/inglês)
├── 03_data/                          # Dados brutos consolidados
└── GUIA_SCRIPTS_AVALIACAO.md        # Este documento

# Na raiz do projeto (fora de evaluation/)
packages/
└── frontend/
    └── integration_test/             # Testes E2E do frontend (Flutter)
```

---

## 1. Avaliação do Modelo de Análise de Sentimentos

### Localização

**Scripts**: `evaluation/scripts/01_model_evaluation/`  
**Dados e Resultados**: `evaluation/model_analysis/`

### Objetivo

Avaliar e validar o modelo de classificação de sentimento (TF-IDF + Logistic Regression) utilizado no sistema, incluindo:
- Acurácia do modelo comparado ao ground truth
- Métricas de desempenho (Accuracy, Precision, Recall, F1-Score)
- Validação de distribuições de sentimento
- Análise de impacto do idioma na classificação

### Scripts Principais

| Script | Descrição | Uso |
|--------|-----------|-----|
| `compare_metrics_vs_benchmark.py` | Compara métricas com benchmark inicial | Validação de desempenho |
| `validate_model_accuracy_with_dataset.py` | Valida acurácia comentário por comentário | Validação detalhada |
| `validate_model_distribution_multiple_sets.py` | Valida distribuições em múltiplos conjuntos | Validação de viés |
| `validate_model_distribution_vs_benchmark.py` | Compara distribuições com benchmark | Validação de consistência |
| `language_impact_analysis.py` | Analisa impacto do idioma | Análise de viés linguístico |
| `multilingual_sentiment_analysis.py` | Análise detalhada multilíngue | Análise por idioma |
| `generate_confusion_matrix.py` | Gera matriz de confusão | Visualização de erros |
| `generate_metrics_comparison_table.py` | Gera tabela comparativa | Visualização de métricas |

### Como Executar

```bash
cd evaluation/scripts/01_model_evaluation
python compare_metrics_vs_benchmark.py
```

### Resultados Principais

- **Acurácia do Modelo**: 66.14%
- **F1-Score**: 66.28%
- **Precision**: 66.64%
- **Recall**: 66.14%
- **Dataset**: 1.032.225 comentários

### Dependências

```bash
pip install pandas numpy scikit-learn matplotlib seaborn requests scipy
```

### Documentação Completa

Ver: `evaluation/scripts/01_model_evaluation/README.md`

---

## 2. Avaliação de Performance da API

### Localização

**Scripts**: `evaluation/scripts/02_api_performance/`  
**Dados e Resultados**: `evaluation/api_load_testing/`

### Objetivo

Avaliar o desempenho, escalabilidade e capacidade de carga da API intermediária, incluindo:
- Tempo de resposta (média, mínimo, máximo, percentis)
- Throughput (requisições por segundo)
- Comportamento sob carga (múltiplos usuários simultâneos)
- Estabilidade temporal
- Comparação cold start vs warm Lambda

### Scripts Principais

| Script | Descrição | Uso |
|--------|-----------|-----|
| `run_all.py` | Executa todos os testes e gera resumo | Teste completo |
| `videos.py` | Testes de listagem de vídeos | Performance de busca |
| `comments.py` | Testes de listagem de comentários | Performance de comentários |
| `stability.py` | Teste de estabilidade temporal | Performance ao longo do tempo |
| `locust_test.py` | Teste de carga básico | Simulação de usuários |
| `locust_max_tps.py` | Teste de TPS máximo | Limite de capacidade |
| `generate_consolidated_graphs.py` | Gera gráficos consolidados | Visualização de resultados |

### Scripts Complementares

Existem scripts adicionais em `evaluation/04_scripts/tests/`:

- `extended_benchmark.py`: Teste estendido (219 requisições)
- `heavy_load_test.py`: Teste de carga pesada (10.600 comentários)
- `multi_video_benchmark.py`: Benchmark com múltiplos vídeos
- `batch_size_analysis.py`: Análise de impacto do tamanho do lote

### Como Executar

```bash
# Executar todos os testes
cd evaluation/scripts/02_api_performance
python run_all.py

# Teste de carga com Locust
locust -f locust_max_tps.py --host=https://API_URL/prod
```

### Resultados Principais

- **Tempo médio de resposta**: ~1.024ms
- **Throughput máximo**: ~10-15 TPS
- **Taxa de sucesso**: 100% (sob carga normal)
- **Suporte a usuários simultâneos**: 50-100 usuários

### Dependências

```bash
pip install requests matplotlib seaborn numpy pandas locust
```

### Documentação Completa

Ver: `evaluation/scripts/02_api_performance/README.md`

---

## 3. Testes End-to-End do Frontend

### Localização

**Scripts**: `packages/frontend/integration_test/` (na raiz do projeto, não em `evaluation/`)

> **Nota**: Os testes do frontend estão localizados na pasta do frontend do projeto, não na pasta de avaliação, pois fazem parte do código do aplicativo Flutter.

### Objetivo

Validar a interface do usuário e o fluxo completo do aplicativo mobile Flutter, incluindo:
- Renderização real da interface gráfica
- Simulação de interações do usuário (taps, scrolls, text input)
- Navegação entre telas
- Funcionalidades (favoritos, filtros, etc.)
- Integração completa frontend → API → análise de sentimento

### Scripts Principais

| Script | Descrição | Testes |
|--------|-----------|--------|
| `critical_user_flows_test.dart` | Fluxos críticos do usuário | 7 testes principais |
| `comprehensive_e2e_test.dart` | Testes abrangentes | 6 cenários |
| `extended_features_test.dart` | Funcionalidades estendidas | 6 testes |
| `complete_all_features_test.dart` | Cobertura completa | 14 testes |

### Como Executar

```bash
# Na raiz do projeto
cd packages/frontend
flutter test integration_test/
```

### Resultados Principais

- **Cobertura**: 25+ funcionalidades testadas
- **Taxa de sucesso**: 90%+
- **Validação**: UI renderizada, interações do usuário, API, análise de sentimento, persistência

### Dependências

```bash
flutter pub get  # No diretório packages/frontend
```

### Documentação Completa

Ver: `packages/frontend/integration_test/README.md`

---

## Como Referenciar na Monografia

### Estrutura Sugerida para a Seção de Metodologia

#### 4. Metodologia de Avaliação

##### 4.1 Avaliação do Modelo de Análise de Sentimentos

Os scripts de avaliação do modelo estão localizados em `evaluation/scripts/01_model_evaluation/` e incluem:

- **Validação de Métricas**: Utilizamos `compare_metrics_vs_benchmark.py` para comparar as métricas do modelo com o benchmark inicial, validando que o modelo mantém o desempenho observado durante a seleção (Acurácia: 66.14%, F1-Score: 66.28%).

- **Validação de Acurácia**: O script `validate_model_accuracy_with_dataset.py` valida a acurácia comentário por comentário, comparando as predições da API com o ground truth do dataset.

- **Validação de Distribuições**: Utilizamos `validate_model_distribution_multiple_sets.py` para validar o viés sistemático do modelo usando múltiplos conjuntos aleatórios de vídeos (145 vídeos divididos em 5 conjuntos de 29).

**Referência**: Todos os scripts estão disponíveis em `evaluation/scripts/01_model_evaluation/` e podem ser executados para reproduzir os resultados.

##### 4.2 Avaliação de Performance da API

Os testes de performance foram realizados utilizando scripts em `evaluation/scripts/02_api_performance/`:

- **Testes Básicos**: Utilizamos `run_all.py` para executar uma bateria completa de testes, incluindo testes de listagem de vídeos (`videos.py`), comentários (`comments.py`) e estabilidade temporal (`stability.py`).

- **Testes de Carga**: Utilizamos Locust (`locust_max_tps.py`) para simular múltiplos usuários simultâneos e determinar o throughput máximo da API.

- **Testes Estendidos**: Realizamos testes adicionais com `extended_benchmark.py` (219 requisições) e `heavy_load_test.py` (10.600 comentários) para avaliar a escalabilidade do sistema.

**Resultados**: Tempo médio de resposta de ~1.024ms, throughput máximo de ~10-15 TPS, suporte a 50-100 usuários simultâneos com 100% de taxa de sucesso.

**Referência**: Scripts disponíveis em `evaluation/scripts/02_api_performance/` e `evaluation/04_scripts/tests/`.

##### 4.3 Testes End-to-End do Frontend

Os testes do frontend foram realizados utilizando o framework Flutter `integration_test`:

- **Localização**: Os testes estão localizados em `packages/frontend/integration_test/` (na raiz do projeto, não em `evaluation/`), pois fazem parte do código do aplicativo Flutter.

- **Cobertura**: 25+ funcionalidades testadas, incluindo busca de vídeos, carregamento de comentários, filtragem por sentimento, favoritos e navegação.

- **Validação**: Renderização real da UI, interações do usuário, integração com API, análise de sentimento e persistência de dados.

**Referência**: Scripts disponíveis em `packages/frontend/integration_test/`.

### Exemplo de Citação

> "Os scripts de avaliação estão organizados em `evaluation/scripts/` e podem ser executados para reproduzir todos os resultados apresentados nesta monografia. A documentação completa está disponível em `evaluation/GUIA_SCRIPTS_AVALIACAO.md`."

### Apêndice Sugerido

**Apêndice A - Scripts de Avaliação**

Este apêndice referencia todos os scripts utilizados nas avaliações:

1. **Avaliação do Modelo**: `evaluation/scripts/01_model_evaluation/`
2. **Avaliação de Performance**: `evaluation/scripts/02_api_performance/`
3. **Testes E2E do Frontend**: `packages/frontend/integration_test/` (testes Flutter com renderização real da UI)

Todos os scripts são reproduzíveis e podem ser executados seguindo as instruções em `evaluation/scripts/README.md`.

**Nota**: Os testes do frontend estão localizados em `packages/frontend/integration_test/` (na raiz do projeto), pois fazem parte do código do aplicativo Flutter.

---

## 📚 Referências Adicionais

- **Documentação Consolidada dos Scripts**: `evaluation/scripts/README.md` ⭐ (Documentação completa e consolidada de todos os scripts)
- **Relatório Final**: `evaluation/01_reports/FINAL_EVALUATION_REPORT.md`
- **Metodologia**: `evaluation/01_reports/TESTING_METHODOLOGY.md`
- **Índice de Navegação**: `evaluation/01_reports/INDEX.md`
- **Guia de Avaliação da API**: `evaluation/API_EVALUATION_GUIDE.md`

---

**Última Atualização**: Novembro 2025  
**Versão**: 1.0  
**Status**: ✅ Completo e Organizado


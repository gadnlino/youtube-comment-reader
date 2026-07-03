# Scripts de Avaliação - YouTube Comment Reader

Índice pai: [`../README.md`](../README.md)

> **Índice completo:** [`CATALOG.md`](CATALOG.md) — scripts, saídas e localizações anteriores.  
> **Verificação:** [`VERIFICATION_STATUS.md`](VERIFICATION_STATUS.md) · [`VERIFICATION_BACKLOG.md`](VERIFICATION_BACKLOG.md)

Este documento consolida a documentação dos scripts de avaliação, organizados por categoria.

## 📁 Estrutura

```
scripts/
├── _paths.py                # Constantes de caminho partilhadas
├── CATALOG.md               # Índice de todos os scripts
├── 01_model_evaluation/     # Avaliação do modelo
├── 02_api_performance/      # Testes de carga e performance da API
│   ├── generators/          # Gráficos académicos (EN/PT)
│   └── benchmarks/          # Benchmarks estendidos (Oct 2025)
├── 03_api_e2e/              # E2E Python (legado; Flutter é canónico)
└── README.md

packages/frontend/integration_test/  # Testes E2E Flutter (canónico)
evaluation/model_comparison/scripts/ # Comparação de modelos (co-localizado)
```

**Nota sobre Resultados**: Cada pasta de scripts contém subpastas `results/` e `graphs/` com **resultados de referência** para facilitar a validação e compreensão. Estes são exemplos dos resultados mais recentes/importantes. Todos os resultados históricos completos estão nas pastas originais:
- `../../model_analysis/results/` e `../../model_analysis/graphs/` - Todos os resultados do modelo
- `../../api_load_testing/results/` e `../../api_load_testing/graphs/` - Todos os resultados da API

Os scripts são **reproduzíveis** - ao executá-los, novos resultados serão gerados nas pastas originais.

---

## 1. Avaliação do Modelo de Análise de Sentimentos

### Localização

**Scripts**: `evaluation/scripts/01_model_evaluation/`  
**Dados e Resultados**: `evaluation/model_analysis/`

### Objetivo

Avaliar e validar o modelo de classificação de sentimento (TF-IDF + Logistic Regression) utilizado no sistema, incluindo:
- Acurácia do modelo comparado aos rótulos verdadeiros
- Métricas de desempenho (acurácia, precisão, revocação, F1-Score)
- Análise de impacto do idioma na classificação
- Geração de visualizações (matriz de confusão, gráficos comparativos)

### Scripts Principais

#### Validação de Métricas

- **`compare_metrics_vs_benchmark.py`**: Compara as métricas básicas (acurácia, precisão, revocação, F1-Score) da validação atual com o benchmark inicial. Valida se o modelo mantém o desempenho observado durante a seleção.

- **`validate_model_accuracy_with_dataset.py`**: Valida a acurácia do modelo comparando predições da API com os rótulos verdadeiros do dataset, comentário a comentário.

#### Análise de Idioma

- **`language_impact_analysis.py`**: Analisa o impacto do idioma na classificação de sentimento, identificando viés linguístico.

- **`multilingual_sentiment_analysis.py`**: Análise detalhada de sentimento em múltiplos idiomas.

- **`analyze_video_language.py`**: Analisa o perfil de idioma dos vídeos.

#### Geração de Visualizações

- **`generate_confusion_matrix.py`**: Gera matriz de confusão do modelo.

- **`generate_metrics_comparison_table.py`**: Gera tabela e gráfico comparando métricas do benchmark vs validação.

- **`generate_language_analysis_graphs.py`**: Gera gráficos de análise de idioma.

- **`generate_language_analysis_graphs_pt.py`**: Gera gráficos de análise de idioma (versão em português).

- **`generate_sentiment_distribution_by_language.py`**: Gera gráficos de distribuição de sentimento por idioma.

- **`generate_language_analysis_graphs.py`**: Gera gráficos de análise de idioma.

- **`generate_language_analysis_graphs_pt.py`**: Gera gráficos de análise de idioma (versão em português).

- **`generate_sentiment_distribution_by_language.py`**: Gera gráficos de distribuição de sentimento por idioma.

#### Utilitários

- **`pre_filter_working_videos.py`**: Pré-filtra vídeos que funcionam com a API para uso nas validações.

### Como Executar

#### Pré-requisitos

Instale uma vez a partir da raiz do repositório (ver também [`../README.md`](../README.md#configuração)):

```bash
pip install -r evaluation/requirements.txt
python3 -m nltk.downloader vader_lexicon
```

#### Executar um Script

```bash
cd evaluation/scripts/01_model_evaluation
python3 compare_metrics_vs_benchmark.py
```

### Estrutura de Dados Necessários

Os scripts esperam encontrar:
- **Dataset com rótulos verdadeiros**: `youtube_comments_cleaned.csv` (geralmente em `../api_load_testing/` ou `../../03_data/csv/`)
- **Listas de vídeos**: Arquivos JSON em `../model_analysis/data/` ou `../../03_data/json/`

### Resultados

Os scripts geram:
- **Arquivos JSON**: Resultados das análises (salvos em `../model_analysis/results/`)
- **Gráficos PNG**: Visualizações (salvos em `../model_analysis/graphs/`)

**Resultados de Referência**: Esta pasta contém resultados e gráficos de referência em `results/` e `graphs/` para facilitar a validação. Todos os resultados históricos completos estão em `../../model_analysis/`.

### Resultados Principais

- **Acurácia do Modelo**: 66.14%
- **F1-Score**: 66.28%
- **Precisão**: 66.64%
- **Revocação**: 66.14%
- **Dataset**: 1.032.225 comentários

### Notas Importantes

- Todos os scripts assumem que você está executando a partir da pasta `evaluation/scripts/01_model_evaluation/` ou `evaluation/`
- Os arquivos de dados podem estar em diferentes locais - os scripts tentam encontrar automaticamente
- Os scripts criam automaticamente as pastas necessárias (`data/`, `results/`, `graphs/`) se não existirem

---

## 2. Testes de Carga e Performance da API

### Localização

**Scripts**: `evaluation/scripts/02_api_performance/`  
**Dados e Resultados**: `evaluation/api_load_testing/`

### Objetivo

Avaliar o desempenho, escalabilidade e capacidade de carga da API intermediária, incluindo:
- Tempo de resposta (média, mínimo, máximo, percentis)
- Throughput (requisições por segundo)
- Comportamento sob carga (múltiplos usuários simultâneos)
- Estabilidade temporal
- Comparação arranque a frio (cold start) vs Lambda aquecida

### Scripts Principais

#### Testes Básicos de Performance

- **`common.py`**: Funções utilitárias compartilhadas (HTTP, métricas, gráficos)
- **`videos.py`**: Testes de listagem de vídeos (endpoint `/videos/search`)
- **`comments.py`**: Testes de listagem de comentários (endpoint `/comments`)
- **`stability.py`**: Teste de estabilidade temporal (performance ao longo do tempo)
- **`run_all.py`**: Script principal que executa todos os testes e gera resumo

#### Testes de Carga com Locust

- **`locust_test.py`**: Teste de carga básico usando Locust
- **`locust_max_tps.py`**: Teste de carga para encontrar TPS máximo
- **`run_max_tps_test.sh`**: Script shell para executar teste de TPS máximo

#### Geração de Gráficos e Relatórios

- **`generate_consolidated_graphs.py`**: Gera gráficos consolidados de todos os testes
- **`generate_locust_graphs.py`**: Gera gráficos a partir dos resultados do Locust
- **`generate_e2e_test_table.py`**: Gera tabela de resultados dos testes E2E

### Como Executar

#### Pré-requisitos

As mesmas dependências da avaliação do modelo — instale uma vez a partir da raiz do repositório:

```bash
pip install -r evaluation/requirements.txt
```

#### Executar Todos os Testes

```bash
cd evaluation/scripts/02_api_performance
python3 run_all.py
```

#### Executar Testes Individuais

```bash
# Testes de vídeos
python3 videos.py

# Testes de comentários
python3 comments.py

# Teste de estabilidade
python3 stability.py
```

#### Testes de Carga com Locust

```bash
# Teste básico
locust -f locust_test.py --host=https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod

# Teste de TPS máximo
./run_max_tps_test.sh
# ou
locust -f locust_max_tps.py --host=https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod
```

#### Gerar Gráficos Consolidados

```bash
python3 generate_consolidated_graphs.py
```

### Configuração

Antes de executar os testes, configure:

#### 1. URL da API

Edite `common.py`:
```python
API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod"
```

#### 2. Vídeos para Teste

Edite `comments.py` e `videos.py` com IDs de vídeos apropriados:
```python
VIDEOS = {
    'poucos': {
        'id': 'VIDEO_ID_AQUI',  # Vídeo com < 100 comentários
        'name': 'Poucos Comentários (< 100)'
    },
    # ...
}
```

### Resultados

Os scripts geram:
- **Arquivos CSV**: Dados brutos dos testes (salvos em `../api_load_testing/results/`)
- **Arquivos JSON**: Resumos estatísticos (salvos em `../api_load_testing/results/`)
- **Gráficos PNG**: Visualizações (salvos em `../api_load_testing/graphs/`; figuras docx em [`../02_graphs/`](../02_graphs/MANIFEST.md))
- **Relatórios HTML**: Relatórios do Locust (salvos em `../api_load_testing/results/`)

**Resultados de Referência**: Esta pasta contém resultados e gráficos consolidados de referência em `results/` e `graphs/` para facilitar a validação. Todos os resultados históricos completos estão em `../../api_load_testing/`.

### Resultados Principais

- **Tempo médio de resposta**: ~1.024ms
- **Throughput máximo**: ~10-15 TPS
- **Taxa de sucesso**: 100% (sob carga normal)
- **Suporte a usuários simultâneos**: 50-100 usuários

### Scripts Adicionais

Benchmarks estendidos (carga pesada, multi-vídeo, tamanho de lote) estão em `benchmarks/`:

- **`extended_benchmark.py`**, **`heavy_load_test.py`**, **`multi_video_benchmark.py`**, etc.

Ver [`CATALOG.md`](CATALOG.md) para a lista completa.

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

#### Pré-requisitos

```bash
cd packages/frontend
flutter pub get
```

#### Executar os Testes

```bash
# Na raiz do projeto
cd packages/frontend
flutter test integration_test/
```

### Resultados Principais

- **Cobertura**: 25+ funcionalidades testadas
- **Taxa de sucesso**: 90%+
- **Validação**: UI renderizada, interações do usuário, API, análise de sentimento, persistência

### Tecnologias Usadas

- **Flutter SDK**: Framework mobile multiplataforma
- **integration_test**: Pacote oficial do Flutter para testes E2E
- **WidgetTester**: Ferramenta para simular interações de usuário
- **Simulação de gestos**: Taps, scroll, text input
- **Renderização real**: Widgets são realmente renderizados

### Cenários de Teste

1. **Busca de vídeos**: Busca e exibição de resultados
2. **Carregamento de comentários**: Com e sem análise de sentimento
3. **Filtragem por sentimento**: Positivo, negativo, neutro (validação de 100% de acurácia)
4. **Favoritos**: Adicionar/remover vídeos e comentários dos favoritos
5. **Navegação**: Navegação entre telas e tabs
6. **Tratamento de erros**: Comportamento com entradas inválidas

---

## 📊 Resultados das Avaliações

Os resultados das avaliações estão organizados em:

- **Relatórios**: `../01_reports/`
- **Gráficos**: `../02_graphs/`
- **Dados brutos**: `../03_data/`

## 📝 Dependências Gerais

### Para Scripts Python (Modelo e API)

```bash
pip install -r evaluation/requirements.txt
```

### Para Testes do Frontend

```bash
cd packages/frontend
flutter pub get
```

## 🔗 Referências Adicionais

- **Relatório Final de Avaliação**: `../01_reports/FINAL_EVALUATION_REPORT.md`
- **Metodologia de Testes**: `../01_reports/TESTING_METHODOLOGY.md`
- **Guia de Avaliação da API**: `../../05_guides/API_EVALUATION_METHODOLOGY.md`
- **Índice de Scripts**: [`CATALOG.md`](CATALOG.md)

## 📚 Para a Monografia

Estes scripts podem ser referenciados na monografia como:

1. **Avaliação do Modelo**: Scripts em `evaluation/scripts/01_model_evaluation/`
2. **Avaliação de Performance**: Scripts em `evaluation/scripts/02_api_performance/`
3. **Testes E2E do Frontend**: Scripts em `packages/frontend/integration_test/` (na raiz do projeto)

Todos os scripts são reproduzíveis e podem ser executados para validar os resultados apresentados na monografia.

**Nota**: Os testes do frontend (Flutter) estão localizados fora da pasta `evaluation/`, em `packages/frontend/integration_test/`, pois fazem parte do código do frontend do projeto.

---

**Última Atualização**: Novembro 2025  
**Versão**: 1.0  
**Status**: ✅ Documentação Consolidada

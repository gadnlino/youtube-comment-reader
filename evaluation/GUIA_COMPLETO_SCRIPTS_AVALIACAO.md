# Guia Completo - Scripts de Avaliação do YouTube Comment Reader

> **Documento de Referência Completo para Monografia**  
> Este guia consolida toda a documentação dos scripts utilizados nas avaliações do sistema, organizado por tipo de teste.

---

## 📋 Índice

1. [Testes de Avaliação do Modelo de Análise de Sentimentos](#1-testes-de-avaliação-do-modelo-de-análise-de-sentimentos)
2. [Testes de Carga e Performance da API](#2-testes-de-carga-e-performance-da-api)
3. [Testes End-to-End do Frontend](#3-testes-end-to-end-do-frontend)

---

## 1. Testes de Avaliação do Modelo de Análise de Sentimentos

### 📍 Localização

**Scripts**: `evaluation/scripts/01_model_evaluation/`  
**Dados e Resultados Completos**: `evaluation/model_analysis/`  
**Resultados de Referência**: `evaluation/scripts/01_model_evaluation/results/` e `graphs/`

### 🎯 Objetivo

Avaliar e validar o modelo de classificação de sentimento (TF-IDF + Logistic Regression) utilizado no sistema, incluindo:
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
- **⚠️ Nota Importante**: Este script seleciona vídeos aleatoriamente de `working_videos_*.json`. Embora o objetivo seja usar vídeos diferentes dos do benchmark inicial (test set), não há verificação automática explícita. Os vídeos são selecionados aleatoriamente do dataset completo, mas é recomendado verificar manualmente que os vídeos selecionados não foram parte do conjunto de treino/teste original (80/20 split).

**`validate_model_accuracy_with_dataset.py`**
- **Função**: Valida a acurácia do modelo comparando predições da API com ground truth do dataset
- **Valida**: Acurácia comentário por comentário
- **Uso**: Validação detalhada de acurácia
- **⚠️ Nota Importante**: Este script usa vídeos de `test_3_videos.json` ou `dataset_videos_for_accuracy_validation.json`. É necessário garantir que esses vídeos não foram utilizados no conjunto de treino/teste original do modelo (80/20 split). Os vídeos devem ser selecionados manualmente para garantir independência dos dados de treino/teste.

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

**⚠️ Importante - Separação de Dados**: Os scripts de validação usam o dataset completo (`youtube_comments_cleaned.csv`) para buscar o ground truth, mas **não há verificação automática** de que os vídeos/comentários selecionados não foram parte do conjunto de treino/teste original usado na seleção do modelo (divisão 80/20). Para garantir validação independente, é recomendado:

1. Manter registro dos vídeos/comentários usados no treino/teste original
2. Verificar manualmente que os vídeos em `test_3_videos.json`, `dataset_videos_for_accuracy_validation.json` ou `working_videos_*.json` não foram parte do conjunto original
3. Ou usar uma divisão explícita do dataset (ex: usar apenas vídeos de um período específico ou com IDs específicos que não foram usados no treino/teste)

### 📊 Resultados

#### Onde os Resultados são Salvos

- **Arquivos JSON**: Resultados das análises são salvos em `../../model_analysis/results/`
- **Gráficos PNG**: Visualizações são salvas em `../../model_analysis/graphs/`
- **Resultados de Referência**: Cópias dos resultados mais recentes estão em `results/` e `graphs/` dentro da pasta dos scripts

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

- **Arquivos CSV**: Dados brutos dos testes são salvos em `../../api_load_testing/results/`
- **Arquivos JSON**: Resumos estatísticos são salvos em `../../api_load_testing/results/`
- **Gráficos PNG**: Visualizações são salvas em `../../api_load_testing/graphs/` ou `../../api_load_testing/consolidated_graphs/`
- **Relatórios HTML**: Relatórios do Locust são salvos em `../../api_load_testing/results/`
- **Resultados de Referência**: Cópias dos resultados mais recentes estão em `results/` e `graphs/` dentro da pasta dos scripts

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

**Scripts**: `packages/frontend/integration_test/` (na raiz do projeto, não em `evaluation/`)

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
flutter test integration_test/app_test.dart
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
  --target=integration_test/app_test.dart
```

##### Opção 3: Teste em Device Específico

```bash
# Listar devices disponíveis
flutter devices

# Executar em device específico
flutter drive \
  --driver=test_driver/integration_test.dart \
  --target=integration_test/app_test.dart \
  -d <device_id>
```

##### Opção 4: Executar Todos os Testes

```bash
cd packages/frontend
flutter test integration_test/
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
- **Relatórios de teste**: `packages/frontend/integration_test/*_REPORT.md`
- **Relatórios de avaliação**: `evaluation/01_reports/`

---

## 📚 Referências Gerais

### Estrutura de Pastas

```
evaluation/
├── scripts/                          # Scripts organizados por categoria
│   ├── 01_model_evaluation/         # Scripts de avaliação do modelo
│   │   ├── results/                 # Resultados de referência (JSON)
│   │   ├── graphs/                  # Gráficos de referência (PNG)
│   │   └── *.py                     # Scripts de avaliação
│   ├── 02_api_performance/          # Scripts de testes de carga/performance
│   │   ├── results/                 # Resultados de referência (JSON)
│   │   ├── graphs/                  # Gráficos consolidados de referência (PNG)
│   │   └── *.py                     # Scripts de testes
│   └── README.md                     # Documentação consolidada
│
├── model_analysis/                   # Dados e resultados completos do modelo
├── api_load_testing/                 # Dados e resultados completos da API
├── 01_reports/                       # Relatórios de avaliação
├── 02_graphs/                        # Gráficos finais (português/inglês)
└── 03_data/                          # Dados brutos consolidados

packages/frontend/integration_test/   # Testes E2E do frontend (Flutter)
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

1. **Avaliação do Modelo**: Scripts em `evaluation/scripts/01_model_evaluation/`
2. **Avaliação de Performance**: Scripts em `evaluation/scripts/02_api_performance/`
3. **Testes E2E do Frontend**: Scripts em `packages/frontend/integration_test/`

Todos os scripts são **reproduzíveis** e podem ser executados para validar os resultados apresentados na monografia.

---

**Última Atualização**: Novembro 2025  
**Versão**: 1.0  
**Status**: ✅ Documentação Completa e Consolidada


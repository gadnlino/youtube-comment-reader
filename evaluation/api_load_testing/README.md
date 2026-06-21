# Testes de Performance da API

Este diretório contém scripts automatizados para avaliar o desempenho da API intermediária do aplicativo de comentários do YouTube.

## Estrutura

```
evaluation/api_load_testing/
├── scripts/
│   ├── common.py          # Funções utilitárias (HTTP, métricas, gráficos)
│   ├── videos.py          # Testes de listagem de vídeos
│   ├── comments.py        # Testes de listagem de comentários
│   ├── stability.py       # Teste de estabilidade temporal
│   ├── run_all.py         # Script principal (executa todos os testes)
│   ├── locust_max_tps.py  # Teste de TPS máximo com Locust
│   ├── run_max_tps_test.sh # Script bash para executar teste de TPS
│   └── [outros scripts auxiliares]
├── results/               # Resultados dos testes (CSV, JSON)
├── graphs/                # Gráficos gerados
├── logs/                  # Logs de execução
├── docs/                  # Documentação adicional
└── README.md              # Este arquivo
```

## Pré-requisitos

From the repository root:

```bash
pip install -r evaluation/requirements.txt
```

## Início Rápido

```bash
# 1. Instalar dependências (see above)

# 2. Configurar (editar scripts/common.py, scripts/videos.py, scripts/comments.py conforme necessário)

# 3. Executar todos os testes
cd evaluation/scripts/02_api_performance
python3 run_all.py

# 4. Ver resultados
# - Resultados: ../results/
# - Gráficos: ../graphs/
# - Logs: ../logs/perf_test.log
```

## Configuração

Antes de executar os testes, você precisa configurar:

### 1. URLs e Endpoints

Edite `scripts/common.py` e ajuste:
```python
API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod"
```

### 2. Testes de Vídeos

Edite `scripts/videos.py` e ajuste:
```python
SEARCH_KEYWORD = "python tutorial"  # Palavra-chave para busca
```

### 3. Testes de Comentários

Edite `scripts/comments.py` e preencha os IDs dos vídeos:
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

### 4. Teste de Estabilidade

Edite `scripts/stability.py` e configure:
```python
TEST_ENDPOINT = '/video/comments'  # ou '/search'
TEST_PARAMS = {
    'videoId': 'VIDEO_ID_AQUI',  # Se usar /video/comments
    # ... outros parâmetros
}
DURATION_MINUTES = 10  # Duração do teste (padrão: 10 minutos)
```

## Uso

### Executar Todos os Testes

```bash
cd evaluation/scripts/02_api_performance
python3 run_all.py
```

Ou a partir da raiz do projeto:
```bash
cd evaluation/scripts/02_api_performance && python3 run_all.py
```

### Executar Testes Individuais

```bash
cd evaluation/scripts/02_api_performance

# Apenas testes de vídeos
python3 videos.py

# Apenas testes de comentários
python3 comments.py

# Apenas teste de estabilidade
python3 stability.py
```

**Nota**: Todos os scripts devem ser executados a partir do diretório `scripts/` para que os imports funcionem corretamente.

## Saída

Os scripts geram arquivos nos seguintes diretórios (criados automaticamente):

1. **Arquivos CSV**: Dados brutos de cada requisição
   - `evaluation/api_load_testing/results/videos_test_YYYYMMDD_HHMMSS.csv`
   - `evaluation/api_load_testing/results/comments_test_YYYYMMDD_HHMMSS.csv`
   - `evaluation/api_load_testing/results/stability_test_YYYYMMDD_HHMMSS.csv`

2. **Arquivos JSON**: Dados brutos + métricas agregadas
   - `evaluation/api_load_testing/results/videos_test_YYYYMMDD_HHMMSS.json`
   - `evaluation/api_load_testing/results/comments_test_YYYYMMDD_HHMMSS.json`
   - `evaluation/api_load_testing/results/stability_test_YYYYMMDD_HHMMSS.json`

3. **Gráficos PNG**: Visualizações dos resultados
   - `evaluation/api_load_testing/graphs/videos_mean_comparison_*.png` - Comparação de tempos médios
   - `evaluation/api_load_testing/graphs/videos_p95_comparison_*.png` - Comparação de P95
   - `evaluation/api_load_testing/graphs/videos_boxplot_*.png` - Distribuição de tempos
   - `evaluation/api_load_testing/graphs/comments_*.png` - Gráficos similares para comentários
   - `evaluation/api_load_testing/graphs/stability_timeseries_*.png` - Série temporal de estabilidade

4. **Resumo Executivo**: 
   - `evaluation/api_load_testing/results/perf_summary_YYYYMMDD_HHMMSS.txt` - Resumo textual
   - `evaluation/api_load_testing/results/perf_summary_YYYYMMDD_HHMMSS.json` - Resumo em JSON

5. **Logs de Execução**:
   - `evaluation/api_load_testing/logs/perf_test.log` - Log detalhado de todas as execuções

## Métricas Calculadas

Para cada cenário/teste, são calculadas:

- **Média**: Tempo médio de resposta
- **Mediana**: Tempo mediano de resposta
- **P95**: Percentil 95 (95% das requisições abaixo deste valor)
- **Mínimo**: Menor tempo observado
- **Máximo**: Maior tempo observado
- **Desvio Padrão**: Variabilidade dos tempos
- **Taxa de Sucesso**: Requisições bem-sucedidas / Total

## Testes Implementados

### 1. Listagem de Vídeos (4 cenários)

- **Consulta Padrão**: Sem filtros adicionais
- **Filtro Textual**: Busca com palavra-chave
- **Ordenação por Relevância**: Resultados ordenados por relevância
- **Ordenação por Data**: Resultados ordenados por data de publicação

Cada cenário executa **30 requisições** com intervalo de **400ms** entre elas.

### 2. Listagem de Comentários (3 volumes)

- **Poucos Comentários**: < 100 comentários
- **Volume Intermediário**: 300-800 comentários
- **Alto Volume**: > 1.500 comentários

Cada volume executa **30 requisições** com intervalo de **400ms** entre elas.

### 3. Estabilidade Sob Carga

Executa **muitas requisições contínuas** durante **10 minutos** (configurável) para verificar a estabilidade do endpoint sob carga alta. 
- Intervalo entre requisições: 400ms (alta frequência)
- Total estimado: ~1.500 requisições em 10 minutos
- Mede **TPS (Transactions Per Second)** e capacidade de processamento

## Resumo Executivo

O resumo gerado (`perf_summary_*.txt`) contém:

- Tempo médio e P95 por cenário
- Comparações entre cenários
- Impacto do volume de comentários
- **TPS (Transactions Per Second)** e capacidade de throughput
- Análise de estabilidade (coeficiente de variação)
- Conclusões gerais sobre a performance

Este resumo pode ser usado diretamente como base para a seção de avaliação de desempenho da monografia.

## Teste de TPS Máximo com Locust

Para encontrar o **TPS máximo** da API com aumento gradual de carga:

```bash
# Executar teste de TPS máximo (Locust incluído em evaluation/requirements.txt)
cd evaluation/scripts/02_api_performance
chmod +x run_max_tps_test.sh  # Dar permissão de execução (primeira vez)
./run_max_tps_test.sh

# Ou com parâmetros customizados
./run_max_tps_test.sh 100 10 20m
# 100 = máximo de usuários
# 10 = ramp-up (usuários por segundo)
# 20m = duração
```

O teste de TPS máximo:
- Aumenta gradualmente usuários simultâneos
- Identifica TPS máximo sustentável
- Detecta ponto de degradação de performance
- Identifica quando começam as falhas
- Gera relatórios CSV e HTML detalhados em `evaluation/api_load_testing/results/`

**Veja `docs/README_MAX_TPS.md` para documentação completa.**

## Figuras da monografia

Figura 25–26 e referência para Tabela 3: executar `generate_consolidated_graphs.py` em `evaluation/scripts/02_api_performance/`. Cópias em [`evaluation/02_graphs/`](../02_graphs/MANIFEST.md).

## Notas Importantes

- **Diretório de execução**: Todos os scripts Python devem ser executados a partir do diretório `scripts/` para que os imports funcionem corretamente
- **Paths relativos**: Os scripts criam automaticamente os diretórios `results/`, `graphs/` e `logs/` no diretório pai (`evaluation/api_load_testing/`)
- **Configuração**: Os scripts incluem marcadores `TODO` onde você precisa ajustar configurações (URLs, IDs de vídeos, etc.)
- **Intervalos**: Os intervalos entre requisições podem ser ajustados nos scripts individuais (`DELAY_BETWEEN_REQUESTS`)
- **Estabilidade**: O teste de estabilidade executa muitas requisições em 10 minutos (teste de carga) - pode levar tempo
- **Timestamps**: Todos os arquivos são salvos com timestamp para evitar sobrescrita
- **TPS**: TPS é calculado automaticamente nos testes de estabilidade
- **Logs**: Todos os logs são salvos em `logs/perf_test.log` para acompanhamento em tempo real


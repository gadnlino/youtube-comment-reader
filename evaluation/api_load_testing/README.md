# Testes de Performance da API

Este diretório contém scripts automatizados para avaliar o desempenho da API intermediária do aplicativo de comentários do YouTube.

## Estrutura

```
evaluation/api_load_testing/
├── common.py          # Funções utilitárias (HTTP, métricas, gráficos)
├── videos.py          # Testes de listagem de vídeos
├── comments.py        # Testes de listagem de comentários
├── stability.py       # Teste de estabilidade temporal
├── run_all.py         # Script principal (executa todos os testes)
└── README.md          # Este arquivo
```

## Pré-requisitos

```bash
pip install requests matplotlib seaborn numpy
```

## Configuração

Antes de executar os testes, você precisa configurar:

### 1. URLs e Endpoints

Edite `common.py` e ajuste:
```python
API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod"
```

### 2. Testes de Vídeos

Edite `videos.py` e ajuste:
```python
SEARCH_KEYWORD = "python tutorial"  # Palavra-chave para busca
```

### 3. Testes de Comentários

Edite `comments.py` e preencha os IDs dos vídeos:
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

Edite `stability.py` e configure:
```python
TEST_ENDPOINT = '/video/comments'  # ou '/search'
TEST_PARAMS = {
    'videoId': 'VIDEO_ID_AQUI',  # Se usar /video/comments
    # ... outros parâmetros
}
DURATION_MINUTES = 60  # Duração do teste
```

## Uso

### Executar Todos os Testes

```bash
cd evaluation/api_load_testing
python3 run_all.py
```

### Executar Testes Individuais

```bash
# Apenas testes de vídeos
python3 videos.py

# Apenas testes de comentários
python3 comments.py

# Apenas teste de estabilidade
python3 stability.py
```

## Saída

Os scripts geram:

1. **Arquivos CSV**: Dados brutos de cada requisição
   - `results/videos_test_YYYYMMDD_HHMMSS.csv`
   - `results/comments_test_YYYYMMDD_HHMMSS.csv`
   - `results/stability_test_YYYYMMDD_HHMMSS.csv`

2. **Arquivos JSON**: Dados brutos + métricas agregadas
   - `results/videos_test_YYYYMMDD_HHMMSS.json`
   - `results/comments_test_YYYYMMDD_HHMMSS.json`
   - `results/stability_test_YYYYMMDD_HHMMSS.json`

3. **Gráficos PNG**: Visualizações dos resultados
   - `graphs/videos_mean_comparison_*.png` - Comparação de tempos médios
   - `graphs/videos_p95_comparison_*.png` - Comparação de P95
   - `graphs/videos_boxplot_*.png` - Distribuição de tempos
   - `graphs/comments_*.png` - Gráficos similares para comentários
   - `graphs/stability_timeseries_*.png` - Série temporal de estabilidade

4. **Resumo Executivo**: 
   - `results/perf_summary_YYYYMMDD_HHMMSS.txt` - Resumo textual
   - `results/perf_summary_YYYYMMDD_HHMMSS.json` - Resumo em JSON

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
# Instalar Locust (se ainda não tiver)
pip install locust

# Executar teste de TPS máximo (script automatizado)
cd evaluation/api_load_testing
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
- Gera relatórios CSV e HTML detalhados

**Veja `README_MAX_TPS.md` para documentação completa.**

## Notas

- Os scripts incluem marcadores `TODO` onde você precisa ajustar configurações
- Os intervalos entre requisições podem ser ajustados nos scripts individuais
- O teste de estabilidade executa muitas requisições em 10 minutos (teste de carga)
- Todos os arquivos são salvos com timestamp para evitar sobrescrita
- TPS é calculado automaticamente nos testes de estabilidade


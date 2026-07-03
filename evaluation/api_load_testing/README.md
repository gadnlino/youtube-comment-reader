# Testes de Performance da API — `api_load_testing/`

Saídas dos testes de carga e performance da API (**Pilar 2**). Scripts canônicos: [`../scripts/02_api_performance/`](../scripts/CATALOG.md).

## Propósito

Este diretório contém **resultados** (CSV, JSON, logs) e pastas de testes Locust (`teste_1`…`teste_4`). Os scripts Python executáveis estão em `evaluation/scripts/02_api_performance/` (não nesta pasta).

## Estrutura

```
evaluation/api_load_testing/
├── results/               # Resultados dos testes (CSV, JSON)
├── graphs/                # Gráficos gerados (execuções locais)
├── logs/                  # Logs de execução
├── docs/                  # Documentação adicional
├── teste_1/ … teste_4/    # Dados de testes Locust por campanha
├── scripts/README.md      # Redirect → ../scripts/02_api_performance/
└── README.md              # Este arquivo
```

## Pré-requisitos

Na raiz do repositório:

```bash
pip install -r evaluation/requirements.txt
```

## Regenerar figuras e tabela da monografia (Tabela 3, Figuras 25–26)

Os ativos embutidos no docx usam dados Locust já gravados sob `evaluation/api_load_testing/` (pastas `teste_*` e `results/`). Inventário completo: [`../02_graphs/MANIFEST.md`](../02_graphs/MANIFEST.md).

Na raiz do repositório:

```bash
# Figuras 25–26 (painéis consolidados de TPS / sucesso / latência)
# e métricas de referência para a Tabela 3
python3 evaluation/scripts/02_api_performance/generate_consolidated_graphs.py
```

Saídas típicas:

| Ativo | Destino canônico |
|--------|------------------|
| **Figura 25** | [`../02_graphs/figures/figura-25_consolidated_graphs_part1.png`](../02_graphs/figures/figura-25_consolidated_graphs_part1.png) |
| **Figura 26** | [`../02_graphs/figures/figura-26_consolidated_graphs_part2.png`](../02_graphs/figures/figura-26_consolidated_graphs_part2.png) |
| **Tabela 3** | Métricas Locust agregadas (texto/Word); o gerador produz os painéis e o resumo a partir dos CSV/JSON em `results/` e `teste_*/` |

Se o gerador gravar PNGs em outro local (por exemplo `graphs/` ou `consolidated_graphs/`), copie-os para `evaluation/02_graphs/figures/` com os nomes canônicos acima.

**Nota:** a **Tabela 4** (testes E2E Flutter) não é gerada aqui — ver [`packages/frontend/integration_test/README.md`](../../packages/frontend/integration_test/README.md) e:

```bash
python3 evaluation/scripts/02_api_performance/generate_e2e_test_table.py --thesis
```

## Início Rápido (reexecutar testes de carga)

```bash
# 1. Instalar dependências (ver Pré-requisitos)

# 2. Configurar (editar arquivos em evaluation/scripts/02_api_performance/)

# 3. Executar todos os testes
cd evaluation/scripts/02_api_performance
python3 run_all.py

# 4. Ver resultados
# - Resultados: evaluation/api_load_testing/results/
# - Gráficos: evaluation/api_load_testing/graphs/
# - Logs: evaluation/api_load_testing/logs/perf_test.log
```

## Configuração

Antes de executar os testes, configure os arquivos em **`evaluation/scripts/02_api_performance/`** (não em `api_load_testing/scripts/`).

### 1. URLs e Endpoints

Edite `evaluation/scripts/02_api_performance/common.py` e ajuste:

```python
API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod"
```

### 2. Testes de Vídeos

Edite `evaluation/scripts/02_api_performance/videos.py` e ajuste:

```python
SEARCH_KEYWORD = "python tutorial"  # Palavra-chave para busca
```

### 3. Testes de Comentários

Edite `evaluation/scripts/02_api_performance/comments.py` e preencha os IDs dos vídeos:

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

Edite `evaluation/scripts/02_api_performance/stability.py` e configure:

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

**Nota:** execute os scripts a partir de `evaluation/scripts/02_api_performance/` para que os imports locais funcionem corretamente.

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

**Veja [`docs/README_MAX_TPS.md`](docs/README_MAX_TPS.md) para documentação completa.**

## Notas Importantes

- **Diretório de execução**: scripts em `evaluation/scripts/02_api_performance/` (não `api_load_testing/scripts/`)
- **Paths relativos**: os scripts criam automaticamente `results/`, `graphs/` e `logs/` em `evaluation/api_load_testing/`
- **Configuração**: os scripts incluem marcadores `TODO` onde é preciso ajustar URLs, IDs de vídeos, etc.
- **Intervalos**: ajustáveis em cada script (`DELAY_BETWEEN_REQUESTS`)
- **Estabilidade**: o teste de estabilidade pode demorar (~10 minutos)
- **Timestamps**: os arquivos de saída usam timestamp para evitar sobrescrita
- **TPS**: calculado automaticamente nos testes de estabilidade
- **Logs**: `evaluation/api_load_testing/logs/perf_test.log`

## Ver também

- [`../02_graphs/MANIFEST.md`](../02_graphs/MANIFEST.md) — inventário das figuras e tabelas da monografia
- [`../README.md`](../README.md) — índice da avaliação
- [`../scripts/CATALOG.md`](../scripts/CATALOG.md) — scripts canônicos

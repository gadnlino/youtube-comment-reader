# Relatório de Testes de Carga - API YouTube Comment Reader

> **Nota:** Este relatório e todos os arquivos relacionados (scripts, dados, gráficos) estão localizados em `evaluation/api_load_testing/` no repositório do projeto.

## 1. Introdução

Este relatório apresenta os resultados dos testes de carga realizados na API intermediária do YouTube Comment Reader, com o objetivo de avaliar a capacidade de processamento, escalabilidade e limites de operação do sistema sob diferentes níveis de carga.

### 1.1 Objetivos

- Avaliar a capacidade de processamento (TPS - Transactions Per Second) da API
- Identificar o limite máximo de usuários simultâneos suportados
- Analisar a estabilidade da API sob carga prolongada
- Identificar pontos de degradação e falhas
- Estabelecer recomendações para operação em produção

### 1.2 Metodologia

Os testes foram realizados utilizando a ferramenta **Locust**, um framework Python para testes de carga. A metodologia seguiu os seguintes passos:

1. **Testes Incrementais**: Iniciando com 50 usuários e aumentando progressivamente
2. **Smoke Tests**: Testes rápidos (3 minutos) para validar capacidade antes de testes prolongados
3. **Testes Prolongados**: Testes de 15 minutos para avaliar estabilidade temporal
4. **Análise de Métricas**: TPS, tempo de resposta, taxa de falhas, percentis

### 1.3 Ambiente de Teste

- **Ferramenta**: Locust 2.x
- **API Base URL**: `https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod`
- **Endpoints Testados**:
  - `/search` - Busca de vídeos
  - `/video/comments` - Listagem de comentários com análise de sentimento
- **Duração dos Testes**: 3 minutos (smoke tests) e 15 minutos (testes completos)
- **Ramp-up**: Gradual, conforme especificado em cada teste

---

## 2. Testes Realizados

### 2.1 Teste 1 - Baseline (50 usuários simultâneos)

**Configuração:**
- Usuários simultâneos: 50
- Ramp-up rate: 5 usuários/segundo
- Duração: 15 minutos
- Data: 2025-11-22 21:14:34

**Resultados:**

| Métrica | Valor |
|---------|-------|
| **TPS Médio** | 60.18 transações/segundo |
| **Total de Requisições** | 54,124 |
| **Taxa de Sucesso** | 100.0% (2 falhas, 0.004%) |
| **Tempo Médio de Resposta** | 624ms |
| **Mediana** | 500ms |
| **P95** | 1,100ms |
| **Mínimo** | 252ms |
| **Máximo** | 5,783ms |

**Análise por Endpoint:**

| Endpoint | Requisições | TPS | Tempo Médio | Falhas |
|----------|-------------|-----|-------------|--------|
| `/search` | 15,543 | 17.28 | 538ms | 2 (0.01%) |
| `/video/comments` | 38,581 | 42.90 | 659ms | 0 (0.00%) |

**Conclusão:**
A API demonstrou excelente performance com 50 usuários simultâneos, mantendo 100% de taxa de sucesso e TPS estável de ~60. A performance indica que a API pode suportar carga adicional.

---

### 2.2 Teste 2 - Escalabilidade (100 usuários simultâneos)

**Configuração:**
- Usuários simultâneos: 100
- Ramp-up rate: 10 usuários/segundo
- Duração: 15 minutos
- Data: 2025-11-22 21:36:54

**Resultados:**

| Métrica | Valor | Variação vs Teste 1 |
|---------|-------|---------------------|
| **TPS Médio** | 133.37 transações/segundo | **+121%** ⬆️ |
| **Total de Requisições** | 119,978 | **+122%** ⬆️ |
| **Taxa de Sucesso** | 100.0% (29 falhas, 0.024%) | Mantida ✅ |
| **Tempo Médio de Resposta** | 544ms | **-13%** ⬇️ |
| **Mediana** | 488ms | -2% |
| **P95** | 1,074ms | **-2%** ⬇️ |
| **Mínimo** | 190ms | -25% |
| **Máximo** | 3,494ms | -40% |

**Análise por Endpoint:**

| Endpoint | Requisições | TPS | Tempo Médio | Falhas |
|----------|-------------|-----|-------------|--------|
| `/search` | 34,553 | 38.41 | 407ms | 7 (0.02%) |
| `/video/comments` | 85,425 | 94.96 | 600ms | 22 (0.03%) |

**Análise Comparativa:**

Ao dobrar o número de usuários (50→100), observou-se:
- **Escalabilidade Linear**: TPS quase dobrou (60→133), demonstrando excelente escalabilidade
- **Performance Melhorou**: Tempo médio de resposta melhorou de 624ms para 544ms, indicando otimização para maior concorrência
- **Confiabilidade Mantida**: Taxa de sucesso permaneceu em 100%, com apenas 29 falhas em quase 120 mil requisições

**Conclusão:**
A API demonstrou excelente escalabilidade linear, mantendo alta confiabilidade mesmo com o dobro de carga. A melhoria no tempo de resposta sugere que a arquitetura está otimizada para maior concorrência.

---

### 2.3 Teste 3 - Limite de Capacidade

#### 2.3.1 Smoke Test - 500 usuários (3 minutos)

**Configuração:**
- Usuários simultâneos: 500
- Ramp-up rate: 50 usuários/segundo
- Duração: 3 minutos
- Data: 2025-11-22 21:55:02

**Resultados:**

| Métrica | Valor |
|---------|-------|
| **TPS Médio** | 459.90 transações/segundo |
| **Total de Requisições** | 82,648 |
| **Taxa de Sucesso** | 97.7% (1,925 falhas, 2.33%) |
| **Tempo Médio de Resposta** | 851ms |
| **Mediana** | 691ms |
| **P95** | 1,740ms |
| **Mínimo** | 143ms |
| **Máximo** | 19,565ms |

**Análise por Endpoint:**

| Endpoint | Requisições | TPS | Tempo Médio | Falhas |
|----------|-------------|-----|-------------|--------|
| `/search` | 23,731 | 132.07 | 800ms | 442 (1.86%) |
| `/video/comments` | 58,917 | 327.88 | 875ms | 1,483 (2.52%) |

**Tipos de Erros:**
- Status 502 (Bad Gateway): 1,652 ocorrências
- Status 500 (Internal Server Error): 271 ocorrências
- Status 403 (Forbidden): 1 ocorrência
- Status 0 (Connection error): 1 ocorrência

**Conclusão:**
A API aguentou 500 usuários simultâneos, mas já mostrou sinais de estresse com taxa de falhas de 2.33% e aumento significativo no tempo de resposta. Recomendado reduzir para 300 usuários para operação mais estável.

---

#### 2.3.2 Smoke Test - 300 usuários (3 minutos)

**Configuração:**
- Usuários simultâneos: 300
- Ramp-up rate: 30 usuários/segundo
- Duração: 3 minutos
- Data: 2025-11-22 21:59:25

**Resultados:**

| Métrica | Valor |
|---------|-------|
| **TPS Médio** | 384.86 transações/segundo |
| **Total de Requisições** | 69,145 |
| **Taxa de Sucesso** | 100.0% (0 falhas) ✅ |
| **Tempo Médio de Resposta** | 557ms |
| **Mediana** | 510ms |
| **P95** | 1,077ms |
| **Mínimo** | 234ms |
| **Máximo** | 2,999ms |

**Análise por Endpoint:**

| Endpoint | Requisições | TPS | Tempo Médio | Falhas |
|----------|-------------|-----|-------------|--------|
| `/search` | 19,636 | 109.30 | 462ms | 0 (0.00%) |
| `/video/comments` | 49,509 | 275.58 | 595ms | 0 (0.00%) |

**Conclusão:**
300 usuários simultâneos demonstraram ser um ponto de operação estável para testes curtos, mantendo 100% de taxa de sucesso e performance consistente.

---

#### 2.3.3 Teste Completo - 300 usuários (15 minutos)

**Configuração:**
- Usuários simultâneos: 300
- Ramp-up rate: 30 usuários/segundo
- Duração: 15 minutos
- Data: 2025-11-22 22:02:30

**Resultados:**

| Métrica | Valor |
|---------|-------|
| **TPS Médio** | 416.32 transações/segundo |
| **Total de Requisições** | 374,584 |
| **Taxa de Sucesso** | 76.5% (87,979 falhas, 23.49%) ❌ |
| **Tempo Médio de Resposta** | 567ms |
| **Mediana** | 505ms |
| **P95** | 1,068ms |
| **Mínimo** | 216ms |
| **Máximo** | 41,640ms |

**Análise por Endpoint:**

| Endpoint | Requisições | TPS | Tempo Médio | Falhas | Taxa de Falhas |
|----------|-------------|-----|-------------|--------|----------------|
| `/search` | 107,000 | 118.92 | 363ms | 77,018 | **72.0%** ⚠️ |
| `/video/comments` | 267,584 | 297.40 | 572ms | 10,961 | 4.1% |

**Nota Técnica sobre `/search`:**
Este endpoint implementa cache usando DynamoDB, mas mesmo assim apresentou alta taxa de falhas. Isso sugere que o problema pode estar relacionado à capacidade do DynamoDB ou à estratégia de cache (TTL muito curto, falta de cache warming, etc.), e não necessariamente à lógica de negócio do endpoint.

**Tipos de Erros:**
- Status 502 (Bad Gateway): 77,261 ocorrências
  - `/search`: 77,017 ocorrências (99.7% das falhas deste endpoint)
  - `/video/comments`: 244 ocorrências
- Status 403 (Forbidden): 10,716 ocorrências
  - Principalmente em `/video/comments` (quota excedida)
- Status 0 (Connection error): 2 ocorrências

**Análise Crítica:**

1. **Endpoint `/search` é o Gargalo**:
   - 72% de falhas durante teste prolongado
   - Indica necessidade de otimização ou rate limiting específico
   - Status 502 sugere problemas de processamento ou timeout

2. **Endpoint `/video/comments` é Mais Resiliente**:
   - Apenas 4.1% de falhas mesmo sob carga prolongada
   - Melhor capacidade de escalar
   - Falhas principalmente por quota excedida (Status 403)

3. **Degradação Temporal**:
   - Smoke test de 3 minutos: 100% de sucesso
   - Teste prolongado de 15 minutos: 76.5% de sucesso
   - Indica que a API não consegue manter carga alta por períodos prolongados

**Conclusão:**
300 usuários simultâneos por 15 minutos excedeu a capacidade da API. O endpoint `/search` apresentou problemas críticos, enquanto `/video/comments` manteve relativa estabilidade. A degradação temporal indica necessidade de otimização para carga prolongada.

---

### 2.4 Teste 4 - Validação (200 usuários) - Cancelado

**Status:** ❌ Cancelado - Quota da API do YouTube Excedida

O teste com 200 usuários não pôde ser completado porque a quota diária da API do YouTube foi esgotada durante os testes anteriores (~400,000 requisições acumuladas).

**Erros Identificados:**
- Status 403: Quota Exceeded - Todas as requisições bloqueadas
- Status 502: Bad Gateway - Erro interno relacionado à quota

**Próximos Passos:**
- Aguardar reset da quota (geralmente à meia-noite UTC ou após 24h)
- Re-executar o teste após reset para validar a recomendação de 200 usuários

---

## 3. Análise Comparativa Geral

### 3.1 Resumo de Todos os Testes

| Teste | Usuários | Duração | TPS Médio | Requisições | Taxa Sucesso | Tempo Médio | Status |
|-------|----------|---------|-----------|-------------|--------------|-------------|--------|
| Teste 1 | 50 | 15min | 60.18 | 54,124 | 100.0% | 624ms | ✅ Excelente |
| Teste 2 | 100 | 15min | 133.37 | 119,978 | 100.0% | 544ms | ✅ Excelente |
| Teste 3 - Smoke 300 | 300 | 3min | 384.86 | 69,145 | 100.0% | 557ms | ✅ Excelente |
| Teste 3 - Smoke 500 | 500 | 3min | 459.90 | 82,648 | 97.7% | 851ms | ⚠️ Estressado |
| Teste 3 - Completo 300 | 300 | 15min | 416.32 | 374,584 | 76.5% | 567ms | ❌ Excedeu capacidade |
| Teste 4 | 200 | - | - | - | - | - | ❌ Cancelado (quota) |

### 3.2 Análise de Escalabilidade

**Escalabilidade Linear (50 → 100 usuários):**
- TPS aumentou proporcionalmente: 60.18 → 133.37 (+121%)
- Tempo de resposta melhorou: 624ms → 544ms (-13%)
- Taxa de sucesso mantida: 100% → 100%

**Limite Identificado (300 usuários):**
- Smoke test (3min): ✅ 100% de sucesso
- Teste prolongado (15min): ❌ 76.5% de sucesso
- **Conclusão**: 300 usuários é viável para picos curtos, mas não para carga sustentada

### 3.3 Análise de Performance por Endpoint

**Endpoint `/search`:**
- **Ponto Forte**: Tempo de resposta rápido (363-538ms)
- **Ponto Fraco**: Alta taxa de falhas sob carga prolongada (72% no teste de 15min)
- **Recomendação**: Requer otimização prioritária

**Endpoint `/video/comments`:**
- **Ponto Forte**: Alta resiliência (4.1% de falhas mesmo sob carga)
- **Ponto Forte**: Melhor escalabilidade (TPS até 327.88)
- **Ponto Fraco**: Tempo de resposta ligeiramente maior (572-659ms)
- **Recomendação**: Endpoint mais estável, pode servir como referência

---

## 4. Limitações Identificadas

### 4.1 Quota da API do YouTube

**Problema:**
- A API intermediária depende da API do YouTube, que possui quota diária limitada
- Durante os testes, foram geradas aproximadamente 400,000 requisições
- Isso esgotou a quota diária, bloqueando todas as requisições subsequentes (Status 403)

**Impacto:**
- Limita a capacidade de realizar testes extensivos
- Pode afetar operação em produção se não monitorada
- Requer estratégias de cache e otimização de requisições

**Recomendações:**
- Implementar cache agressivo para reduzir requisições à API do YouTube
- Monitorar quota em tempo real
- Implementar rate limiting na API intermediária
- Considerar múltiplas API keys (se disponível)

### 4.2 Degradação Temporal

**Problema:**
- API mantém performance em testes curtos (3 minutos)
- Degrada significativamente em testes prolongados (15 minutos)
- Endpoint `/search` é particularmente afetado

**Causas Prováveis:**
- Acúmulo de requisições não processadas
- Timeout em requisições à API do YouTube
- Limites de concorrência não configurados adequadamente

**Recomendações:**
- Implementar circuit breaker
- Configurar timeouts apropriados
- Implementar retry com backoff exponencial
- Considerar queue system para requisições

### 4.3 Endpoint `/search` como Gargalo

**Problema:**
- 72% de taxa de falhas em teste prolongado
- Principalmente erros 502 (Bad Gateway)
- Indica problema específico neste endpoint

**Observação Importante:**
O endpoint `/search` **já implementa cache** usando DynamoDB:
- Cache habilitado via variável de ambiente `CACHE_ENABLED=true`
- TTL configurável via `EXPIRATION_TIME_MINUTES` (padrão: 1 minuto)
- Cache key baseado em parâmetros da busca: `searchVideos:part=${part}&regionCode=${regionCode}&type=${type}&q=${q}&pageToken=${pageToken}`

**Possíveis Causas dos Erros 502:**
1. **Cache do DynamoDB sob carga**: O DynamoDB pode estar atingindo limites de throughput durante picos
2. **TTL muito curto**: Com TTL de 1 minuto, muitas requisições podem estar "cache miss" simultaneamente
3. **Timeout no DynamoDB**: Queries ao DynamoDB podem estar timeout durante alta carga
4. **Falta de cache warming**: Primeira requisição sempre vai à API do YouTube, causando gargalo

**Recomendações:**
- Investigar métricas do DynamoDB durante os testes (read/write capacity)
- Aumentar TTL do cache para reduzir requisições à API do YouTube
- Implementar cache warming para queries comuns
- Adicionar circuit breaker para DynamoDB
- Considerar aumentar read capacity do DynamoDB
- Adicionar logging detalhado para diagnóstico (cache hit/miss rates)

---

## 5. Recomendações para Produção

### 5.1 Capacidade Recomendada

**Operação Normal:**
- **Usuários simultâneos**: Até 100 usuários
- **TPS esperado**: ~130 TPS
- **Taxa de sucesso esperada**: >99.9%

**Picos de Tráfego:**
- **Usuários simultâneos**: Até 200 usuários (validar após reset de quota)
- **Duração máxima**: 5 minutos
- **Taxa de sucesso esperada**: >95%

**Não Recomendado:**
- **Usuários simultâneos**: >300 usuários
- **Carga prolongada**: >10 minutos com >200 usuários

### 5.2 Monitoramento

Implementar monitoramento contínuo de:
- TPS em tempo real
- Taxa de falhas por endpoint
- Tempo de resposta (média, mediana, P95, P99)
- Quota da API do YouTube
- Status codes de erro (403, 502, 500)

### 5.3 Otimizações Prioritárias

1. **Endpoint `/search`**:
   - Investigar e corrigir causa dos erros 502
   - Implementar cache para queries comuns
   - Adicionar rate limiting específico

2. **Gestão de Quota**:
   - Implementar cache agressivo
   - Monitorar quota em tempo real
   - Implementar fallback quando quota estiver baixa

3. **Resiliência**:
   - Implementar circuit breaker
   - Adicionar retry com backoff exponencial
   - Configurar timeouts apropriados

---

## 6. Conclusões

### 6.1 Principais Descobertas

1. **Excelente Escalabilidade Linear**: A API demonstrou escalabilidade linear até 100 usuários simultâneos, dobrando o TPS ao dobrar os usuários.

2. **Limite de Capacidade Identificado**: 300 usuários simultâneos é viável para picos curtos (3 minutos), mas não para carga sustentada (15 minutos).

3. **Endpoint `/search` Requer Atenção**: Apresentou 72% de falhas em teste prolongado, indicando necessidade de otimização prioritária.

4. **Endpoint `/video/comments` Mais Resiliente**: Manteve apenas 4.1% de falhas mesmo sob carga prolongada.

5. **Quota da API do YouTube é Limitação**: A dependência da API do YouTube e sua quota limitada é um fator crítico a ser considerado.

### 6.2 Capacidade Máxima Validada

- **TPS Máximo Sustentável**: ~130 TPS (100 usuários simultâneos)
- **TPS Máximo em Picos**: ~385 TPS (300 usuários simultâneos, 3 minutos)
- **Usuários Simultâneos Recomendados**: 100-200 para operação estável

### 6.3 Próximos Passos

1. **Validação Final**: Re-executar teste com 200 usuários após reset de quota
2. **Otimização**: Priorizar otimização do endpoint `/search`
3. **Monitoramento**: Implementar sistema de monitoramento em produção
4. **Cache**: Implementar estratégia de cache para reduzir dependência da quota

---

## 7. Anexos

### 7.1 Arquivos de Resultados

**Localização:** Todos os arquivos estão organizados em `evaluation/api_load_testing/`

Todos os dados brutos, gráficos e relatórios detalhados estão disponíveis em:
- `teste_1/` - Teste baseline (50 usuários)
- `teste_2/` - Teste de escalabilidade (100 usuários)
- `teste_3/` - Testes de limite (300-500 usuários)
  - `smoke_test_300/` - Smoke test com 300 usuários
  - `smoke_test_500/` - Smoke test com 500 usuários
- `teste_4/` - Teste de validação (200 usuários) - Cancelado

**Scripts e Documentação:**
- Scripts de teste: `*.py` (videos.py, comments.py, stability.py, run_all.py, etc.)
- Scripts Locust: `locust_max_tps.py`, `locust_test.py`
- Documentação: `README.md`, `README_MAX_TPS.md`, `ANALISE_ERROS.md`

### 7.2 Gráficos Gerados

**Gráficos Individuais por Teste:**
Para cada teste, foram gerados os seguintes gráficos:
- TPS ao longo do tempo
- Tempo de resposta ao longo do tempo
- Taxa de falhas ao longo do tempo
- Dashboard resumo com múltiplas métricas

**Gráficos Consolidados (Comparação entre Testes):**
Foram gerados gráficos comparativos consolidando todos os testes:
- `tps_comparison.png` - Comparação de TPS por número de usuários
- `success_rate_comparison.png` - Taxa de sucesso por teste
- `response_time_comparison.png` - Tempo de resposta (média e P95)
- `endpoint_comparison.png` - Comparação de performance por endpoint
- `consolidated_graphs_only.png` - Dashboard com 6 gráficos principais (sem tabela)
- `consolidated_table_only.png` - Tabela resumo com métricas consolidadas (para referência)

**Regeneração (2026-06):** os PNGs consolidados originais em `consolidated_graphs/` foram arquivados. Para obter novas cópias, execute `evaluation/scripts/02_api_performance/generate_consolidated_graphs.py`. Figuras da monografia (Figura 25–26): [`evaluation/02_graphs/MANIFEST.md`](../../02_graphs/MANIFEST.md). Arquivo histórico: [`evaluation/06_archived/pruned_figures/2026-06/`](../../06_archived/pruned_figures/2026-06/).

### 7.3 Ferramentas Utilizadas

- **Locust**: Framework Python para testes de carga
- **Python 3.12**: Linguagem de programação
- **Matplotlib/Seaborn**: Geração de gráficos
- **Pandas**: Análise de dados

---

**Data do Relatório:** 22 de Novembro de 2025  
**Versão:** 1.0  
**Autor:** Análise Automatizada de Testes de Carga


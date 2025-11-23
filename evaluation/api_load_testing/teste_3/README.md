# Teste 3 - Análise de Capacidade Máxima (300-500 usuários)

## Resumo Executivo

Este conjunto de testes foi projetado para encontrar o limite de capacidade da API através de testes incrementais, começando com smoke tests rápidos e seguindo com testes completos de 15 minutos.

## Testes Realizados

### 1. Smoke Test - 500 usuários (3 minutos)
**Status**: ⚠️ API aguentou, mas mostrou sinais de estresse

- **Taxa de sucesso**: 97.7% (1,925 falhas de 82,648 requisições)
- **TPS médio**: 459.90
- **Tempo médio**: 851ms
- **Conclusão**: 500 usuários está próximo do limite. Recomendado reduzir para 300.

**Ver**: `smoke_test_500/README.md` para detalhes completos.

### 2. Smoke Test - 300 usuários (3 minutos)
**Status**: ✅ Excelente - 100% de sucesso

- **Taxa de sucesso**: 100.0% (0 falhas!)
- **TPS médio**: 384.86
- **Tempo médio**: 557ms
- **P95**: 1,077ms
- **Conclusão**: 300 usuários é um ponto de operação estável para testes curtos.

**Ver**: `smoke_test_300/` para detalhes.

### 3. Teste Completo - 300 usuários (15 minutos)
**Status**: ❌ API excedeu capacidade após período prolongado

- **Taxa de sucesso**: 76.5% (87,979 falhas de 374,584 requisições - 23.49%)
- **TPS médio**: 416.32
- **Tempo médio**: 567ms
- **P95**: 1,068ms

#### Análise Detalhada por Endpoint

**`/search`**:
- Requisições: 107,000
- **Falhas: 77,018 (72.0%)** ⚠️
- TPS: 118.92
- Tempo médio: 363ms
- **Problema crítico**: Este endpoint não suporta carga prolongada

**`/video/comments`**:
- Requisições: 267,584
- Falhas: 10,961 (4.1%)
- TPS: 297.40
- Tempo médio: 572ms
- **Status**: Relativamente estável, mas também apresentou degradação

#### Tipos de Erros
- **Status 502 (Bad Gateway)**: 77,261 ocorrências - Principal causa de falhas
- **Status 403 (Forbidden)**: 10,716 ocorrências - Provavelmente rate limiting
- **Status 0 (Connection error)**: 2 ocorrências

## Conclusões Principais

1. **Limite de Capacidade Identificado**: 
   - **Smoke tests (3 min)**: 300 usuários = ✅ Estável | 500 usuários = ⚠️ Estressado
   - **Testes prolongados (15 min)**: 300 usuários = ❌ Excede capacidade

2. **Endpoint `/search` é o Gargalo**:
   - 72% de falhas durante teste prolongado
   - Indica necessidade de otimização ou rate limiting específico

3. **Endpoint `/video/comments` é Mais Resiliente**:
   - Apenas 4.1% de falhas mesmo sob carga prolongada
   - Melhor capacidade de escalar

4. **Recomendações**:
   - **Para produção**: Limitar a ~200 usuários simultâneos para operação estável
   - **Para picos**: Até 300 usuários são aceitáveis por períodos curtos (< 5 minutos)
   - **Otimização necessária**: Endpoint `/search` requer atenção prioritária

## Comparação com Testes Anteriores

| Teste | Usuários | Duração | Taxa Sucesso | TPS | Status |
|-------|----------|---------|--------------|-----|--------|
| Teste 1 | 50 | 15min | 100.0% | 60.18 | ✅ Excelente |
| Teste 2 | 100 | 15min | 100.0% | 133.37 | ✅ Excelente |
| Teste 3 - Smoke 300 | 300 | 3min | 100.0% | 384.86 | ✅ Excelente |
| Teste 3 - Smoke 500 | 500 | 3min | 97.7% | 459.90 | ⚠️ Estressado |
| Teste 3 - Completo 300 | 300 | 15min | 76.5% | 416.32 | ❌ Excedeu capacidade |

## Arquivos

- `smoke_test_500/` - Resultados do smoke test com 500 usuários
- `smoke_test_300/` - Resultados do smoke test com 300 usuários
- `locust_max_tps_20251122_220230_*` - Resultados do teste completo de 15 minutos
- `graphs/` - Gráficos gerados do teste completo


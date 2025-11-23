# Smoke Test - 500 usuários (3 minutos)

## Configuração
- **Usuários simultâneos**: 500
- **Ramp-up rate**: 50 usuários/segundo
- **Duração**: 3 minutos
- **Data**: 2025-11-22 21:55:02

## Resultados Principais

### Throughput (TPS)
- **TPS médio**: 459.90 transações/segundo
- **Requisições totais**: 82,648
- **Requisições por hora**: 1,655,631

### Performance
- **Tempo médio de resposta**: 851ms
- **Mediana**: 691ms
- **P95**: 1,740ms
- **Mínimo**: 143ms
- **Máximo**: 19,565ms

### Confiabilidade
- **Taxa de sucesso**: 97.7%
- **Total de falhas**: 1,925 (2.33%)
- **Status**: ⚠️ API aguentou, mas mostrou sinais de estresse

### Por Endpoint

#### `/search`
- Requisições: 23,731
- TPS: 132.07
- Tempo médio: 800ms
- Falhas: 442 (1.86%)

#### `/video/comments`
- Requisições: 58,917
- TPS: 327.88
- Tempo médio: 875ms
- Falhas: 1,483 (2.52%)

## Análise
A API aguentou 500 usuários simultâneos, mas já mostrou sinais de estresse:
- Taxa de falhas aumentou para 2.33% (vs 0.02% com 100 usuários)
- Tempo de resposta aumentou significativamente (851ms vs 544ms)
- Erros 502 (Bad Gateway) e 500 (Internal Server Error) começaram a aparecer

**Conclusão**: 500 usuários está próximo do limite. Recomenda-se testar com 300 usuários para encontrar um ponto de operação mais estável.

## Tipos de Erros
- Status 502: 1,652 ocorrências (Bad Gateway)
- Status 500: 271 ocorrências (Internal Server Error)
- Status 403: 1 ocorrência (Forbidden)
- Status 0: 1 ocorrência (Connection error)


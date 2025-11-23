# Teste 1 - TPS Máximo (50 usuários)

## Configuração
- **Usuários simultâneos**: 50
- **Ramp-up rate**: 5 usuários/segundo
- **Duração**: 15 minutos
- **Data**: 2025-11-22 21:14:34

## Resultados Principais

### Throughput (TPS)
- **TPS médio**: 60.18 transações/segundo
- **TPS máximo observado**: ~64 TPS
- **Requisições totais**: 54,124
- **Requisições por hora**: 216,635

### Performance
- **Tempo médio de resposta**: 624ms
- **Mediana**: 500ms
- **P95**: 1,100ms
- **Mínimo**: 252ms
- **Máximo**: 5,783ms

### Confiabilidade
- **Taxa de sucesso**: 100.0%
- **Total de falhas**: 2 (0.004%)
- **Status**: ✅ Excelente - API suporta 60+ TPS com alta confiabilidade

### Por Endpoint

#### `/search`
- Requisições: 15,543
- TPS: 17.28
- Tempo médio: 538ms
- Falhas: 2 (0.01%)

#### `/video/comments`
- Requisições: 38,581
- TPS: 42.90
- Tempo médio: 659ms
- Falhas: 0 (0.00%)

## Análise
A API demonstrou excelente capacidade, mantendo ~60 TPS com apenas 2 falhas em 54,124 requisições. A taxa de sucesso de 100% indica que a API pode suportar mais carga. Recomenda-se aumentar o número de usuários simultâneos para encontrar o limite real.

## Arquivos
- `locust_max_tps_20251122_211434_stats_history.csv` - Histórico detalhado
- `locust_max_tps_20251122_211434_stats.csv` - Estatísticas agregadas
- `locust_max_tps_report_20251122_211434.html` - Relatório HTML do Locust
- `graphs/` - Gráficos gerados

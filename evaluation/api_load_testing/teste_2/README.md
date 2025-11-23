# Teste 2 - TPS Máximo (100 usuários)

## Configuração
- **Usuários simultâneos**: 100
- **Ramp-up rate**: 10 usuários/segundo
- **Duração**: 15 minutos
- **Data**: 2025-11-22 21:36:54

## Resultados Principais

### Throughput (TPS)
- **TPS médio**: 133.37 transações/segundo
- **TPS máximo observado**: ~137 TPS
- **Requisições totais**: 119,978
- **Requisições por hora**: 480,127
- **Aumento vs Teste 1**: +121% (de 60.18 para 133.37 TPS)

### Performance
- **Tempo médio de resposta**: 544ms
- **Mediana**: 488ms
- **P95**: 1,074ms
- **Mínimo**: 190ms
- **Máximo**: 3,494ms
- **Melhoria vs Teste 1**: Tempo médio melhorou de 624ms para 544ms (-13%)

### Confiabilidade
- **Taxa de sucesso**: 100.0%
- **Total de falhas**: 29 (0.024%)
- **Status**: ✅ Excelente - API suporta 133+ TPS com alta confiabilidade

### Por Endpoint

#### `/search`
- Requisições: 34,553
- TPS: 38.41
- Tempo médio: 407ms
- Falhas: 7 (0.02%)

#### `/video/comments`
- Requisições: 85,425
- TPS: 94.96
- Tempo médio: 600ms
- Falhas: 22 (0.03%)

## Análise Comparativa (Teste 1 vs Teste 2)

| Métrica | Teste 1 (50 users) | Teste 2 (100 users) | Mudança |
|---------|-------------------|-------------------|---------|
| TPS Médio | 60.18 | 133.37 | **+121%** ⬆️ |
| Requisições Totais | 54,124 | 119,978 | **+122%** ⬆️ |
| Tempo Médio | 624ms | 544ms | **-13%** ⬇️ |
| P95 | 1,100ms | 1,074ms | **-2%** ⬇️ |
| Taxa de Sucesso | 100.0% | 100.0% | **Mantida** ✅ |
| Falhas | 2 (0.004%) | 29 (0.024%) | +27 falhas |

## Conclusões

1. **Escalabilidade Excelente**: Ao dobrar o número de usuários (50→100), o TPS quase dobrou (60→133), demonstrando excelente escalabilidade linear.

2. **Performance Melhorou**: Apesar do aumento de carga, o tempo médio de resposta melhorou de 624ms para 544ms, indicando que a API está otimizada para maior concorrência.

3. **Confiabilidade Mantida**: Taxa de sucesso permaneceu em 100%, com apenas 29 falhas (0.024%) em quase 120 mil requisições.

4. **Capacidade Não Atingida**: A API ainda não atingiu seu limite. Recomenda-se testar com 150-200 usuários para encontrar o ponto de degradação.

## Arquivos
- `locust_max_tps_20251122_213654_stats_history.csv` - Histórico detalhado
- `locust_max_tps_20251122_213654_stats.csv` - Estatísticas agregadas
- `locust_max_tps_report_20251122_213654.html` - Relatório HTML do Locust
- `graphs/` - Gráficos gerados


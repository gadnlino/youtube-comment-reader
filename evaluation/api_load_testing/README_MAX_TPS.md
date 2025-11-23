# Teste de TPS Máximo

Este documento descreve como executar testes para encontrar o TPS (Transactions Per Second) máximo da API.

## Objetivo

Encontrar:
- **TPS máximo sustentável**: Maior taxa de transações que a API consegue manter sem degradação
- **Ponto de degradação**: Quando o tempo de resposta começa a aumentar significativamente
- **Ponto de falhas**: Quando a API começa a retornar erros

## Método

O teste usa **ramp-up gradual** de usuários simultâneos:
- Começa com poucos usuários
- Aumenta gradualmente (ex: 5 usuários por segundo)
- Continua até atingir o máximo configurado
- Monitora TPS, tempo de resposta e taxa de falhas

## Pré-requisitos

```bash
pip install locust
```

## Execução Rápida

```bash
cd evaluation/api_load_testing
./run_max_tps_test.sh
```

Ou com parâmetros customizados:
```bash
./run_max_tps_test.sh 100 10 20m
# 100 = máximo de usuários
# 10 = ramp-up (10 usuários/segundo)
# 20m = duração (20 minutos)
```

## Execução Manual

```bash
locust -f locust_max_tps.py \
  --host=https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod \
  --headless \
  -u 50 \              # Máximo de 50 usuários simultâneos
  -r 5 \                # Ramp-up: 5 usuários por segundo
  -t 15m                # Duração: 15 minutos
  --csv=results/locust_max_tps \
  --html=results/locust_max_tps_report.html
```

## Parâmetros

- `-u, --users`: Número máximo de usuários simultâneos
- `-r, --spawn-rate`: Taxa de criação de usuários (usuários por segundo)
- `-t, --run-time`: Duração do teste (ex: `10m`, `1h`, `300s`)
- `--headless`: Executa sem interface web
- `--csv`: Salva estatísticas em CSV
- `--html`: Gera relatório HTML

## Exemplos de Configuração

### Teste Conservador (TPS Sustentável)
```bash
locust -f locust_max_tps.py --host=https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod \
  --headless -u 20 -r 2 -t 10m
```
- 20 usuários máximo
- Ramp-up lento (2/segundo)
- 10 minutos

### Teste Moderado
```bash
locust -f locust_max_tps.py --host=https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod \
  --headless -u 50 -r 5 -t 15m
```
- 50 usuários máximo
- Ramp-up moderado (5/segundo)
- 15 minutos

### Teste Agressivo (Limite Máximo)
```bash
locust -f locust_max_tps.py --host=https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod \
  --headless -u 100 -r 10 -t 20m
```
- 100 usuários máximo
- Ramp-up rápido (10/segundo)
- 20 minutos

## Saída

O teste gera:

1. **Console**: Logs em tempo real com TPS atual, falhas, etc.
2. **CSV**: `locust_max_tps_*_stats.csv` - Estatísticas detalhadas
3. **CSV**: `locust_max_tps_*_failures.csv` - Falhas registradas
4. **HTML**: `locust_max_tps_report_*.html` - Relatório visual completo

## Interpretação dos Resultados

### TPS Máximo Sustentável
- **Bom sinal**: TPS estável com taxa de sucesso > 99%
- **Indica**: API consegue manter essa carga indefinidamente

### Ponto de Degradação
- **Sinal**: Tempo de resposta começa a aumentar (> 2x a média)
- **Indica**: API está próxima do limite, mas ainda funcional

### Ponto de Falhas
- **Sinal**: Taxa de falhas > 5%
- **Indica**: API excedeu capacidade máxima

## Análise do Relatório HTML

O relatório HTML do Locust inclui:
- Gráfico de requisições por segundo (RPS/TPS)
- Gráfico de tempo de resposta ao longo do tempo
- Gráfico de número de usuários
- Tabela de estatísticas por endpoint
- Distribuição de tempos de resposta

## Dicas

1. **Comece conservador**: Execute primeiro com poucos usuários para ter uma baseline
2. **Aumente gradualmente**: Use ramp-up lento para identificar o ponto exato de degradação
3. **Monitore logs**: Acompanhe o console para ver quando começam as falhas
4. **Compare resultados**: Execute múltiplas vezes para confirmar consistência
5. **Considere horários**: Execute em diferentes horários para verificar variações

## Troubleshooting

### Locust não encontrado
```bash
pip install locust
```

### Muitas falhas desde o início
- Reduza o número máximo de usuários (`-u`)
- Aumente o intervalo entre requisições no código (`wait_time`)

### Teste muito lento
- Aumente o ramp-up (`-r`)
- Reduza a duração (`-t`)

### API retornando 429 (Too Many Requests)
- A API tem rate limiting
- Reduza usuários ou aumente intervalo entre requisições


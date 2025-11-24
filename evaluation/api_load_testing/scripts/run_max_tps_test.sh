#!/bin/bash
# Script para executar teste de TPS máximo com Locust

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================================================"
echo "TESTE DE TPS MÁXIMO - YouTube Comment Reader API"
echo "================================================================================"
echo ""

# Verificar se Locust está instalado
if ! command -v locust &> /dev/null; then
    echo "❌ Locust não encontrado!"
    echo "   Instale com: pip install locust"
    exit 1
fi

# Configuração padrão (pode ser ajustada)
MAX_USERS=${1:-50}          # Máximo de usuários simultâneos (padrão: 50)
RAMP_UP=${2:-5}            # Ramp-up: usuários por segundo (padrão: 5)
DURATION=${3:-15m}         # Duração total (padrão: 15 minutos)

echo "📋 Configuração:"
echo "   Máximo de usuários: $MAX_USERS"
echo "   Ramp-up: $RAMP_UP usuários/segundo"
echo "   Duração: $DURATION"
echo ""
echo "⚠️  Este teste vai estressar a API gradualmente"
echo "   O Locust vai aumentar usuários até encontrar o limite"
echo ""

# Criar diretório de resultados
mkdir -p results

# Timestamp para arquivos
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🚀 Iniciando teste..."
echo ""

# Executar Locust em modo headless
locust -f locust_max_tps.py \
  --host=https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod \
  --headless \
  -u $MAX_USERS \
  -r $RAMP_UP \
  -t $DURATION \
  --csv=results/locust_max_tps_${TIMESTAMP} \
  --html=results/locust_max_tps_report_${TIMESTAMP}.html \
  --loglevel INFO

EXIT_CODE=$?

echo ""
echo "================================================================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ TESTE CONCLUÍDO COM SUCESSO${NC}"
else
    echo -e "${YELLOW}⚠️  TESTE CONCLUÍDO COM AVISOS (código: $EXIT_CODE)${NC}"
fi
echo "================================================================================"
echo ""
echo "📄 Relatórios gerados:"
echo "   - results/locust_max_tps_${TIMESTAMP}_stats.csv"
echo "   - results/locust_max_tps_${TIMESTAMP}_failures.csv"
echo "   - results/locust_max_tps_report_${TIMESTAMP}.html"
echo ""
echo "💡 Dica: Abra o arquivo HTML no navegador para ver gráficos detalhados"
echo ""

exit $EXIT_CODE


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Estabilidade Temporal

Executa 1 requisição por minuto durante 60 minutos (ou intervalo configurável)
para verificar a estabilidade do endpoint ao longo do tempo.
"""

import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
from common import (
    make_request, calculate_metrics, save_results_csv, 
    save_results_json, create_time_series_plot, setup_logging
)

# Configurar logging
logger = setup_logging('perf_test.log')

# Configuração do endpoint e parâmetros
TEST_ENDPOINT = '/video/comments'  # Pode ser '/search' ou '/video/comments'
TEST_PARAMS = {
    'videoId': 'dQw4w9WgXcQ',  # Rick Astley - vídeo popular para teste de estabilidade
    'part': 'snippet',
    'maxResults': 100,
    'showPositives': 'true',
    'showNegatives': 'true',
    'showNeutral': 'true'
}

# Configuração do teste
DURATION_MINUTES = 10  # 10 minutos de teste de estabilidade
DELAY_BETWEEN_REQUESTS = 0.4  # 400ms entre requisições (alta frequência)


def run_stability_test() -> Dict[str, Any]:
    """Executa teste de estabilidade sob carga (muitas requisições em 10 minutos)."""
    logger.info("="*80)
    logger.info("TESTE DE ESTABILIDADE SOB CARGA")
    logger.info("="*80)
    logger.info(f"Endpoint: {TEST_ENDPOINT}")
    logger.info(f"Duração: {DURATION_MINUTES} minutos")
    logger.info(f"Intervalo entre requisições: {DELAY_BETWEEN_REQUESTS*1000:.0f}ms")
    logger.info(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Estimar número de requisições (aproximado)
    estimated_requests = int((DURATION_MINUTES * 60) / DELAY_BETWEEN_REQUESTS)
    logger.info(f"Total estimado de requisições: ~{estimated_requests}")
    logger.info("⚠️  Este é um teste de CARGA - muitas requisições em pouco tempo!")
    
    if TEST_ENDPOINT == '/video/comments' and not TEST_PARAMS.get('videoId'):
        logger.warning("\n⚠️  AVISO: videoId não configurado!")
        logger.warning("  Configure TEST_PARAMS['videoId'] antes de executar o teste.")
        return {}
    
    results = []
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=DURATION_MINUTES)
    request_count = 0
    last_log_time = start_time
    
    logger.info(f"\nTeste iniciado. Executando até {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*80)
    logger.info("Executando requisições contínuas...")
    
    while datetime.now() < end_time:
        request_count += 1
        elapsed = (datetime.now() - start_time).total_seconds()
        remaining = (end_time - datetime.now()).total_seconds()
        
        # Log a cada 10 requisições ou a cada 30 segundos
        should_log = (request_count % 10 == 0) or ((datetime.now() - last_log_time).total_seconds() >= 30)
        
        if should_log:
            logger.info(f"Requisição {request_count} (Elapsed: {elapsed/60:.1f}min, Remaining: {remaining/60:.1f}min, ~{request_count/(elapsed/60):.1f} req/min)...")
            last_log_time = datetime.now()
        
        result = make_request(TEST_ENDPOINT, TEST_PARAMS)
        result['request_number'] = request_count
        result['elapsed_minutes'] = elapsed / 60
        results.append(result)
        
        if should_log:
            if result['success']:
                logger.info(f"  ✓ Sucesso: {result['response_time_ms']:.0f}ms ({result.get('item_count', 0)} itens)")
            else:
                logger.warning(f"  ✗ Erro: {result.get('error', 'Unknown')}")
        
        # Aguardar até a próxima requisição (ou até o fim se já passou)
        if datetime.now() < end_time:
            sleep_time = min(DELAY_BETWEEN_REQUESTS, (end_time - datetime.now()).total_seconds())
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    total_time = (datetime.now() - start_time).total_seconds()
    throughput = len(results) / total_time if total_time > 0 else 0
    tps = throughput  # TPS = Transactions Per Second
    
    logger.info("\n" + "="*80)
    logger.info("TESTE CONCLUÍDO")
    logger.info("="*80)
    logger.info(f"Total de requisições: {len(results)}")
    logger.info(f"Tempo total: {total_time/60:.1f} minutos ({total_time:.1f} segundos)")
    logger.info(f"TPS (Transactions Per Second): {tps:.2f}")
    logger.info(f"Throughput: {throughput:.2f} requisições/segundo ({throughput*60:.1f} req/min)")
    
    # Calcular métricas
    metrics = calculate_metrics(results)
    metrics['tps'] = tps
    metrics['total_time_seconds'] = total_time
    metrics['total_requests'] = len(results)
    
    logger.info(f"\nMétricas Gerais:")
    logger.info(f"  TPS (Transactions Per Second): {tps:.2f}")
    logger.info(f"  Média: {metrics['mean']:.2f}ms")
    logger.info(f"  Mediana: {metrics['median']:.2f}ms")
    logger.info(f"  P95: {metrics['p95']:.2f}ms")
    logger.info(f"  Mínimo: {metrics['min']:.2f}ms")
    logger.info(f"  Máximo: {metrics['max']:.2f}ms")
    logger.info(f"  Desvio Padrão: {metrics['std']:.2f}ms")
    logger.info(f"  Sucessos: {metrics['success_count']}/{metrics['count']}")
    
    # Análise de estabilidade de TPS
    logger.info(f"\nAnálise de Throughput:")
    logger.info(f"  TPS médio: {tps:.2f}")
    logger.info(f"  Requisições por minuto: {tps*60:.1f}")
    logger.info(f"  Requisições por hora: {tps*3600:.0f}")
    
    # Salvar resultados
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_file = f'results/stability_test_{timestamp}.csv'
    json_file = f'results/stability_test_{timestamp}.json'
    
    save_results_csv(results, csv_file)
    save_results_json(results, metrics, json_file)
    
    # Gerar gráfico de série temporal
    logger.info("\n" + "="*80)
    logger.info("GERANDO GRÁFICO...")
    logger.info("="*80)
    
    create_time_series_plot(
        results,
        f'Tempo de Resposta sob Carga - Estabilidade ({DURATION_MINUTES} min, {len(results)} requisições)',
        'Tempo de Resposta (ms)',
        f'graphs/stability_timeseries_{timestamp}.png'
    )
    
    logger.info("\n" + "="*80)
    logger.info("✅ TESTE DE ESTABILIDADE CONCLUÍDO")
    logger.info("="*80)
    logger.info(f"Arquivos gerados:")
    logger.info(f"  - {csv_file}")
    logger.info(f"  - {json_file}")
    logger.info(f"  - graphs/stability_timeseries_{timestamp}.png")
    
    return {
        'results': results,
        'metrics': metrics,
        'files': {
            'csv': csv_file,
            'json': json_file,
            'graph': f'graphs/stability_timeseries_{timestamp}.png'
        }
    }


if __name__ == "__main__":
    import os
    os.makedirs('results', exist_ok=True)
    os.makedirs('graphs', exist_ok=True)
    run_stability_test()


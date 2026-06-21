#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes de Performance - Listagem de Vídeos

Avalia o tempo de resposta do endpoint de listagem de vídeos em 4 cenários:
1. Consulta padrão (sem filtros)
2. Consulta com filtro textual
3. Ordenação por relevância
4. Ordenação por data de publicação
"""

import time
import os
from datetime import datetime
from typing import Dict, List, Any
from common import (
    make_request, calculate_metrics, save_results_csv, 
    save_results_json, create_bar_chart, create_boxplot, setup_logging
)

# Configurar logging
logger = setup_logging('perf_test.log')

# TODO: Ajustar palavra-chave de busca conforme necessário
SEARCH_KEYWORD = "python tutorial"

# Configuração dos testes
REQUESTS_PER_SCENARIO = 30
DELAY_BETWEEN_REQUESTS = 0.4  # 400ms


def test_default_search() -> List[Dict[str, Any]]:
    """Teste 1: Consulta padrão, sem filtros adicionais."""
    logger.info("="*80)
    logger.info("TESTE 1: Consulta Padrão (query genérica)")
    logger.info("="*80)
    
    results = []
    # O endpoint /search requer um parâmetro 'q', então usamos uma query genérica
    params = {
        'part': 'snippet',
        'type': 'video',
        'q': 'video',  # Query genérica para busca padrão
        'maxResults': 10
    }
    
    for i in range(REQUESTS_PER_SCENARIO):
        logger.info(f"  Requisição {i+1}/{REQUESTS_PER_SCENARIO}...")
        result = make_request('/search', params)
        result['scenario'] = 'Padrão'
        result['params'] = params.copy()
        results.append(result)
        
        if result['success']:
            logger.info(f"    ✓ Sucesso: {result['response_time_ms']:.0f}ms ({result.get('item_count', 0)} itens)")
        else:
            logger.warning(f"    ✗ Erro: {result.get('error', 'Unknown')}")
        
        if i < REQUESTS_PER_SCENARIO - 1:
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    logger.info(f"  Concluído: {len([r for r in results if r['success']])}/{len(results)} requisições bem-sucedidas")
    return results


def test_text_filter() -> List[Dict[str, Any]]:
    """Teste 2: Consulta com filtro textual."""
    logger.info("="*80)
    logger.info(f"TESTE 2: Consulta com Filtro Textual (palavra-chave: '{SEARCH_KEYWORD}')")
    logger.info("="*80)
    
    results = []
    params = {
        'part': 'snippet',
        'type': 'video',
        'q': SEARCH_KEYWORD,
        'maxResults': 10
    }
    
    for i in range(REQUESTS_PER_SCENARIO):
        logger.info(f"  Requisição {i+1}/{REQUESTS_PER_SCENARIO}...")
        result = make_request('/search', params)
        result['scenario'] = 'Filtro Textual'
        result['params'] = params.copy()
        results.append(result)
        
        if result['success']:
            logger.info(f"    ✓ Sucesso: {result['response_time_ms']:.0f}ms ({result.get('item_count', 0)} itens)")
        else:
            logger.warning(f"    ✗ Erro: {result.get('error', 'Unknown')}")
        
        if i < REQUESTS_PER_SCENARIO - 1:
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    logger.info(f"  Concluído: {len([r for r in results if r['success']])}/{len(results)} requisições bem-sucedidas")
    return results


def test_order_by_relevance() -> List[Dict[str, Any]]:
    """Teste 3: Ordenação por relevância."""
    logger.info("="*80)
    logger.info(f"TESTE 3: Ordenação por Relevância (palavra-chave: '{SEARCH_KEYWORD}')")
    logger.info("="*80)
    
    results = []
    params = {
        'part': 'snippet',
        'type': 'video',
        'q': SEARCH_KEYWORD,
        'order': 'relevance',
        'maxResults': 10
    }
    
    for i in range(REQUESTS_PER_SCENARIO):
        logger.info(f"  Requisição {i+1}/{REQUESTS_PER_SCENARIO}...")
        result = make_request('/search', params)
        result['scenario'] = 'Ordenação: Relevância'
        result['params'] = params.copy()
        results.append(result)
        
        if result['success']:
            logger.info(f"    ✓ Sucesso: {result['response_time_ms']:.0f}ms ({result.get('item_count', 0)} itens)")
        else:
            logger.warning(f"    ✗ Erro: {result.get('error', 'Unknown')}")
        
        if i < REQUESTS_PER_SCENARIO - 1:
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    logger.info(f"  Concluído: {len([r for r in results if r['success']])}/{len(results)} requisições bem-sucedidas")
    return results


def test_order_by_date() -> List[Dict[str, Any]]:
    """Teste 4: Ordenação por data de publicação."""
    logger.info("="*80)
    logger.info(f"TESTE 4: Ordenação por Data de Publicação (palavra-chave: '{SEARCH_KEYWORD}')")
    logger.info("="*80)
    
    results = []
    params = {
        'part': 'snippet',
        'type': 'video',
        'q': SEARCH_KEYWORD,
        'order': 'date',
        'maxResults': 10
    }
    
    for i in range(REQUESTS_PER_SCENARIO):
        logger.info(f"  Requisição {i+1}/{REQUESTS_PER_SCENARIO}...")
        result = make_request('/search', params)
        result['scenario'] = 'Ordenação: Data'
        result['params'] = params.copy()
        results.append(result)
        
        if result['success']:
            logger.info(f"    ✓ Sucesso: {result['response_time_ms']:.0f}ms ({result.get('item_count', 0)} itens)")
        else:
            logger.warning(f"    ✗ Erro: {result.get('error', 'Unknown')}")
        
        if i < REQUESTS_PER_SCENARIO - 1:
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    logger.info(f"  Concluído: {len([r for r in results if r['success']])}/{len(results)} requisições bem-sucedidas")
    return results


def run_video_tests() -> Dict[str, Any]:
    """Executa todos os testes de listagem de vídeos."""
    logger.info("="*80)
    logger.info("BATERIA DE TESTES: LISTAGEM DE VÍDEOS")
    logger.info("="*80)
    logger.info(f"Requisições por cenário: {REQUESTS_PER_SCENARIO}")
    logger.info(f"Intervalo entre requisições: {DELAY_BETWEEN_REQUESTS*1000:.0f}ms")
    logger.info(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Total de requisições: {REQUESTS_PER_SCENARIO * 4}")
    
    # Executar todos os testes
    all_results = []
    
    results_default = test_default_search()
    all_results.extend(results_default)
    
    results_filter = test_text_filter()
    all_results.extend(results_filter)
    
    results_relevance = test_order_by_relevance()
    all_results.extend(results_relevance)
    
    results_date = test_order_by_date()
    all_results.extend(results_date)
    
    # Calcular métricas por cenário
    scenarios = {
        'Padrão': results_default,
        'Filtro Textual': results_filter,
        'Ordenação: Relevância': results_relevance,
        'Ordenação: Data': results_date
    }
    
    metrics_by_scenario = {}
    for scenario_name, scenario_results in scenarios.items():
        metrics = calculate_metrics(scenario_results)
        metrics_by_scenario[scenario_name] = metrics
        
        logger.info(f"\n{scenario_name}:")
        logger.info(f"  Média: {metrics['mean']:.2f}ms")
        logger.info(f"  Mediana: {metrics['median']:.2f}ms")
        logger.info(f"  P95: {metrics['p95']:.2f}ms")
        logger.info(f"  Mínimo: {metrics['min']:.2f}ms")
        logger.info(f"  Máximo: {metrics['max']:.2f}ms")
        logger.info(f"  Desvio Padrão: {metrics['std']:.2f}ms")
        logger.info(f"  Sucessos: {metrics['success_count']}/{metrics['count']}")
    
    # Salvar resultados
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_file = f'results/videos_test_{timestamp}.csv'
    json_file = f'results/videos_test_{timestamp}.json'
    
    save_results_csv(all_results, csv_file)
    save_results_json(all_results, metrics_by_scenario, json_file)
    
    # Gerar gráficos
    logger.info("\n" + "="*80)
    logger.info("GERANDO GRÁFICOS...")
    logger.info("="*80)
    
    # Gráfico de barras - tempo médio
    create_bar_chart(
        metrics_by_scenario,
        'Tempo Médio de Resposta - Listagem de Vídeos',
        'Tempo de Resposta (ms)',
        f'graphs/videos_mean_comparison_{timestamp}.png',
        'mean'
    )
    
    # Gráfico de barras - P95
    create_bar_chart(
        metrics_by_scenario,
        'Percentil 95 (P95) - Listagem de Vídeos',
        'Tempo de Resposta (ms)',
        f'graphs/videos_p95_comparison_{timestamp}.png',
        'p95'
    )
    
    # Boxplot
    data_by_scenario = {
        name: [r['response_time_ms'] for r in results if r.get('success', False)]
        for name, results in scenarios.items()
    }
    create_boxplot(
        data_by_scenario,
        'Distribuição de Tempos de Resposta - Listagem de Vídeos',
        'Tempo de Resposta (ms)',
        f'graphs/videos_boxplot_{timestamp}.png'
    )
    
    logger.info("\n" + "="*80)
    logger.info("✅ TESTES DE LISTAGEM DE VÍDEOS CONCLUÍDOS")
    logger.info("="*80)
    logger.info(f"Arquivos gerados:")
    logger.info(f"  - {csv_file}")
    logger.info(f"  - {json_file}")
    logger.info(f"  - graphs/videos_mean_comparison_{timestamp}.png")
    logger.info(f"  - graphs/videos_p95_comparison_{timestamp}.png")
    logger.info(f"  - graphs/videos_boxplot_{timestamp}.png")
    
    return {
        'results': all_results,
        'metrics': metrics_by_scenario,
        'files': {
            'csv': csv_file,
            'json': json_file,
            'graphs': [
                f'graphs/videos_mean_comparison_{timestamp}.png',
                f'graphs/videos_p95_comparison_{timestamp}.png',
                f'graphs/videos_boxplot_{timestamp}.png'
            ]
        }
    }


if __name__ == "__main__":
    import os
    os.makedirs('results', exist_ok=True)
    os.makedirs('graphs', exist_ok=True)
    run_video_tests()


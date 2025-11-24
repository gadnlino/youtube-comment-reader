#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes de Performance - Listagem de Comentários

Avalia o impacto do volume de comentários no tempo de resposta.
Testa 3 vídeos com diferentes volumes:
1. Poucos comentários (< 100)
2. Volume intermediário (300-800)
3. Alto volume (> 1.500)
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

# Vídeos selecionados para teste com diferentes volumes de comentários
VIDEOS = {
    'poucos': {
        'id': 'jNQXAC9IVRw',  # Me at the zoo - primeiro vídeo do YouTube (histórico)
        'name': 'Poucos Comentários (< 100)'
    },
    'medio': {
        'id': 'fJ9rUzIMcZQ',  # Queen - Bohemian Rhapsody (clássico)
        'name': 'Volume Intermediário (300-800)'
    },
    'muitos': {
        'id': 'dQw4w9WgXcQ',  # Rick Astley - Never Gonna Give You Up (viral)
        'name': 'Alto Volume (> 1.500)'
    }
}

# Configuração dos testes
REQUESTS_PER_VIDEO = 30
DELAY_BETWEEN_REQUESTS = 0.4  # 400ms


def test_video_comments(video_id: str, video_name: str) -> List[Dict[str, Any]]:
    """
    Executa testes de listagem de comentários para um vídeo.
    
    Args:
        video_id: ID do vídeo do YouTube
        video_name: Nome descritivo do vídeo
    
    Returns:
        Lista de resultados
    """
    logger.info(f"\n{'='*80}")
    logger.info(f"TESTE: {video_name} (ID: {video_id})")
    logger.info("="*80)
    
    if not video_id:
        logger.warning("⚠️  ID de vídeo não configurado. Pulando teste.")
        return []
    
    results = []
    params = {
        'videoId': video_id,
        'part': 'snippet',
        'maxResults': 100,
        'showPositives': 'true',
        'showNegatives': 'true',
        'showNeutral': 'true'
    }
    
    for i in range(REQUESTS_PER_VIDEO):
        logger.info(f"  Requisição {i+1}/{REQUESTS_PER_VIDEO}...")
        result = make_request('/video/comments', params)
        result['scenario'] = video_name
        result['video_id'] = video_id
        result['params'] = params.copy()
        results.append(result)
        
        if result['success']:
            logger.info(f"    ✓ Sucesso: {result['response_time_ms']:.0f}ms ({result.get('item_count', 0)} comentários)")
        else:
            logger.warning(f"    ✗ Erro: {result.get('error', 'Unknown')}")
        
        if i < REQUESTS_PER_VIDEO - 1:
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    logger.info(f"  Concluído: {len([r for r in results if r['success']])}/{len(results)} requisições bem-sucedidas")
    return results


def run_comment_tests() -> Dict[str, Any]:
    """Executa todos os testes de listagem de comentários."""
    logger.info("="*80)
    logger.info("BATERIA DE TESTES: LISTAGEM DE COMENTÁRIOS")
    logger.info("="*80)
    logger.info(f"Requisições por vídeo: {REQUESTS_PER_VIDEO}")
    logger.info(f"Intervalo entre requisições: {DELAY_BETWEEN_REQUESTS*1000:.0f}ms")
    logger.info(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Total de requisições: {REQUESTS_PER_VIDEO * len([v for v in VIDEOS.values() if v['id']])}")
    
    # Verificar se os vídeos estão configurados
    missing_videos = [name for key, info in VIDEOS.items() if not info['id']]
    if missing_videos:
        logger.warning(f"\n⚠️  AVISO: Os seguintes vídeos não estão configurados:")
        for name in missing_videos:
            logger.warning(f"  - {name}")
        logger.warning("  Configure os IDs em VIDEOS antes de executar os testes.")
    
    # Executar testes para cada vídeo
    all_results = []
    results_by_video = {}
    
    for key, video_info in VIDEOS.items():
        if video_info['id']:
            results = test_video_comments(video_info['id'], video_info['name'])
            all_results.extend(results)
            results_by_video[video_info['name']] = results
    
    if not all_results:
        logger.error("\n❌ Nenhum teste executado. Configure os IDs dos vídeos primeiro.")
        return {}
    
    # Calcular métricas por volume
    metrics_by_volume = {}
    for volume_name, volume_results in results_by_video.items():
        metrics = calculate_metrics(volume_results)
        metrics_by_volume[volume_name] = metrics
        
        logger.info(f"\n{volume_name}:")
        logger.info(f"  Média: {metrics['mean']:.2f}ms")
        logger.info(f"  Mediana: {metrics['median']:.2f}ms")
        logger.info(f"  P95: {metrics['p95']:.2f}ms")
        logger.info(f"  Mínimo: {metrics['min']:.2f}ms")
        logger.info(f"  Máximo: {metrics['max']:.2f}ms")
        logger.info(f"  Desvio Padrão: {metrics['std']:.2f}ms")
        logger.info(f"  Sucessos: {metrics['success_count']}/{metrics['count']}")
    
    # Salvar resultados
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_file = f'results/comments_test_{timestamp}.csv'
    json_file = f'results/comments_test_{timestamp}.json'
    
    save_results_csv(all_results, csv_file)
    save_results_json(all_results, metrics_by_volume, json_file)
    
    # Gerar gráficos
    logger.info("\n" + "="*80)
    logger.info("GERANDO GRÁFICOS...")
    logger.info("="*80)
    
    # Gráfico de barras - tempo médio
    create_bar_chart(
        metrics_by_volume,
        'Tempo Médio de Resposta - Listagem de Comentários',
        'Tempo de Resposta (ms)',
        f'graphs/comments_mean_comparison_{timestamp}.png',
        'mean'
    )
    
    # Gráfico de barras - P95
    create_bar_chart(
        metrics_by_volume,
        'Percentil 95 (P95) - Listagem de Comentários',
        'Tempo de Resposta (ms)',
        f'graphs/comments_p95_comparison_{timestamp}.png',
        'p95'
    )
    
    # Boxplot
    data_by_volume = {
        name: [r['response_time_ms'] for r in results if r.get('success', False)]
        for name, results in results_by_video.items()
    }
    create_boxplot(
        data_by_volume,
        'Distribuição de Tempos de Resposta - Listagem de Comentários',
        'Tempo de Resposta (ms)',
        f'graphs/comments_boxplot_{timestamp}.png'
    )
    
    logger.info("\n" + "="*80)
    logger.info("✅ TESTES DE LISTAGEM DE COMENTÁRIOS CONCLUÍDOS")
    logger.info("="*80)
    logger.info(f"Arquivos gerados:")
    logger.info(f"  - {csv_file}")
    logger.info(f"  - {json_file}")
    logger.info(f"  - graphs/comments_mean_comparison_{timestamp}.png")
    logger.info(f"  - graphs/comments_p95_comparison_{timestamp}.png")
    logger.info(f"  - graphs/comments_boxplot_{timestamp}.png")
    
    return {
        'results': all_results,
        'metrics': metrics_by_volume,
        'files': {
            'csv': csv_file,
            'json': json_file,
            'graphs': [
                f'graphs/comments_mean_comparison_{timestamp}.png',
                f'graphs/comments_p95_comparison_{timestamp}.png',
                f'graphs/comments_boxplot_{timestamp}.png'
            ]
        }
    }


if __name__ == "__main__":
    import os
    os.makedirs('results', exist_ok=True)
    os.makedirs('graphs', exist_ok=True)
    run_comment_tests()


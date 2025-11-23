#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de TPS Máximo usando Locust - Ramp-up de Usuários

Este script aumenta gradualmente o número de usuários simultâneos para encontrar:
- TPS máximo sustentável
- Ponto de degradação de performance
- Ponto de falhas

Uso:
    locust -f locust_max_tps.py \
      --host=https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod \
      --headless \
      -u 50 \              # Máximo de usuários
      -r 5 \                # Ramp-up: 5 usuários por segundo
      -t 15m                # Duração total: 15 minutos
      --csv=results/locust_max_tps \
      --html=results/locust_max_tps_report.html
"""

from locust import HttpUser, task, between, events
import json
import time
import logging
from typing import Dict, Any
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: Configurar conforme necessário
VIDEO_ID = "dQw4w9WgXcQ"  # Rick Astley
SEARCH_KEYWORD = "python tutorial"

# Contadores globais para análise
request_stats = {
    'total_requests': 0,
    'total_failures': 0,
    'response_times': [],
    'start_time': None
}


class MaxTPSUser(HttpUser):
    """
    Usuário simulado para teste de TPS máximo.
    
    Foca em requisições frequentes para estressar a API.
    """
    
    # Espera mínima entre requisições (alta frequência)
    wait_time = between(0.1, 0.3)
    
    def on_start(self):
        """Chamado quando um usuário inicia."""
        if request_stats['start_time'] is None:
            request_stats['start_time'] = time.time()
    
    @task(5)
    def test_fetch_comments(self):
        """Testa endpoint de comentários (mais frequente - 5x mais que search)."""
        params = {
            "videoId": VIDEO_ID,
            "part": "snippet",
            "maxResults": 100,
            "showPositives": "true",
            "showNegatives": "true",
            "showNeutral": "true"
        }
        
        start_time = time.time()
        with self.client.get(
            "/video/comments",
            params=params,
            catch_response=True,
            name="/video/comments"
        ) as response:
            elapsed = (time.time() - start_time) * 1000  # ms
            
            request_stats['total_requests'] += 1
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "items" in data:
                        response.success()
                        request_stats['response_times'].append(elapsed)
                    else:
                        response.failure("No items in response")
                        request_stats['total_failures'] += 1
                except json.JSONDecodeError:
                    response.failure("Invalid JSON")
                    request_stats['total_failures'] += 1
            else:
                response.failure(f"Status {response.status_code}")
                request_stats['total_failures'] += 1
    
    @task(2)
    def test_search_videos(self):
        """Testa endpoint de busca de vídeos."""
        params = {
            "q": SEARCH_KEYWORD,
            "part": "snippet",
            "type": "video",
            "maxResults": 10
        }
        
        start_time = time.time()
        with self.client.get(
            "/search",
            params=params,
            catch_response=True,
            name="/search"
        ) as response:
            elapsed = (time.time() - start_time) * 1000  # ms
            
            request_stats['total_requests'] += 1
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "items" in data:
                        response.success()
                        request_stats['response_times'].append(elapsed)
                    else:
                        response.failure("No items in response")
                        request_stats['total_failures'] += 1
                except json.JSONDecodeError:
                    response.failure("Invalid JSON")
                    request_stats['total_failures'] += 1
            else:
                response.failure(f"Status {response.status_code}")
                request_stats['total_failures'] += 1


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Chamado quando o teste inicia."""
    logger.info("="*80)
    logger.info("TESTE DE TPS MÁXIMO - INICIANDO")
    logger.info("="*80)
    logger.info(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    request_stats['start_time'] = time.time()


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    Chamado quando o teste para.
    Gera relatório detalhado de TPS máximo.
    """
    stats = environment.stats
    total_time = time.time() - request_stats['start_time'] if request_stats['start_time'] else 0
    
    logger.info("\n" + "="*80)
    logger.info("RELATÓRIO FINAL - TPS MÁXIMO")
    logger.info("="*80)
    
    # Estatísticas gerais
    total_requests = stats.total.num_requests
    total_failures = stats.total.num_failures
    success_rate = ((total_requests - total_failures) / total_requests * 100) if total_requests > 0 else 0
    
    if total_time > 0:
        tps = total_requests / total_time
        max_tps = max([entry.num_requests / (entry.total_response_time / 1000) 
                      for entry in stats.entries.values() 
                      if entry.total_response_time > 0], default=0)
    else:
        tps = 0
        max_tps = 0
    
    logger.info(f"\n📊 ESTATÍSTICAS GERAIS:")
    logger.info(f"  Total de requisições: {total_requests:,}")
    logger.info(f"  Requisições falhadas: {total_failures:,}")
    logger.info(f"  Taxa de sucesso: {success_rate:.1f}%")
    logger.info(f"  Tempo total: {total_time:.1f}s ({total_time/60:.1f} minutos)")
    logger.info(f"")
    logger.info(f"🚀 THROUGHPUT (TPS):")
    logger.info(f"  TPS médio: {tps:.2f} transações/segundo")
    logger.info(f"  TPS máximo observado: {max_tps:.2f} transações/segundo")
    logger.info(f"  Requisições por minuto: {tps*60:.1f}")
    logger.info(f"  Requisições por hora: {tps*3600:.0f}")
    logger.info(f"")
    
    # Estatísticas de resposta
    if request_stats['response_times']:
        import statistics
        avg_time = statistics.mean(request_stats['response_times'])
        median_time = statistics.median(request_stats['response_times'])
        p95_time = sorted(request_stats['response_times'])[int(len(request_stats['response_times']) * 0.95)]
        min_time = min(request_stats['response_times'])
        max_time = max(request_stats['response_times'])
        
        logger.info(f"⏱️  TEMPO DE RESPOSTA:")
        logger.info(f"  Média: {avg_time:.0f}ms")
        logger.info(f"  Mediana: {median_time:.0f}ms")
        logger.info(f"  P95: {p95_time:.0f}ms")
        logger.info(f"  Mínimo: {min_time:.0f}ms")
        logger.info(f"  Máximo: {max_time:.0f}ms")
        logger.info(f"")
    
    # Estatísticas por endpoint
    logger.info(f"📈 ESTATÍSTICAS POR ENDPOINT:")
    for name, entry in sorted(stats.entries.items()):
        if name != "Aggregated" and entry.num_requests > 0:
            entry_time = entry.total_response_time / 1000  # Converter para segundos
            entry_tps = entry.num_requests / entry_time if entry_time > 0 else 0
            failure_rate = (entry.num_failures / entry.num_requests * 100) if entry.num_requests > 0 else 0
            
            logger.info(f"  {name}:")
            logger.info(f"    Requisições: {entry.num_requests:,}")
            logger.info(f"    Falhas: {entry.num_failures:,} ({failure_rate:.1f}%)")
            logger.info(f"    TPS: {entry_tps:.2f}")
            logger.info(f"    Tempo médio: {entry.avg_response_time:.0f}ms")
            logger.info(f"    Tempo mínimo: {entry.min_response_time:.0f}ms")
            logger.info(f"    Tempo máximo: {entry.max_response_time:.0f}ms")
            logger.info(f"")
    
    # Análise de capacidade
    logger.info(f"💡 ANÁLISE DE CAPACIDADE:")
    if success_rate >= 99:
        logger.info(f"  ✅ Taxa de sucesso excelente ({success_rate:.1f}%)")
        logger.info(f"  ✅ API suporta {tps:.2f} TPS com alta confiabilidade")
    elif success_rate >= 95:
        logger.info(f"  ⚠️  Taxa de sucesso boa ({success_rate:.1f}%)")
        logger.info(f"  ⚠️  Algumas falhas observadas - próximo do limite")
    elif success_rate >= 90:
        logger.info(f"  ⚠️  Taxa de sucesso aceitável ({success_rate:.1f}%)")
        logger.info(f"  ⚠️  API está próxima da capacidade máxima")
    else:
        logger.info(f"  ❌ Taxa de sucesso baixa ({success_rate:.1f}%)")
        logger.info(f"  ❌ API excedeu capacidade máxima - muitas falhas")
    
    logger.info(f"")
    logger.info(f"📋 RECOMENDAÇÕES:")
    if tps >= 2.0:
        logger.info(f"  ✅ TPS excelente (≥ 2.0) - API tem alta capacidade")
    elif tps >= 1.0:
        logger.info(f"  ✅ TPS bom (≥ 1.0) - API tem capacidade adequada")
    elif tps >= 0.5:
        logger.info(f"  ⚠️  TPS moderado (≥ 0.5) - Considere otimizações")
    else:
        logger.info(f"  ❌ TPS baixo (< 0.5) - API precisa de otimizações")
    
    logger.info(f"")
    logger.info("="*80)
    logger.info("✅ TESTE CONCLUÍDO")
    logger.info("="*80)
    logger.info("")
    logger.info("💾 Relatórios salvos:")
    logger.info("  - results/locust_max_tps_stats.csv")
    logger.info("  - results/locust_max_tps_failures.csv")
    logger.info("  - results/locust_max_tps_report.html (se gerado)")


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """Chamado a cada requisição para monitoramento em tempo real."""
    # Log a cada 100 requisições para não poluir muito
    if request_stats['total_requests'] % 100 == 0 and request_stats['total_requests'] > 0:
        elapsed = time.time() - request_stats['start_time'] if request_stats['start_time'] else 1
        current_tps = request_stats['total_requests'] / elapsed if elapsed > 0 else 0
        failure_rate = (request_stats['total_failures'] / request_stats['total_requests'] * 100) if request_stats['total_requests'] > 0 else 0
        
        logger.info(f"[Progresso] Requisições: {request_stats['total_requests']:,} | "
                   f"TPS atual: {current_tps:.2f} | "
                   f"Falhas: {request_stats['total_failures']} ({failure_rate:.1f}%)")


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Carga usando Locust - Medição de TPS

Este script executa testes de carga usando Locust para medir TPS (Transactions Per Second)
e capacidade máxima da API.

Uso:
    locust -f locust_test.py --host=https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod --headless -u 10 -r 2 -t 10m
"""

from locust import HttpUser, task, between, events
import json
import time
import logging
from typing import Dict, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: Configurar conforme necessário
VIDEO_ID = "dQw4w9WgXcQ"  # Rick Astley
SEARCH_KEYWORD = "python tutorial"


class APILoadTestUser(HttpUser):
    """
    Simula usuários fazendo requisições à API.
    
    Mede TPS (Transactions Per Second) e capacidade de carga.
    """
    
    # Espera entre 0.3-0.5 segundos entre tarefas (alta frequência)
    wait_time = between(0.3, 0.5)
    
    def on_start(self):
        """Chamado quando um usuário simulado inicia."""
        pass
    
    @task(3)
    def test_search_videos(self):
        """Testa endpoint de busca de vídeos."""
        params = {
            "q": SEARCH_KEYWORD,
            "part": "snippet",
            "type": "video",
            "maxResults": 10
        }
        
        with self.client.get(
            "/search",
            params=params,
            catch_response=True,
            name="/search"
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "items" in data:
                        response.success()
                    else:
                        response.failure("No items in response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON")
            else:
                response.failure(f"Status {response.status_code}")
    
    @task(5)
    def test_fetch_comments(self):
        """Testa endpoint de comentários (mais frequente)."""
        params = {
            "videoId": VIDEO_ID,
            "part": "snippet",
            "maxResults": 100,
            "showPositives": "true",
            "showNegatives": "true",
            "showNeutral": "true"
        }
        
        with self.client.get(
            "/video/comments",
            params=params,
            catch_response=True,
            name="/video/comments"
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "items" in data:
                        response.success()
                    else:
                        response.failure("No items in response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON")
            else:
                response.failure(f"Status {response.status_code}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    Chamado quando o teste de carga para.
    Imprime estatísticas de TPS.
    """
    stats = environment.stats
    
    logger.info("\n" + "="*80)
    logger.info("RESUMO DO TESTE DE CARGA - TPS")
    logger.info("="*80)
    
    total_requests = stats.total.num_requests
    total_failures = stats.total.num_failures
    total_time = stats.total.total_response_time / 1000  # Converter de ms para s
    avg_response_time = stats.total.avg_response_time
    
    if total_time > 0:
        tps = total_requests / total_time
    else:
        tps = 0
    
    logger.info(f"\nEstatísticas Gerais:")
    logger.info(f"  Total de requisições: {total_requests}")
    logger.info(f"  Requisições falhadas: {total_failures}")
    logger.info(f"  Taxa de sucesso: {((total_requests - total_failures) / total_requests * 100):.1f}%")
    logger.info(f"  Tempo total: {total_time:.1f}s")
    logger.info(f"  Tempo médio de resposta: {avg_response_time:.0f}ms")
    logger.info(f"")
    logger.info(f"TPS (Transactions Per Second):")
    logger.info(f"  TPS médio: {tps:.2f}")
    logger.info(f"  Requisições por minuto: {tps*60:.1f}")
    logger.info(f"  Requisições por hora: {tps*3600:.0f}")
    logger.info(f"")
    
    logger.info("Estatísticas por Endpoint:")
    for name, entry in stats.entries.items():
        if name != "Aggregated":
            entry_tps = entry.num_requests / (entry.total_response_time / 1000) if entry.total_response_time > 0 else 0
            logger.info(f"  {name}:")
            logger.info(f"    Requisições: {entry.num_requests}")
            logger.info(f"    Falhas: {entry.num_failures}")
            logger.info(f"    Tempo médio: {entry.avg_response_time:.0f}ms")
            logger.info(f"    TPS: {entry_tps:.2f}")
    
    logger.info("\n" + "="*80)


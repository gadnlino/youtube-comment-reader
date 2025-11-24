#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo comum com funções utilitárias para testes de performance

Contém:
- Funções de chamada HTTP
- Funções de medição de tempo
- Funções de agregação de métricas
- Funções de geração de gráficos
"""

import requests
import time
import statistics
import json
import csv
import logging
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar logging
def setup_logging(log_file: str = 'perf_test.log'):
    """Configura logging para arquivo e console."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

# Logger global (será inicializado nos scripts)
logger = None

# TODO: Ajustar a URL base da API conforme necessário
API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod"

# Configuração de estilo para gráficos
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 11


def make_request(endpoint: str, params: Optional[Dict[str, Any]] = None, timeout: int = 60) -> Dict[str, Any]:
    """
    Faz uma requisição HTTP e retorna o resultado com timing.
    
    Args:
        endpoint: Caminho do endpoint (ex: '/search', '/video/comments')
        params: Parâmetros da query string
        timeout: Timeout em segundos
    
    Returns:
        Dict com: response_time_ms, status_code, success, data, item_count
    """
    url = f"{API_BASE_URL}{endpoint}"
    params = params or {}
    
    start_time = time.time()
    try:
        response = requests.get(url, params=params, timeout=timeout)
        elapsed_ms = (time.time() - start_time) * 1000
        
        result = {
            'response_time_ms': elapsed_ms,
            'status_code': response.status_code,
            'success': 200 <= response.status_code < 300,
            'timestamp': datetime.now().isoformat()
        }
        
        if result['success']:
            try:
                data = response.json()
                result['data'] = data
                # Contar itens retornados
                if isinstance(data, dict):
                    if 'items' in data:
                        result['item_count'] = len(data.get('items', []))
                    elif 'pageInfo' in data:
                        result['item_count'] = data.get('pageInfo', {}).get('totalResults', 0)
                    else:
                        result['item_count'] = 0
                else:
                    result['item_count'] = 0
            except:
                result['data'] = None
                result['item_count'] = 0
        else:
            result['data'] = None
            result['item_count'] = 0
            result['error'] = response.text[:200]  # Primeiros 200 chars do erro
        
        return result
    except Exception as e:
        elapsed_ms = (time.time() - start_time) * 1000
        return {
            'response_time_ms': elapsed_ms,
            'status_code': 0,
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat(),
            'data': None,
            'item_count': 0
        }


def calculate_metrics(results: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Calcula métricas estatísticas de uma lista de resultados.
    
    Args:
        results: Lista de resultados com 'response_time_ms'
    
    Returns:
        Dict com média, mediana, p95, mínimo, máximo, desvio padrão
    """
    if not results:
        return {
            'mean': 0.0,
            'median': 0.0,
            'p95': 0.0,
            'min': 0.0,
            'max': 0.0,
            'std': 0.0,
            'count': 0
        }
    
    times = [r['response_time_ms'] for r in results if r.get('success', False)]
    
    if not times:
        return {
            'mean': 0.0,
            'median': 0.0,
            'p95': 0.0,
            'min': 0.0,
            'max': 0.0,
            'std': 0.0,
            'count': len(results),
            'success_count': 0
        }
    
    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'p95': np.percentile(times, 95),
        'min': min(times),
        'max': max(times),
        'std': statistics.stdev(times) if len(times) > 1 else 0.0,
        'count': len(results),
        'success_count': len(times)
    }


def save_results_csv(results: List[Dict[str, Any]], filename: str):
    """Salva resultados em arquivo CSV."""
    if not results:
        return
    
    # Flatten results for CSV
    rows = []
    for r in results:
        row = {
            'timestamp': r.get('timestamp', ''),
            'response_time_ms': r.get('response_time_ms', 0),
            'status_code': r.get('status_code', 0),
            'success': r.get('success', False),
            'item_count': r.get('item_count', 0),
            'scenario': r.get('scenario', ''),
            'params': json.dumps(r.get('params', {}))
        }
        if 'error' in r:
            row['error'] = r['error']
        rows.append(row)
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)


def save_results_json(results: List[Dict[str, Any]], metrics: Dict[str, Any], filename: str):
    """Salva resultados e métricas em arquivo JSON."""
    data = {
        'timestamp': datetime.now().isoformat(),
        'results': results,
        'metrics': metrics
    }
    
    # Adicionar TPS se disponível
    if results and 'timestamp' in results[0]:
        try:
            start_time = datetime.fromisoformat(results[0]['timestamp'])
            end_time = datetime.fromisoformat(results[-1]['timestamp'])
            total_time = (end_time - start_time).total_seconds()
            if total_time > 0:
                data['tps'] = len(results) / total_time
        except:
            pass
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def create_bar_chart(metrics_by_scenario: Dict[str, Dict[str, float]], 
                    title: str, 
                    ylabel: str,
                    filename: str,
                    metric_key: str = 'mean'):
    """
    Cria gráfico de barras comparando métricas por cenário.
    
    Args:
        metrics_by_scenario: Dict com cenário -> métricas
        title: Título do gráfico
        ylabel: Label do eixo Y
        filename: Nome do arquivo de saída
        metric_key: Chave da métrica a plotar (default: 'mean')
    """
    scenarios = list(metrics_by_scenario.keys())
    values = [metrics_by_scenario[s][metric_key] for s in scenarios]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(scenarios, values, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Adicionar valores nas barras
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val:.0f}ms',
               ha='center', va='bottom', fontweight='bold')
    
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(bottom=0)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico salvo: {filename}")


def create_boxplot(data_by_scenario: Dict[str, List[float]], 
                   title: str,
                   ylabel: str,
                   filename: str):
    """
    Cria gráfico boxplot comparando distribuições por cenário.
    
    Args:
        data_by_scenario: Dict com cenário -> lista de tempos
        title: Título do gráfico
        ylabel: Label do eixo Y
        filename: Nome do arquivo de saída
    """
    scenarios = list(data_by_scenario.keys())
    data = [data_by_scenario[s] for s in scenarios]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bp = ax.boxplot(data, labels=scenarios, patch_artist=True, showmeans=True)
    
    # Colorir boxes
    colors = sns.color_palette("husl", len(scenarios))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(bottom=0)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico salvo: {filename}")


def create_time_series_plot(results: List[Dict[str, Any]], 
                           title: str,
                           ylabel: str,
                           filename: str):
    """
    Cria gráfico de série temporal.
    
    Args:
        results: Lista de resultados ordenados por timestamp
        title: Título do gráfico
        ylabel: Label do eixo Y
        filename: Nome do arquivo de saída
    """
    times = [r['response_time_ms'] for r in results]
    x_values = range(len(times))
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(x_values, times, marker='o', markersize=4, linewidth=1.5, 
           alpha=0.7, color='#3498db', markeredgecolor='white', markeredgewidth=0.3)
    
    # Linha de média
    mean_time = statistics.mean(times) if times else 0
    ax.axhline(y=mean_time, color='red', linestyle='--', linewidth=2,
              alpha=0.8, label=f'Média: {mean_time:.0f}ms')
    
    # Linha de mediana
    median_time = statistics.median(times) if times else 0
    ax.axhline(y=median_time, color='orange', linestyle='--', linewidth=2,
              alpha=0.8, label=f'Mediana: {median_time:.0f}ms')
    
    ax.set_xlabel('Requisição', fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico salvo: {filename}")


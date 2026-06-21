#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera gráficos consolidados comparando todos os testes de carga realizados.

Cria visualizações comparativas:
- TPS por número de usuários
- Taxa de sucesso por número de usuários
- Tempo de resposta por número de usuários
- Comparação de endpoints
- Dashboard consolidado
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import json
from pathlib import Path

# Configuração de estilo
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'sans-serif'

# Dados consolidados dos testes
TESTES = [
    {
        'nome': 'Teste 1',
        'usuarios': 50,
        'duracao': '15min',
        'tps_medio': 60.18,
        'taxa_sucesso': 100.0,
        'tempo_medio': 624,
        'p95': 1100,
        'requisicoes': 54124,
        'falhas': 2,
        'endpoint_search_tps': 17.28,
        'endpoint_search_tempo': 538,
        'endpoint_comments_tps': 42.90,
        'endpoint_comments_tempo': 659,
        'pasta': 'teste_1'
    },
    {
        'nome': 'Teste 2',
        'usuarios': 100,
        'duracao': '15min',
        'tps_medio': 133.37,
        'taxa_sucesso': 100.0,
        'tempo_medio': 544,
        'p95': 1074,
        'requisicoes': 119978,
        'falhas': 29,
        'endpoint_search_tps': 38.41,
        'endpoint_search_tempo': 407,
        'endpoint_comments_tps': 94.96,
        'endpoint_comments_tempo': 600,
        'pasta': 'teste_2'
    },
    {
        'nome': 'Teste 3 - Smoke',
        'usuarios': 300,
        'duracao': '3min',
        'tps_medio': 384.86,
        'taxa_sucesso': 100.0,
        'tempo_medio': 557,
        'p95': 1077,
        'requisicoes': 69145,
        'falhas': 0,
        'endpoint_search_tps': 109.30,
        'endpoint_search_tempo': 462,
        'endpoint_comments_tps': 275.58,
        'endpoint_comments_tempo': 595,
        'pasta': 'teste_3/smoke_test_300'
    },
    {
        'nome': 'Teste 3 - Smoke 500',
        'usuarios': 500,
        'duracao': '3min',
        'tps_medio': 459.90,
        'taxa_sucesso': 97.7,
        'tempo_medio': 851,
        'p95': 1740,
        'requisicoes': 82648,
        'falhas': 1925,
        'endpoint_search_tps': 132.07,
        'endpoint_search_tempo': 800,
        'endpoint_comments_tps': 327.88,
        'endpoint_comments_tempo': 875,
        'pasta': 'teste_3/smoke_test_500'
    },
    {
        'nome': 'Teste 3 - Completo',
        'usuarios': 300,
        'duracao': '15min',
        'tps_medio': 416.32,
        'taxa_sucesso': 76.5,
        'tempo_medio': 567,
        'p95': 1068,
        'requisicoes': 374584,
        'falhas': 87979,
        'endpoint_search_tps': 118.92,
        'endpoint_search_tempo': 363,
        'endpoint_comments_tps': 297.40,
        'endpoint_comments_tempo': 572,
        'pasta': 'teste_3'
    }
]

def create_tps_comparison():
    """Gráfico comparativo de TPS por número de usuários."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Separar testes de 15min e 3min
    testes_15min = [t for t in TESTES if t['duracao'] == '15min']
    testes_3min = [t for t in TESTES if t['duracao'] == '3min']
    
    usuarios_15min = [t['usuarios'] for t in testes_15min]
    tps_15min = [t['tps_medio'] for t in testes_15min]
    
    usuarios_3min = [t['usuarios'] for t in testes_3min]
    tps_3min = [t['tps_medio'] for t in testes_3min]
    
    # Plot
    ax.plot(usuarios_15min, tps_15min, marker='o', markersize=10, 
           linewidth=2.5, label='Testes de 15 minutos', color='#2ecc71')
    ax.plot(usuarios_3min, tps_3min, marker='s', markersize=10, 
           linewidth=2.5, label='Smoke tests (3 minutos)', color='#e74c3c', linestyle='--')
    
    # Adicionar valores nos pontos
    for i, (u, t) in enumerate(zip(usuarios_15min, tps_15min)):
        ax.annotate(f'{t:.1f}', (u, t), textcoords="offset points", 
                   xytext=(0,10), ha='center', fontsize=9, fontweight='bold')
    
    for i, (u, t) in enumerate(zip(usuarios_3min, tps_3min)):
        ax.annotate(f'{t:.1f}', (u, t), textcoords="offset points", 
                   xytext=(0,10), ha='center', fontsize=9, fontweight='bold')
    
    ax.set_xlabel('Número de Usuários Simultâneos', fontsize=12, fontweight='bold')
    ax.set_ylabel('TPS (Transactions Per Second)', fontsize=12, fontweight='bold')
    ax.set_title('Comparação de TPS por Número de Usuários', 
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    output_file = 'consolidated_graphs/tps_comparison.png'
    os.makedirs('consolidated_graphs', exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico salvo: {output_file}")


def create_success_rate_comparison():
    """Gráfico comparativo de taxa de sucesso."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    usuarios = [t['usuarios'] for t in TESTES]
    taxa_sucesso = [t['taxa_sucesso'] for t in TESTES]
    nomes = [t['nome'] for t in TESTES]
    
    # Cores baseadas na taxa de sucesso
    cores = ['#2ecc71' if ts >= 99 else '#f39c12' if ts >= 95 else '#e74c3c' 
             for ts in taxa_sucesso]
    
    bars = ax.bar(range(len(TESTES)), taxa_sucesso, color=cores, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Adicionar valores nas barras
    for i, (bar, taxa) in enumerate(zip(bars, taxa_sucesso)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{taxa:.1f}%',
               ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Teste', fontsize=12, fontweight='bold')
    ax.set_ylabel('Taxa de Sucesso (%)', fontsize=12, fontweight='bold')
    ax.set_title('Taxa de Sucesso por Teste', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(range(len(TESTES)))
    # Criar labels diferenciados
    labels = []
    for t in TESTES:
        if t['nome'] == 'Teste 3 - Smoke':
            labels.append(f"{t['nome']}\n(300u - S)")
        elif t['nome'] == 'Teste 3 - Completo':
            labels.append(f"{t['nome']}\n(300u - C)")
        else:
            labels.append(f"{t['nome']}\n({t['usuarios']} users)")
    ax.set_xticklabels(labels, rotation=15, ha='right', fontsize=9)
    ax.set_ylim([0, 105])
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # Linha de referência 95%
    ax.axhline(y=95, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Limite recomendado (95%)')
    ax.legend(loc='upper right', fontsize=10)
    
    plt.tight_layout()
    output_file = 'consolidated_graphs/success_rate_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico salvo: {output_file}")


def create_response_time_comparison():
    """Gráfico comparativo de tempo de resposta."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    usuarios = [t['usuarios'] for t in TESTES]
    tempo_medio = [t['tempo_medio'] for t in TESTES]
    p95 = [t['p95'] for t in TESTES]
    nomes = [t['nome'] for t in TESTES]
    
    # Gráfico 1: Tempo médio
    x = np.arange(len(TESTES))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, tempo_medio, width, label='Tempo Médio', 
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=1)
    bars2 = ax1.bar(x + width/2, p95, width, label='P95', 
                   color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1)
    
    ax1.set_xlabel('Teste', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Tempo de Resposta (ms)', fontsize=12, fontweight='bold')
    ax1.set_title('Tempo de Resposta - Média e P95', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    # Criar labels diferenciados
    labels = []
    for t in TESTES:
        if t['nome'] == 'Teste 3 - Smoke':
            labels.append(f"300u (S)")
        elif t['nome'] == 'Teste 3 - Completo':
            labels.append(f"300u (C)")
        else:
            labels.append(f"{t['usuarios']}u")
    ax1.set_xticklabels(labels, fontsize=9)
    ax1.legend(loc='upper left', fontsize=10)
    ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # Adicionar valores
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    # Gráfico 2: Tempo por número de usuários (linha)
    testes_15min = [t for t in TESTES if t['duracao'] == '15min']
    testes_3min = [t for t in TESTES if t['duracao'] == '3min']
    
    usuarios_15min = [t['usuarios'] for t in testes_15min]
    tempo_15min = [t['tempo_medio'] for t in testes_15min]
    
    usuarios_3min = [t['usuarios'] for t in testes_3min]
    tempo_3min = [t['tempo_medio'] for t in testes_3min]
    
    ax2.plot(usuarios_15min, tempo_15min, marker='o', markersize=10, 
            linewidth=2.5, label='Testes de 15min (Média)', color='#2ecc71')
    ax2.plot(usuarios_3min, tempo_3min, marker='s', markersize=10, 
            linewidth=2.5, label='Smoke tests 3min (Média)', color='#e74c3c', linestyle='--')
    
    ax2.set_xlabel('Número de Usuários Simultâneos', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Tempo de Resposta (ms)', fontsize=12, fontweight='bold')
    ax2.set_title('Tempo de Resposta por Número de Usuários', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend(loc='upper left', fontsize=10)
    ax2.set_ylim(bottom=0)
    
    plt.tight_layout()
    output_file = 'consolidated_graphs/response_time_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico salvo: {output_file}")


def create_endpoint_comparison():
    """Gráfico comparativo de performance por endpoint."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Filtrar apenas testes de 15min para comparação justa
    testes_15min = [t for t in TESTES if t['duracao'] == '15min']
    
    usuarios = [t['usuarios'] for t in testes_15min]
    search_tps = [t['endpoint_search_tps'] for t in testes_15min]
    comments_tps = [t['endpoint_comments_tps'] for t in testes_15min]
    
    search_tempo = [t['endpoint_search_tempo'] for t in testes_15min]
    comments_tempo = [t['endpoint_comments_tempo'] for t in testes_15min]
    
    # Gráfico 1: TPS por endpoint
    x = np.arange(len(testes_15min))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, search_tps, width, label='/search', 
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=1)
    bars2 = ax1.bar(x + width/2, comments_tps, width, label='/video/comments', 
                   color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1)
    
    ax1.set_xlabel('Teste', fontsize=12, fontweight='bold')
    ax1.set_ylabel('TPS', fontsize=12, fontweight='bold')
    ax1.set_title('TPS por Endpoint (Testes de 15min)', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"{t['usuarios']} users" for t in testes_15min], fontsize=9)
    ax1.legend(loc='upper left', fontsize=10)
    ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # Gráfico 2: Tempo de resposta por endpoint
    bars3 = ax2.bar(x - width/2, search_tempo, width, label='/search', 
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=1)
    bars4 = ax2.bar(x + width/2, comments_tempo, width, label='/video/comments', 
                   color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1)
    
    ax2.set_xlabel('Teste', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Tempo de Resposta (ms)', fontsize=12, fontweight='bold')
    ax2.set_title('Tempo de Resposta por Endpoint (Testes de 15min)', fontsize=13, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"{t['usuarios']} users" for t in testes_15min], fontsize=9)
    ax2.legend(loc='upper left', fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # Adicionar valores
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax = ax1 if bars in [bars1, bars2] else ax2
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    plt.tight_layout()
    output_file = 'consolidated_graphs/endpoint_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico salvo: {output_file}")


def create_consolidated_graphs_part1():
    """Primeiros 3 gráficos consolidados (TPS, Taxa Sucesso, Tempo Resposta)."""
    fig = plt.figure(figsize=(20, 7))
    gs = fig.add_gridspec(1, 3, hspace=0.1, wspace=0.15, top=0.96, bottom=0.07, left=0.03, right=0.995)
    
    # 1. TPS por usuários (linha)
    ax1 = fig.add_subplot(gs[0, 0])
    testes_15min = [t for t in TESTES if t['duracao'] == '15min']
    testes_3min = [t for t in TESTES if t['duracao'] == '3min']
    
    usuarios_15min = [t['usuarios'] for t in testes_15min]
    tps_15min = [t['tps_medio'] for t in testes_15min]
    usuarios_3min = [t['usuarios'] for t in testes_3min]
    tps_3min = [t['tps_medio'] for t in testes_3min]
    
    ax1.plot(usuarios_15min, tps_15min, marker='o', markersize=10, linewidth=2.5, label='15min', color='#2ecc71')
    ax1.plot(usuarios_3min, tps_3min, marker='s', markersize=10, linewidth=2.5, label='3min', color='#e74c3c', linestyle='--')
    ax1.set_xlabel('Usuários', fontsize=15, fontweight='bold')
    ax1.set_ylabel('TPS', fontsize=15, fontweight='bold')
    ax1.set_title('TPS por Usuários', fontsize=16, fontweight='bold', pad=15)
    ax1.tick_params(labelsize=13)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=13)
    
    # 2. Taxa de sucesso (barras)
    ax2 = fig.add_subplot(gs[0, 1])
    usuarios = [t['usuarios'] for t in TESTES]
    taxa_sucesso = [t['taxa_sucesso'] for t in TESTES]
    cores = ['#2ecc71' if ts >= 99 else '#f39c12' if ts >= 95 else '#e74c3c' for ts in taxa_sucesso]
    bars = ax2.bar(range(len(TESTES)), taxa_sucesso, color=cores, alpha=0.8, edgecolor='black', linewidth=1.5)
    # Adicionar valores nas barras
    for i, (bar, taxa) in enumerate(zip(bars, taxa_sucesso)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{taxa:.1f}%',
                ha='center', va='bottom', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Teste', fontsize=15, fontweight='bold')
    ax2.set_ylabel('Taxa Sucesso (%)', fontsize=15, fontweight='bold')
    ax2.set_title('Taxa de Sucesso', fontsize=16, fontweight='bold', pad=15)
    ax2.set_xticks(range(len(TESTES)))
    # Criar labels diferenciados
    labels = []
    for t in TESTES:
        if t['nome'] == 'Teste 3 - Smoke':
            labels.append(f"300u (S)")
        elif t['nome'] == 'Teste 3 - Completo':
            labels.append(f"300u (C)")
        else:
            labels.append(f"{t['usuarios']}u")
    ax2.set_xticklabels(labels, fontsize=13, rotation=45, ha='right')
    ax2.tick_params(labelsize=13)
    ax2.set_ylim([0, 105])
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.axhline(y=95, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Limite 95%')
    ax2.legend(fontsize=13, loc='upper right')
    
    # 3. Tempo de resposta (barras)
    ax3 = fig.add_subplot(gs[0, 2])
    tempo_medio = [t['tempo_medio'] for t in TESTES]
    p95 = [t['p95'] for t in TESTES]
    x = np.arange(len(TESTES))
    width = 0.35
    bars1 = ax3.bar(x - width/2, tempo_medio, width, label='Média', color='#3498db', alpha=0.8, edgecolor='black', linewidth=1)
    bars2 = ax3.bar(x + width/2, p95, width, label='P95', color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1)
    # Adicionar valores
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Teste', fontsize=15, fontweight='bold')
    ax3.set_ylabel('Tempo (ms)', fontsize=15, fontweight='bold')
    ax3.set_title('Tempo de Resposta', fontsize=16, fontweight='bold', pad=15)
    ax3.set_xticks(x)
    # Criar labels diferenciados
    labels = []
    for t in TESTES:
        if t['nome'] == 'Teste 3 - Smoke':
            labels.append(f"300u (S)")
        elif t['nome'] == 'Teste 3 - Completo':
            labels.append(f"300u (C)")
        else:
            labels.append(f"{t['usuarios']}u")
    ax3.set_xticklabels(labels, fontsize=13)
    ax3.tick_params(labelsize=13)
    ax3.legend(fontsize=13)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Salvar parte 1
    output_file = 'consolidated_graphs/consolidated_graphs_part1.png'
    os.makedirs('consolidated_graphs', exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print(f"✓ Gráficos consolidados (Parte 1) salvo: {output_file}")


def create_consolidated_graphs_part2():
    """Últimos 3 gráficos consolidados (TPS Endpoint, Requisições, Taxa Falhas)."""
    fig = plt.figure(figsize=(20, 7))
    gs = fig.add_gridspec(1, 3, hspace=0.1, wspace=0.15, top=0.96, bottom=0.07, left=0.03, right=0.995)
    
    # 4. TPS por endpoint (testes 15min)
    ax4 = fig.add_subplot(gs[0, 0])
    testes_15min = [t for t in TESTES if t['duracao'] == '15min']
    search_tps = [t['endpoint_search_tps'] for t in testes_15min]
    comments_tps = [t['endpoint_comments_tps'] for t in testes_15min]
    usuarios_15min = [t['usuarios'] for t in testes_15min]
    x = np.arange(len(testes_15min))
    width = 0.35
    bars1 = ax4.bar(x - width/2, search_tps, width, label='/search', color='#3498db', alpha=0.8, edgecolor='black', linewidth=1)
    bars2 = ax4.bar(x + width/2, comments_tps, width, label='/video/comments', color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1)
    # Adicionar valores
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Teste (15min)', fontsize=15, fontweight='bold')
    ax4.set_ylabel('TPS', fontsize=15, fontweight='bold')
    ax4.set_title('TPS por Endpoint', fontsize=16, fontweight='bold', pad=15)
    ax4.set_xticks(x)
    ax4.set_xticklabels([f"{u}u" for u in usuarios_15min], fontsize=13)
    ax4.tick_params(labelsize=13)
    ax4.legend(fontsize=13)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 5. Requisições totais
    ax5 = fig.add_subplot(gs[0, 1])
    requisicoes = [t['requisicoes'] for t in TESTES]
    bars = ax5.bar(range(len(TESTES)), requisicoes, color='#9b59b6', alpha=0.8, edgecolor='black', linewidth=1.5)
    # Adicionar valores
    for i, (bar, req) in enumerate(zip(bars, requisicoes)):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{req/1000:.0f}k',
                ha='center', va='bottom', fontsize=13, fontweight='bold')
    ax5.set_xlabel('Teste', fontsize=15, fontweight='bold')
    ax5.set_ylabel('Requisições', fontsize=15, fontweight='bold')
    ax5.set_title('Total de Requisições', fontsize=16, fontweight='bold', pad=15)
    ax5.set_xticks(range(len(TESTES)))
    # Criar labels diferenciados
    labels = []
    for t in TESTES:
        if t['nome'] == 'Teste 3 - Smoke':
            labels.append(f"300u (S)")
        elif t['nome'] == 'Teste 3 - Completo':
            labels.append(f"300u (C)")
        else:
            labels.append(f"{t['usuarios']}u")
    ax5.set_xticklabels(labels, fontsize=13, rotation=45, ha='right')
    ax5.tick_params(labelsize=13)
    ax5.grid(True, alpha=0.3, axis='y')
    # Formatar eixo Y
    ax5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k'))
    
    # 6. Taxa de falhas
    ax6 = fig.add_subplot(gs[0, 2])
    taxa_falhas = [100 - t['taxa_sucesso'] for t in TESTES]
    cores_falhas = ['#2ecc71' if tf < 1 else '#f39c12' if tf < 5 else '#e74c3c' for tf in taxa_falhas]
    bars = ax6.bar(range(len(TESTES)), taxa_falhas, color=cores_falhas, alpha=0.8, edgecolor='black', linewidth=1.5)
    # Adicionar valores
    for i, (bar, tf) in enumerate(zip(bars, taxa_falhas)):
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height,
                f'{tf:.1f}%',
                ha='center', va='bottom', fontsize=13, fontweight='bold')
    ax6.set_xlabel('Teste', fontsize=15, fontweight='bold')
    ax6.set_ylabel('Taxa de Falhas (%)', fontsize=15, fontweight='bold')
    ax6.set_title('Taxa de Falhas', fontsize=16, fontweight='bold', pad=15)
    ax6.set_xticks(range(len(TESTES)))
    # Criar labels diferenciados
    labels = []
    for t in TESTES:
        if t['nome'] == 'Teste 3 - Smoke':
            labels.append(f"300u (S)")
        elif t['nome'] == 'Teste 3 - Completo':
            labels.append(f"300u (C)")
        else:
            labels.append(f"{t['usuarios']}u")
    ax6.set_xticklabels(labels, fontsize=13, rotation=45, ha='right')
    ax6.tick_params(labelsize=13)
    ax6.grid(True, alpha=0.3, axis='y')
    
    # Salvar parte 2
    output_file = 'consolidated_graphs/consolidated_graphs_part2.png'
    os.makedirs('consolidated_graphs', exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print(f"✓ Gráficos consolidados (Parte 2) salvo: {output_file}")


def create_consolidated_table_only():
    """Tabela consolidada separada."""
    fig, ax = plt.subplots(figsize=(18, 6))
    ax.axis('off')
    
    # Criar tabela
    table_data = []
    headers = ['Teste', 'Usuários', 'Duração', 'TPS Médio', 'Taxa Sucesso', 'Tempo Médio (ms)', 'P95 (ms)', 'Requisições']
    
    for t in TESTES:
        table_data.append([
            t['nome'],
            str(t['usuarios']),
            t['duracao'],
            f"{t['tps_medio']:.2f}",
            f"{t['taxa_sucesso']:.1f}%",
            str(int(t['tempo_medio'])),
            str(int(t['p95'])),
            f"{t['requisicoes']:,}"
        ])
    
    table = ax.table(cellText=table_data, colLabels=headers, 
                     cellLoc='center', loc='center',
                     colWidths=[0.15, 0.08, 0.08, 0.12, 0.12, 0.12, 0.12, 0.15])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 3)
    
    # Colorir células baseado em taxa de sucesso
    for i in range(len(table_data)):
        taxa = TESTES[i]['taxa_sucesso']
        if taxa >= 99:
            color = '#d4edda'  # Verde claro
        elif taxa >= 95:
            color = '#fff3cd'  # Amarelo claro
        else:
            color = '#f8d7da'  # Vermelho claro
        
        for j in range(len(headers)):
            table[(i+1, j)].set_facecolor(color)
            table[(i+1, j)].set_text_props(fontsize=12)
    
    # Cabeçalho
    for j in range(len(headers)):
        table[(0, j)].set_facecolor('#343a40')
        table[(0, j)].set_text_props(weight='bold', color='white', fontsize=13)
    
    ax.set_title('Resumo Consolidado de Todos os Testes', 
                 fontsize=16, fontweight='bold', pad=20)
    
    output_file = 'consolidated_graphs/consolidated_table_only.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', pad_inches=0.3)
    plt.close()
    print(f"✓ Tabela consolidada salva: {output_file}")


def create_consolidated_dashboard():
    """Dashboard consolidado com múltiplas métricas (gera duas imagens separadas)."""
    create_consolidated_graphs_part1()
    create_consolidated_graphs_part2()
    create_consolidated_table_only()


def main():
    print("="*80)
    print("GERANDO GRÁFICOS CONSOLIDADOS")
    print("="*80)
    
    os.makedirs('consolidated_graphs', exist_ok=True)
    
    print("\nGerando gráficos...")
    create_tps_comparison()
    create_success_rate_comparison()
    create_response_time_comparison()
    create_endpoint_comparison()
    create_consolidated_dashboard()  # Agora gera duas imagens separadas
    
    print("\n" + "="*80)
    print("✅ GRÁFICOS CONSOLIDADOS GERADOS COM SUCESSO")
    print("="*80)
    print(f"Diretório: consolidated_graphs/")
    print("\nGráficos gerados:")
    print("  1. tps_comparison.png - Comparação de TPS")
    print("  2. success_rate_comparison.png - Taxa de sucesso")
    print("  3. response_time_comparison.png - Tempo de resposta")
    print("  4. endpoint_comparison.png - Comparação de endpoints")
    print("  5. consolidated_graphs_part1.png - Dashboard Parte 1 (TPS, Taxa Sucesso, Tempo Resposta)")
    print("  6. consolidated_graphs_part2.png - Dashboard Parte 2 (TPS Endpoint, Requisições, Taxa Falhas)")
    print("  7. consolidated_table_only.png - Tabela resumo (para referência)")


if __name__ == "__main__":
    main()


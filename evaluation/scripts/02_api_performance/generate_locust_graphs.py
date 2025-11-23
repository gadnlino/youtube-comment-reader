#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera gráficos a partir dos resultados do Locust

Lê os arquivos CSV gerados pelo Locust e cria visualizações:
- TPS ao longo do tempo
- Tempo de resposta ao longo do tempo
- Distribuição de tempos de resposta
- Taxa de falhas
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import glob
import os
from datetime import datetime

# Configuração de estilo
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'sans-serif'


def load_locust_stats(csv_file):
    """Carrega estatísticas do Locust do arquivo CSV."""
    df = pd.read_csv(csv_file)
    return df


def load_locust_history(csv_file):
    """Carrega histórico de estatísticas do Locust (mais detalhado)."""
    try:
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        print(f"⚠️  Erro ao carregar histórico: {e}")
        return None


def create_tps_over_time_graph(df_history, output_dir, timestamp):
    """Cria gráfico de TPS ao longo do tempo usando histórico."""
    if df_history is None or len(df_history) == 0:
        print("⚠️  Dados de histórico não disponíveis")
        return
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # O histórico tem colunas como 'Current RPS' ou podemos calcular
    if 'Current RPS' in df_history.columns:
        tps_data = df_history['Current RPS']
        time_data = df_history['Timestamp'] if 'Timestamp' in df_history.columns else df_history.index
    elif 'Total Request Count' in df_history.columns:
        df_sorted = df_history.sort_values('Timestamp' if 'Timestamp' in df_history.columns else df_history.index).reset_index(drop=True)
        df_sorted['Requests_Diff'] = df_sorted['Total Request Count'].diff()
        if 'Timestamp' in df_sorted.columns:
            df_sorted['Time_Diff'] = df_sorted['Timestamp'].diff()
            time_data = df_sorted['Timestamp']
        else:
            df_sorted['Time_Diff'] = 1  # Assumir 1 segundo entre registros
            time_data = df_sorted.index
        tps_data = df_sorted['Requests_Diff'] / df_sorted['Time_Diff'].replace(0, 1)
    else:
        print("⚠️  Não foi possível calcular TPS")
        return
    
    ax.plot(time_data, tps_data, 
           linewidth=2, color='#3498db', alpha=0.8, label='TPS')
    
    # Linha de média
    mean_tps = tps_data.mean()
    ax.axhline(y=mean_tps, color='red', linestyle='--', linewidth=2,
              alpha=0.8, label=f'Média: {mean_tps:.2f} TPS')
    
    ax.set_xlabel('Tempo (segundos)', fontsize=12, fontweight='bold')
    ax.set_ylabel('TPS (Transactions Per Second)', fontsize=12, fontweight='bold')
    ax.set_title('TPS ao Longo do Tempo - Teste de Carga', 
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    output_file = f'{output_dir}/tps_over_time_{timestamp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico salvo: {output_file}")


def create_response_time_graph(df_history, output_dir, timestamp):
    """Cria gráfico de tempo de resposta ao longo do tempo."""
    if df_history is None or len(df_history) == 0:
        print("⚠️  Dados de histórico não disponíveis")
        return
    
    # Procurar colunas de tempo de resposta
    time_cols = [col for col in df_history.columns if 'Response Time' in col or 'response_time' in col.lower()]
    if not time_cols:
        print("⚠️  Colunas de tempo de resposta não encontradas")
        return
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    time_col = 'Timestamp' if 'Timestamp' in df_history.columns else df_history.index
    time_data = df_history[time_col] if isinstance(time_col, str) else df_history.index
    
    if 'Average Response Time' in df_history.columns:
        ax.plot(time_data, df_history['Average Response Time'],
               linewidth=2, color='#e74c3c', alpha=0.8, label='Tempo Médio')
    
    if 'Median Response Time' in df_history.columns:
        ax.plot(time_data, df_history['Median Response Time'],
               linewidth=2, color='#2ecc71', alpha=0.8, label='Mediana')
    
    if '95%' in df_history.columns:
        ax.plot(time_data, df_history['95%'],
               linewidth=1.5, color='#f39c12', alpha=0.7, linestyle='--', label='P95')
    
    # Linha de média geral
    if 'Average Response Time' in df_history.columns:
        mean_time = df_history['Average Response Time'].mean()
        ax.axhline(y=mean_time, color='red', linestyle='--', linewidth=2,
                  alpha=0.6, label=f'Média: {mean_time:.0f}ms')
    
    ax.set_xlabel('Tempo (segundos)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Tempo de Resposta (ms)', fontsize=12, fontweight='bold')
    ax.set_title('Tempo de Resposta ao Longo do Tempo - Teste de Carga',
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    output_file = f'{output_dir}/response_time_over_time_{timestamp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico salvo: {output_file}")


def create_failure_rate_graph(df_history, output_dir, timestamp):
    """Cria gráfico de taxa de falhas ao longo do tempo."""
    if df_history is None or len(df_history) == 0:
        print("⚠️  Dados de histórico não disponíveis")
        return
    
    if 'Total Failure Count' not in df_history.columns or 'Total Request Count' not in df_history.columns:
        print("⚠️  Colunas necessárias não encontradas")
        return
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    time_col = 'Timestamp' if 'Timestamp' in df_history.columns else df_history.index
    time_data = df_history[time_col] if isinstance(time_col, str) else df_history.index
    
    df_history['Failure_Rate'] = (df_history['Total Failure Count'] / 
                                 df_history['Total Request Count'] * 100).fillna(0)
    
    ax.plot(time_data, df_history['Failure_Rate'],
           linewidth=2, color='#e74c3c', alpha=0.8, label='Taxa de Falhas')
    
    # Linha de média
    mean_failure = df_history['Failure_Rate'].mean()
    ax.axhline(y=mean_failure, color='orange', linestyle='--', linewidth=2,
              alpha=0.6, label=f'Média: {mean_failure:.2f}%')
    
    ax.set_xlabel('Tempo (segundos)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Taxa de Falhas (%)', fontsize=12, fontweight='bold')
    ax.set_title('Taxa de Falhas ao Longo do Tempo - Teste de Carga',
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    output_file = f'{output_dir}/failure_rate_over_time_{timestamp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gráfico salvo: {output_file}")


def create_summary_dashboard(df_stats, df_history, output_dir, timestamp):
    """Cria dashboard resumo com múltiplas métricas."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Usar histórico se disponível, senão usar stats
    df_to_plot = df_history if df_history is not None and len(df_history) > 0 else df_stats
    
    if df_to_plot is None or len(df_to_plot) == 0:
        print("⚠️  Sem dados para criar dashboard")
        return
    
    time_col = 'Timestamp' if 'Timestamp' in df_to_plot.columns else df_to_plot.index
    time_data = df_to_plot[time_col] if isinstance(time_col, str) else df_to_plot.index
    
    # 1. TPS
    if 'Requests/s' in df_to_plot.columns:
        axes[0, 0].plot(time_data, df_to_plot['Requests/s'], 
                        linewidth=2, color='#3498db')
        axes[0, 0].set_title('TPS ao Longo do Tempo', fontweight='bold')
        axes[0, 0].set_xlabel('Tempo (s)')
        axes[0, 0].set_ylabel('TPS')
        axes[0, 0].grid(True, alpha=0.3)
    elif 'Total Request Count' in df_to_plot.columns and len(df_to_plot) > 1:
        df_sorted = df_to_plot.sort_values(time_col if isinstance(time_col, str) else df_to_plot.index).reset_index(drop=True)
        df_sorted['Requests_Diff'] = df_sorted['Total Request Count'].diff()
        if isinstance(time_col, str) and time_col in df_sorted.columns:
            df_sorted['Time_Diff'] = df_sorted[time_col].diff()
            axes[0, 0].plot(df_sorted[time_col], df_sorted['Requests_Diff'] / df_sorted['Time_Diff'].replace(0, 1),
                            linewidth=2, color='#3498db')
        else:
            axes[0, 0].plot(df_sorted.index, df_sorted['Requests_Diff'],
                            linewidth=2, color='#3498db')
        axes[0, 0].set_title('TPS ao Longo do Tempo', fontweight='bold')
        axes[0, 0].set_xlabel('Tempo (s)')
        axes[0, 0].set_ylabel('TPS')
        axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Tempo de Resposta
    if 'Total Average Response Time' in df_to_plot.columns:
        axes[0, 1].plot(time_data, df_to_plot['Total Average Response Time'],
                       linewidth=2, color='#e74c3c')
        axes[0, 1].set_title('Tempo Médio de Resposta', fontweight='bold')
        axes[0, 1].set_xlabel('Tempo (s)')
        axes[0, 1].set_ylabel('Tempo (ms)')
        axes[0, 1].grid(True, alpha=0.3)
    elif 'Average Response Time' in df_to_plot.columns:
        axes[0, 1].plot(time_data, df_to_plot['Average Response Time'],
                       linewidth=2, color='#e74c3c')
        axes[0, 1].set_title('Tempo Médio de Resposta', fontweight='bold')
        axes[0, 1].set_xlabel('Tempo (s)')
        axes[0, 1].set_ylabel('Tempo (ms)')
        axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Taxa de Falhas
    if 'Total Failure Count' in df_to_plot.columns and 'Total Request Count' in df_to_plot.columns:
        failure_rate = (df_to_plot['Total Failure Count'] / 
                            df_to_plot['Total Request Count'] * 100).fillna(0)
        axes[1, 0].plot(time_data, failure_rate,
                       linewidth=2, color='#f39c12')
        axes[1, 0].set_title('Taxa de Falhas', fontweight='bold')
        axes[1, 0].set_xlabel('Tempo (s)')
        axes[1, 0].set_ylabel('Taxa de Falhas (%)')
        axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Estatísticas resumo (texto)
    axes[1, 1].axis('off')
    
    # Pegar valores finais
    total_requests = df_to_plot['Total Request Count'].iloc[-1] if 'Total Request Count' in df_to_plot.columns else 0
    total_failures = df_to_plot['Total Failure Count'].iloc[-1] if 'Total Failure Count' in df_to_plot.columns else 0
    success_rate = ((total_requests - total_failures) / total_requests * 100) if total_requests > 0 else 0
    
    avg_time = df_to_plot['Total Average Response Time'].mean() if 'Total Average Response Time' in df_to_plot.columns else (df_to_plot['Average Response Time'].mean() if 'Average Response Time' in df_to_plot.columns else 0)
    median_time = df_to_plot['Total Median Response Time'].mean() if 'Total Median Response Time' in df_to_plot.columns else (df_to_plot['Median Response Time'].mean() if 'Median Response Time' in df_to_plot.columns else 0)
    p95_time = df_to_plot['95%'].mean() if '95%' in df_to_plot.columns else 0
    
    tps_mean = df_to_plot['Requests/s'].mean() if 'Requests/s' in df_to_plot.columns else 0
    tps_max = df_to_plot['Requests/s'].max() if 'Requests/s' in df_to_plot.columns else 0
    
    stats_text = f'''ESTATÍSTICAS GERAIS
    
Total de Requisições: {total_requests:,}
Total de Falhas: {total_failures:,}
Taxa de Sucesso: {success_rate:.2f}%

Tempo Médio: {avg_time:.0f}ms
Tempo Mediano: {median_time:.0f}ms
P95: {p95_time:.0f}ms

TPS Médio: {tps_mean:.2f}
TPS Máximo: {tps_max:.2f}'''
    
    axes[1, 1].text(0.1, 0.5, stats_text, transform=axes[1, 1].transAxes,
                   fontsize=11, verticalalignment='center',
                   family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.suptitle('Dashboard de Performance - Teste de Carga', 
                fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    output_file = f'{output_dir}/dashboard_{timestamp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Dashboard salvo: {output_file}")


def generate_graphs_from_test(test_dir):
    """Gera gráficos para um diretório de teste específico."""
    print("="*80)
    print(f"GERANDO GRÁFICOS PARA: {test_dir}")
    print("="*80)
    
    # Procurar arquivo CSV de histórico (mais detalhado)
    history_files = glob.glob(f'{test_dir}/locust_max_tps_*_stats_history.csv')
    stats_files = glob.glob(f'{test_dir}/locust_max_tps_*_stats.csv')
    
    df_history = None
    df_stats = None
    
    if history_files:
        history_file = history_files[0]
        print(f"✓ Arquivo de histórico encontrado: {history_file}")
        df_history = load_locust_history(history_file)
        if df_history is not None:
            print(f"✓ Dados de histórico carregados: {len(df_history)} registros")
    
    if stats_files:
        stats_file = stats_files[0]
        print(f"✓ Arquivo de estatísticas encontrado: {stats_file}")
        df_stats = load_locust_stats(stats_file)
        print(f"✓ Dados de estatísticas carregados: {len(df_stats)} registros")
    
    if df_history is None and df_stats is None:
        print(f"❌ Nenhum arquivo de dados encontrado em {test_dir}")
        return
    
    # Usar histórico se disponível, senão usar stats
    df_to_use = df_history if df_history is not None else df_stats
    
    # Criar diretório para gráficos
    graphs_dir = f'{test_dir}/graphs'
    os.makedirs(graphs_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Gerar gráficos
    print("\nGerando gráficos...")
    create_tps_over_time_graph(df_to_use, graphs_dir, timestamp)
    create_response_time_graph(df_to_use, graphs_dir, timestamp)
    create_failure_rate_graph(df_to_use, graphs_dir, timestamp)
    
    create_summary_dashboard(df_stats, df_history, graphs_dir, timestamp)
    
    print("\n" + "="*80)
    print("✅ GRÁFICOS GERADOS COM SUCESSO")
    print("="*80)
    print(f"Diretório: {graphs_dir}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = "teste_1"
    
    generate_graphs_from_test(test_dir)


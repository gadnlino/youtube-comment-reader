# -*- coding: utf-8 -*-
"""
Gerar Gráficos de Qualidade Acadêmica para Relatório de Performance Multi-Vídeo

Este script cria visualizações prontas para publicação para o relatório de
avaliação de performance, incluindo distribuições de tempo de resposta e
análises comparativas.

Versão em Português Brasileiro
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import json

# Configurar estilo para publicações acadêmicas
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'

def load_data():
    """Carregar resultados de testes dos arquivos CSV e JSON."""
    csv_file = 'multi_video_results_20251026_212004.csv'
    json_file = 'multi_video_summary_20251026_212004.json'
    
    # Carregar dados CSV
    df = pd.read_csv(csv_file)
    
    # Carregar resumo JSON
    with open(json_file, 'r') as f:
        summary = json.load(f)
    
    return df, summary

def create_response_time_distribution_pt(df):
    """Criar box plot mostrando distribuição de tempo de resposta em todas as requisições."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Preparar dados por vídeo
    video_data = []
    video_labels = []
    
    for video_name in df['video_name'].unique():
        video_df = df[df['video_name'] == video_name]
        video_data.append(video_df['response_time_ms'].values)
        # Encurtar rótulos para legibilidade
        if 'Music Video' in video_name:
            video_labels.append('Vídeo Musical\n(Rick Astley)')
        elif 'Educational' in video_name:
            video_labels.append('Documentário\n(Me at the zoo)')
        else:
            video_labels.append('Música Viral\n(Gangnam Style)')
    
    # Criar box plot
    bp = ax.boxplot(video_data, labels=video_labels, patch_artist=True,
                    showmeans=True, meanline=True)
    
    # Personalizar cores
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Formatação
    ax.set_ylabel('Tempo de Resposta (ms)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Tipo de Vídeo', fontsize=12, fontweight='bold')
    ax.set_title('Distribuição de Tempo de Resposta por Tipo de Vídeo', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(bottom=0)
    
    # Adicionar legenda
    ax.legend([bp['boxes'][0], bp['medians'][0], bp['means'][0]], 
              ['IQR', 'Mediana', 'Média'],
              loc='upper right')
    
    plt.tight_layout()
    plt.savefig('boxplot_tempo_resposta_pt.png', dpi=300, bbox_inches='tight')
    print("✓ Criado: boxplot_tempo_resposta_pt.png")
    plt.close()

def create_video_specific_trends_pt(df):
    """Criar linhas de tendência individuais para cada vídeo."""
    videos = df['video_name'].unique()
    
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    
    video_labels = [
        'Vídeo Musical - Alta Popularidade (Rick Astley)',
        'Documentário - Me at the zoo',
        'Música Viral - Gangnam Style'
    ]
    
    for idx, (video_name, color, label) in enumerate(zip(videos, colors, video_labels)):
        ax = axes[idx]
        video_df = df[df['video_name'] == video_name].sort_values('request_number')
        
        # Plotar linha de tendência
        ax.plot(video_df['request_number'], video_df['response_time_ms'], 
               marker='o', color=color, linewidth=2, markersize=6, 
               label='Tempo de Resposta')
        
        # Adicionar linha de média
        mean_time = video_df['response_time_ms'].mean()
        ax.axhline(y=mean_time, color='red', linestyle='--', 
                  linewidth=1.5, alpha=0.7, label=f'Média: {mean_time:.0f}ms')
        
        # Formatação
        ax.set_ylabel('Tempo de Resposta (ms)', fontsize=11, fontweight='bold')
        ax.set_title(label, fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
        ax.set_xlim(0, 21)
        
        # Mostrar rótulo do eixo x apenas no gráfico inferior
        if idx == 2:
            ax.set_xlabel('Número da Requisição', fontsize=11, fontweight='bold')
    
    plt.suptitle('Tendências de Tempo de Resposta por Vídeo', 
                fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig('tendencias_por_video_pt.png', dpi=300, bbox_inches='tight')
    print("✓ Criado: tendencias_por_video_pt.png")
    plt.close()

def create_comparative_bar_chart_pt(summary):
    """Criar gráfico de barras comparando tempos médios de resposta."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Extrair dados
    videos = []
    avg_times = []
    std_devs = []
    
    video_labels = [
        'Vídeo Musical\n(Rick Astley)',
        'Documentário\n(Me at the zoo)',
        'Música Viral\n(Gangnam Style)'
    ]
    
    for result in summary['video_results']:
        avg_times.append(result['avg_response_time'])
        std_devs.append(result['std_dev'])
    
    # Criar gráfico de barras
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    bars = ax.bar(range(len(video_labels)), avg_times, color=colors, alpha=0.7,
                  edgecolor='black', linewidth=1.5, yerr=std_devs, capsize=10)
    
    # Adicionar rótulos de valor nas barras
    for i, (bar, avg) in enumerate(zip(bars, avg_times)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{avg:.0f}ms', ha='center', va='bottom', 
               fontsize=11, fontweight='bold')
    
    # Adicionar linha de limite
    ax.axhline(y=500, color='orange', linestyle='--', alpha=0.5,
              linewidth=2, label='Limite Bom (500ms)')
    
    # Formatação
    ax.set_ylabel('Tempo Médio de Resposta (ms)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Vídeo', fontsize=12, fontweight='bold')
    ax.set_title('Comparação de Tempo Médio de Resposta com Desvio Padrão', 
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(range(len(video_labels)))
    ax.set_xticklabels(video_labels, rotation=15, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend()
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    plt.savefig('comparacao_tempo_medio_resposta_pt.png', dpi=300, 
                bbox_inches='tight')
    print("✓ Criado: comparacao_tempo_medio_resposta_pt.png")
    plt.close()

def main():
    """Função principal para gerar todos os gráficos em português."""
    print("="*80)
    print("GERADOR DE GRÁFICOS ACADÊMICOS - VERSÃO PORTUGUÊS")
    print("="*80)
    print("\nCarregando dados...")
    
    try:
        df, summary = load_data()
        print(f"✓ Dados carregados: {len(df)} requisições de {len(summary['video_results'])} vídeos")
        
        print("\nGerando gráficos em português...")
        print("-"*80)
        
        # Gerar apenas os gráficos essenciais (sem CDF)
        create_response_time_distribution_pt(df)
        create_video_specific_trends_pt(df)
        create_comparative_bar_chart_pt(summary)
        
        print("-"*80)
        print("\n✅ Todos os gráficos em português foram gerados com sucesso!")
        print("\nArquivos criados:")
        print("  1. boxplot_tempo_resposta_pt.png")
        print("  2. tendencias_por_video_pt.png")
        print("  3. comparacao_tempo_medio_resposta_pt.png")
        print("\n💡 Estes gráficos estão prontos para inserção no documento da monografia")
        print("="*80)
        
    except FileNotFoundError as e:
        print(f"\n❌ Erro: Arquivo não encontrado - {e}")
        print("Certifique-se de que os arquivos de resultados estão no diretório correto:")
        print("  - multi_video_results_20251026_212004.csv")
        print("  - multi_video_summary_20251026_212004.json")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()


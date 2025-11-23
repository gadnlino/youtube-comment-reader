#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gerar Visualizações Acadêmicas para Análise Multilíngue de Sentimento
(Versão em Português Brasileiro)

Cria gráficos de qualidade profissional mostrando impacto do idioma na 
classificação de sentimento para inclusão em monografia/tese acadêmica.

Autor: AI Assistant
Data: 2 de Novembro de 2025
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime

# Configurar estilo profissional
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")

# Configurar fonte para suportar caracteres especiais em português
plt.rcParams['font.family'] = 'DejaVu Sans'

def load_results(filename):
    """Carregar resultados do arquivo JSON."""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_language_comparison_bar_chart(data, timestamp):
    """
    Gerar gráfico de barras comparando NEUTRAL% entre idiomas.
    """
    # Organizar dados por idioma
    languages = {
        'Inglês': [],
        'Espanhol': [],
        'Português': [],
        'Coreano/Multi': []
    }
    
    for result in data['results']:
        if not result.get('success', False):
            continue
        
        lang = result['language']
        neutral_pct = result['sentiment_distribution']['NEUTRAL']['percentage']
        
        if lang == 'English':
            languages['Inglês'].append(neutral_pct)
        elif 'Spanish' in lang:
            languages['Espanhol'].append(neutral_pct)
        elif 'Portuguese' in lang:
            languages['Português'].append(neutral_pct)
        elif 'Korean' in lang or 'Multilingual' in lang:
            languages['Coreano/Multi'].append(neutral_pct)
    
    # Calcular médias
    lang_names = []
    avg_neutrals = []
    std_neutrals = []
    colors = []
    
    for lang, values in languages.items():
        if values:
            lang_names.append(lang)
            avg_neutrals.append(np.mean(values))
            std_neutrals.append(np.std(values) if len(values) > 1 else 0)
            colors.append('#3498db' if lang == 'Inglês' else '#e74c3c')
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(lang_names))
    bars = ax.bar(x, avg_neutrals, yerr=std_neutrals, capsize=5,
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
    
    # Personalizar
    ax.set_ylabel('Classificação NEUTRAL Média (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Idioma', fontsize=12, fontweight='bold')
    ax.set_title('Impacto do Idioma na Classificação de Sentimento\nViés da Classe NEUTRAL Entre Idiomas',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(lang_names, fontsize=11)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adicionar rótulos de valor nas barras
    for i, (bar, val, std) in enumerate(zip(bars, avg_neutrals, std_neutrals)):
        height = bar.get_height()
        label = f'{val:.1f}%'
        if std > 0:
            label += f'\n(σ={std:.1f})'
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
               label, ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Adicionar linha de referência baseline
    english_avg = avg_neutrals[0] if lang_names[0] == 'Inglês' else None
    if english_avg:
        ax.axhline(y=english_avg, color='blue', linestyle='--', alpha=0.5,
                  label=f'Baseline Inglês ({english_avg:.1f}%)')
        ax.legend(loc='upper right', fontsize=10)
    
    plt.tight_layout()
    import os
    os.makedirs('graphs', exist_ok=True)
    filename = f'graphs/comparacao_viés_neutral_idiomas_pt_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Gerado: {filename}")
    plt.close()

def generate_individual_video_chart(data, timestamp):
    """
    Gerar gráfico mostrando NEUTRAL% para cada vídeo individual.
    """
    videos = []
    neutrals = []
    colors = []
    languages = []
    
    for result in data['results']:
        if not result.get('success', False):
            continue
        
        video_name = result['video_name'][:30]  # Truncar nomes longos
        neutral_pct = result['sentiment_distribution']['NEUTRAL']['percentage']
        lang = result['language']
        
        # Traduzir idiomas
        lang_pt = lang.replace('English', 'Inglês').replace('Spanish', 'Espanhol')\
                     .replace('Portuguese', 'Português').replace('Korean', 'Coreano')\
                     .replace('Multilingual', 'Multilíngue')
        
        videos.append(video_name)
        neutrals.append(neutral_pct)
        languages.append(lang_pt)
        
        # Cor por idioma
        if 'Inglês' in lang_pt:
            colors.append('#3498db')
        elif 'Espanhol' in lang_pt:
            colors.append('#e67e22')
        elif 'Português' in lang_pt:
            colors.append('#9b59b6')
        else:
            colors.append('#e74c3c')
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(12, 8))
    
    y_pos = np.arange(len(videos))
    bars = ax.barh(y_pos, neutrals, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    
    # Personalizar
    ax.set_yticks(y_pos)
    ax.set_yticklabels(videos, fontsize=9)
    ax.set_xlabel('Classificação NEUTRAL (%)', fontsize=12, fontweight='bold')
    ax.set_title('Classificação de Sentimento por Vídeo\nPercentual NEUTRAL em Conteúdos de Diferentes Idiomas',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 100)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Adicionar rótulos de valor
    for i, (bar, val, lang) in enumerate(zip(bars, neutrals, languages)):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2,
               f'{val:.0f}% ({lang})', va='center', fontsize=8)
    
    # Adicionar legenda
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#3498db', label='Inglês'),
        Patch(facecolor='#e67e22', label='Espanhol'),
        Patch(facecolor='#9b59b6', label='Português'),
        Patch(facecolor='#e74c3c', label='Coreano/Multi')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    filename = f'graphs/taxa_neutral_videos_individuais_pt_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Gerado: {filename}")
    plt.close()

def generate_sentiment_distribution_heatmap(data, timestamp):
    """
    Gerar heatmap mostrando distribuição completa de sentimentos.
    """
    videos = []
    positives = []
    negatives = []
    neutrals = []
    
    for result in data['results']:
        if not result.get('success', False):
            continue
        
        video_name = result['video_name'][:25]
        lang = result['language']
        # Traduzir idioma
        lang_pt = lang.replace('English', 'Inglês').replace('Spanish', 'Espanhol')\
                     .replace('Portuguese', 'Português').replace('Korean', 'Coreano')\
                     .replace('Multilingual', 'Multilíngue')
        video_label = f"{video_name}\n({lang_pt})"
        
        videos.append(video_label)
        positives.append(result['sentiment_distribution']['POSITIVE']['percentage'])
        negatives.append(result['sentiment_distribution']['NEGATIVE']['percentage'])
        neutrals.append(result['sentiment_distribution']['NEUTRAL']['percentage'])
    
    # Criar matriz para heatmap
    data_matrix = np.array([positives, negatives, neutrals])
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(14, 6))
    
    im = ax.imshow(data_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
    
    # Definir ticks e labels
    ax.set_xticks(np.arange(len(videos)))
    ax.set_yticks(np.arange(3))
    ax.set_xticklabels(videos, rotation=45, ha='right', fontsize=8)
    ax.set_yticklabels(['POSITIVO', 'NEGATIVO', 'NEUTRO'], fontsize=11, fontweight='bold')
    
    # Adicionar colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Porcentagem (%)', rotation=270, labelpad=20, fontsize=11, fontweight='bold')
    
    # Adicionar anotações de texto
    for i in range(3):
        for j in range(len(videos)):
            text = ax.text(j, i, f'{data_matrix[i, j]:.0f}%',
                          ha="center", va="center", color="black", fontsize=8, fontweight='bold')
    
    ax.set_title('Mapa de Calor da Distribuição de Sentimentos\nDistribuição Completa por Idioma do Vídeo',
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    filename = f'graphs/heatmap_distribuicao_sentimentos_pt_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Gerado: {filename}")
    plt.close()

def generate_language_bias_statistical_plot(data, timestamp):
    """
    Gerar box plot mostrando distribuição de NEUTRAL% por idioma.
    """
    # Organizar dados por idioma
    language_data = {
        'Inglês': [],
        'Espanhol': [],
        'Português': [],
        'Coreano/Multi': []
    }
    
    for result in data['results']:
        if not result.get('success', False):
            continue
        
        lang = result['language']
        neutral_pct = result['sentiment_distribution']['NEUTRAL']['percentage']
        
        if lang == 'English':
            language_data['Inglês'].append(neutral_pct)
        elif 'Spanish' in lang:
            language_data['Espanhol'].append(neutral_pct)
        elif 'Portuguese' in lang:
            language_data['Português'].append(neutral_pct)
        elif 'Korean' in lang or 'Multilingual' in lang:
            language_data['Coreano/Multi'].append(neutral_pct)
    
    # Filtrar categorias vazias
    languages = []
    data_for_plot = []
    for lang, values in language_data.items():
        if values:
            languages.append(lang)
            data_for_plot.append(values)
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Criar box plot tradicional (SEM notch)
    bp = ax.boxplot(data_for_plot, labels=languages, patch_artist=True,
                    showmeans=True, widths=0.5,
                    boxprops=dict(facecolor='lightblue', alpha=0.7, linewidth=1.5),
                    medianprops=dict(color='red', linewidth=2.5),
                    meanprops=dict(marker='D', markerfacecolor='green', 
                                 markeredgecolor='darkgreen', markersize=10, linewidth=1.5),
                    whiskerprops=dict(linewidth=1.5),
                    capprops=dict(linewidth=1.5))
    
    # Personalizar cores
    colors = ['#3498db', '#e67e22', '#9b59b6', '#e74c3c']
    for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
        patch.set_edgecolor('black')
    
    # Sobrepor pontos individuais
    for i, (lang_data, x_pos) in enumerate(zip(data_for_plot, range(1, len(data_for_plot) + 1))):
        y = lang_data
        # Jitter horizontal para visualização melhor
        x = np.random.normal(x_pos, 0.04, size=len(y))
        ax.scatter(x, y, alpha=0.7, s=80, color='gray', edgecolors='black', linewidths=1)
    
    # Personalizar
    ax.set_ylabel('Classificação NEUTRAL (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Idioma', fontsize=12, fontweight='bold')
    ax.set_title('Distribuição Estatística da Classificação NEUTRAL por Idioma\n' +
                 'Box Plot com Pontos de Dados Individuais',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(40, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adicionar legenda
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='red', linewidth=2, label='Mediana'),
        Line2D([0], [0], marker='D', color='w', markerfacecolor='green', 
               markeredgecolor='darkgreen', markersize=8, label='Média'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=8, 
               alpha=0.7, markeredgecolor='black', label='Vídeos Individuais')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, framealpha=0.9)
    
    plt.tight_layout()
    filename = f'graphs/boxplot_viés_linguistico_pt_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Gerado: {filename}")
    plt.close()

def generate_stacked_bar_comparison(data, timestamp):
    """
    Gerar gráfico de barras empilhadas mostrando distribuição completa.
    """
    # Preparar dados
    video_labels = []
    languages_list = []
    positive_pcts = []
    negative_pcts = []
    neutral_pcts = []
    
    for result in data['results']:
        if not result.get('success', False):
            continue
        
        # Traduzir idioma
        lang = result['language']
        lang_pt = lang.replace('English', 'Inglês').replace('Spanish', 'Espanhol')\
                     .replace('Portuguese', 'Português').replace('Korean', 'Coreano')\
                     .replace('Multilingual', 'Multilíngue')
        lang_short = lang_pt.split('/')[0]  # Pegar primeiro idioma
        label = f"{result['video_name'][:20]}\n({lang_short})"
        video_labels.append(label)
        languages_list.append(lang_pt)
        
        dist = result['sentiment_distribution']
        positive_pcts.append(dist['POSITIVE']['percentage'])
        negative_pcts.append(dist['NEGATIVE']['percentage'])
        neutral_pcts.append(dist['NEUTRAL']['percentage'])
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(len(video_labels))
    width = 0.7
    
    # Barras empilhadas
    p1 = ax.bar(x, positive_pcts, width, label='Positivo', color='#27ae60')
    p2 = ax.bar(x, negative_pcts, width, bottom=positive_pcts, 
                label='Negativo', color='#e74c3c')
    p3 = ax.bar(x, neutral_pcts, width,
                bottom=np.array(positive_pcts) + np.array(negative_pcts),
                label='Neutro', color='#95a5a6')
    
    # Personalizar
    ax.set_ylabel('Porcentagem de Comentários (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Vídeo (Idioma Principal)', fontsize=12, fontweight='bold')
    ax.set_title('Distribuição de Sentimentos por Idioma do Vídeo\n' +
                 'Teste do Modelo TF-IDF em Múltiplos Idiomas (100 comentários cada)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(video_labels, fontsize=8, rotation=45, ha='right')
    ax.legend(loc='upper right', fontsize=11)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adicionar rótulos de porcentagem
    for i, (pos, neg, neu) in enumerate(zip(positive_pcts, negative_pcts, neutral_pcts)):
        if pos > 8:
            ax.text(i, pos/2, f'{pos:.0f}%', ha='center', va='center',
                   fontweight='bold', color='white', fontsize=9)
        if neg > 8:
            ax.text(i, pos + neg/2, f'{neg:.0f}%', ha='center', va='center',
                   fontweight='bold', color='white', fontsize=9)
        if neu > 8:
            ax.text(i, pos + neg + neu/2, f'{neu:.0f}%', ha='center', va='center',
                   fontweight='bold', color='white', fontsize=9)
    
    plt.tight_layout()
    filename = f'graphs/comparacao_sentimentos_multilíngue_pt_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Gerado: {filename}")
    plt.close()

def main():
    print("=" * 80)
    print("GERANDO VISUALIZAÇÕES ACADÊMICAS - VERSÃO PORTUGUÊS BRASILEIRO")
    print("=" * 80)
    
    # Carregar resultados mais recentes - tenta results/, depois api_load_testing, depois local
    import glob
    result_files = sorted(glob.glob('results/multilingual_sentiment_results_*.json'))
    if not result_files:
        result_files = sorted(glob.glob('../api_load_testing/multilingual_sentiment_results_*.json'))
    if not result_files:
        result_files = sorted(glob.glob('multilingual_sentiment_results_*.json'))
    if not result_files:
        print("❌ Nenhum arquivo de resultados encontrado!")
        return
    
    latest_file = result_files[-1]
    print(f"\n📊 Carregando dados de: {latest_file}")
    
    data = load_results(latest_file)
    timestamp = data['timestamp']
    
    print(f"✓ Carregados {len(data['results'])} resultados de vídeos")
    print(f"✓ Testes bem-sucedidos: {data['successful_tests']}")
    print(f"✓ Testes falhados: {data['failed_tests']}\n")
    
    print("Gerando visualizações em português...\n")
    
    # Gerar todos os gráficos
    generate_language_comparison_bar_chart(data, timestamp)
    generate_individual_video_chart(data, timestamp)
    generate_sentiment_distribution_heatmap(data, timestamp)
    generate_language_bias_statistical_plot(data, timestamp)
    generate_stacked_bar_comparison(data, timestamp)
    
    print("\n" + "=" * 80)
    print("✅ TODAS AS VISUALIZAÇÕES GERADAS COM SUCESSO!")
    print("=" * 80)
    print("\nArquivos gerados:")
    print(f"  1. comparacao_viés_neutral_idiomas_pt_{timestamp}.png")
    print(f"  2. taxa_neutral_videos_individuais_pt_{timestamp}.png")
    print(f"  3. heatmap_distribuicao_sentimentos_pt_{timestamp}.png")
    print(f"  4. boxplot_viés_linguistico_pt_{timestamp}.png")
    print(f"  5. comparacao_sentimentos_multilíngue_pt_{timestamp}.png")
    print("\n📝 Prontos para inclusão na monografia em português")

if __name__ == "__main__":
    main()


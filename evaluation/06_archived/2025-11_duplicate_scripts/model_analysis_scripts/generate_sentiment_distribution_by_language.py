#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera gráfico de distribuição de sentimento (POSITIVE, NEGATIVE, NEUTRAL) por idioma

Este script cria um gráfico mostrando como o modelo categoriza comentários
em diferentes idiomas, demonstrando que funciona melhor com inglês e tem
dificuldades com português, espanhol e outras línguas.
"""

import json
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

# Configuração de estilo
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'sans-serif'

def normalize_language(lang):
    """Normaliza nomes de idiomas para agrupamento."""
    lang = str(lang).strip()
    if 'English' in lang and 'Spanish' not in lang and 'Korean' not in lang:
        return 'Inglês'
    elif 'Spanish' in lang:
        return 'Espanhol'
    elif 'Portuguese' in lang:
        return 'Português'
    elif 'Korean' in lang:
        return 'Coreano/Outros'
    else:
        return 'Outros'

def load_latest_results():
    """Carrega o arquivo de resultados mais recente."""
    # Tenta results/, depois api_load_testing, depois local
    json_files = sorted(glob.glob('results/multilingual_sentiment_results_*.json'))
    if not json_files:
        json_files = sorted(glob.glob('../api_load_testing/multilingual_sentiment_results_*.json'))
    if not json_files:
        json_files = sorted(glob.glob('multilingual_sentiment_results_*.json'))
    
    if not json_files:
        raise FileNotFoundError("Nenhum arquivo de resultados multilíngue encontrado")
    
    latest_file = json_files[-1]
    print(f"Carregando: {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data, latest_file

def aggregate_by_language(data):
    """Agrega distribuições por idioma."""
    if 'results' in data:
        results = data['results']
    else:
        results = data if isinstance(data, list) else [data]
    
    language_stats = defaultdict(lambda: {
        'POSITIVE': [],
        'NEGATIVE': [],
        'NEUTRAL': [],
        'videos': []
    })
    
    for result in results:
        if not result.get('success', False):
            continue
        
        lang = normalize_language(result.get('language', 'Unknown'))
        dist = result.get('sentiment_distribution', {})
        
        language_stats[lang]['POSITIVE'].append(dist.get('POSITIVE', {}).get('percentage', 0))
        language_stats[lang]['NEGATIVE'].append(dist.get('NEGATIVE', {}).get('percentage', 0))
        language_stats[lang]['NEUTRAL'].append(dist.get('NEUTRAL', {}).get('percentage', 0))
        language_stats[lang]['videos'].append(result.get('video_name', 'Unknown'))
    
    # Calcular médias por idioma
    aggregated = {}
    for lang, stats in language_stats.items():
        aggregated[lang] = {
            'POSITIVE': np.mean(stats['POSITIVE']),
            'NEGATIVE': np.mean(stats['NEGATIVE']),
            'NEUTRAL': np.mean(stats['NEUTRAL']),
            'n_videos': len(stats['videos']),
            'std_POSITIVE': np.std(stats['POSITIVE']),
            'std_NEGATIVE': np.std(stats['NEGATIVE']),
            'std_NEUTRAL': np.std(stats['NEUTRAL'])
        }
    
    return aggregated

def generate_distribution_chart(aggregated_data, timestamp):
    """Gera gráfico de barras agrupadas mostrando distribuição por idioma."""
    # Ordenar idiomas: Inglês primeiro, depois outros
    language_order = ['Inglês', 'Espanhol', 'Português', 'Coreano/Outros', 'Outros']
    languages = [lang for lang in language_order if lang in aggregated_data]
    languages.extend([lang for lang in aggregated_data.keys() if lang not in language_order])
    
    if not languages:
        print("❌ Nenhum dado válido encontrado")
        return
    
    # Preparar dados para o gráfico
    positive_means = [aggregated_data[lang]['POSITIVE'] for lang in languages]
    negative_means = [aggregated_data[lang]['NEGATIVE'] for lang in languages]
    neutral_means = [aggregated_data[lang]['NEUTRAL'] for lang in languages]
    
    positive_stds = [aggregated_data[lang]['std_POSITIVE'] for lang in languages]
    negative_stds = [aggregated_data[lang]['std_NEGATIVE'] for lang in languages]
    neutral_stds = [aggregated_data[lang]['std_NEUTRAL'] for lang in languages]
    
    n_videos = [aggregated_data[lang]['n_videos'] for lang in languages]
    
    # Criar gráfico
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(len(languages))
    width = 0.25
    
    # Cores
    colors = {
        'POSITIVE': '#4CAF50',  # Verde
        'NEGATIVE': '#F44336',  # Vermelho
        'NEUTRAL': '#FF9800'    # Laranja
    }
    
    # Barras
    bars1 = ax.bar(x - width, positive_means, width, label='POSITIVO',
                   yerr=positive_stds, capsize=5, color=colors['POSITIVE'],
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    bars2 = ax.bar(x, negative_means, width, label='NEGATIVO',
                   yerr=negative_stds, capsize=5, color=colors['NEGATIVE'],
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    bars3 = ax.bar(x + width, neutral_means, width, label='NEUTRO',
                   yerr=neutral_stds, capsize=5, color=colors['NEUTRAL'],
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Adicionar valores nas barras
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 2:  # Só mostra se for > 2% para não poluir
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}%', ha='center', va='bottom',
                       fontsize=9, fontweight='bold')
    
    # Adicionar número de vídeos abaixo de cada idioma
    for i, (lang, n) in enumerate(zip(languages, n_videos)):
        ax.text(i, -5, f'(n={n})', ha='center', va='top',
               fontsize=9, style='italic', color='gray')
    
    # Formatação
    ax.set_xlabel('Idioma', fontsize=13, fontweight='bold')
    ax.set_ylabel('Percentual de Comentários (%)', fontsize=13, fontweight='bold')
    ax.set_title('Distribuição de Sentimento por Idioma\n(Comparação: Inglês vs Outras Línguas)',
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(languages, fontsize=11)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(bottom=-8, top=100)
    
    plt.tight_layout()
    
    # Salvar
    os.makedirs('graphs', exist_ok=True)
    output_file = f'graphs/distribuicao_sentimento_por_idioma_{timestamp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Gráfico salvo: {output_file}")
    plt.close()
    
    return output_file

def main():
    print("="*80)
    print("GERAÇÃO DE GRÁFICO: DISTRIBUIÇÃO DE SENTIMENTO POR IDIOMA")
    print("="*80)
    print()
    
    try:
        # Carregar dados
        data, source_file = load_latest_results()
        print(f"✓ Dados carregados de: {source_file}")
        print()
        
        # Agregar por idioma
        aggregated = aggregate_by_language(data)
        
        print("Estatísticas por idioma:")
        print("-" * 80)
        for lang, stats in sorted(aggregated.items()):
            print(f"\n{lang} ({stats['n_videos']} vídeos):")
            print(f"  POSITIVO: {stats['POSITIVE']:.2f}% ± {stats['std_POSITIVE']:.2f}%")
            print(f"  NEGATIVO: {stats['NEGATIVE']:.2f}% ± {stats['std_NEGATIVE']:.2f}%")
            print(f"  NEUTRO:   {stats['NEUTRAL']:.2f}% ± {stats['std_NEUTRAL']:.2f}%")
        print()
        
        # Gerar gráfico
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = generate_distribution_chart(aggregated, timestamp)
        
        print()
        print("="*80)
        print("✅ GRÁFICO GERADO COM SUCESSO")
        print("="*80)
        print(f"Arquivo: {output_file}")
        print()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


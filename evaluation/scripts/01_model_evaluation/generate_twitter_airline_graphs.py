#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geração de Gráficos para Validação com Twitter US Airline Sentiment

Este script gera visualizações acadêmicas dos resultados da validação
do modelo com o dataset Twitter US Airline Sentiment.
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import glob
from datetime import datetime

# Configuração de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

def load_results(results_file):
    """Carrega resultados do arquivo JSON."""
    with open(results_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_confusion_matrix_heatmap(results, timestamp):
    """Gera heatmap da matriz de confusão."""
    print("📊 Gerando matriz de confusão...")
    
    cm = np.array(results['confusion_matrix'])
    labels = results['confusion_matrix_labels']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Criar heatmap
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels,
                cbar_kws={'label': 'Quantidade de Tweets'},
                linewidths=0.5, linecolor='gray', ax=ax)
    
    ax.set_xlabel('Predito', fontsize=13, fontweight='bold')
    ax.set_ylabel('Real (Ground Truth)', fontsize=13, fontweight='bold')
    ax.set_title('Matriz de Confusão - Validação com Twitter US Airline Sentiment', 
                 fontsize=15, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    os.makedirs('graphs', exist_ok=True)
    filename = f'graphs/confusion_matrix_twitter_airline_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gerado: {filename}")

def generate_metrics_comparison_bar(results, timestamp):
    """Gera gráfico de barras comparando métricas."""
    print("📊 Gerando gráfico de métricas...")
    
    metrics = results['metrics']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    metric_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    metric_values = [
        metrics['accuracy'] * 100,
        metrics['precision'] * 100,
        metrics['recall'] * 100,
        metrics['f1_score'] * 100
    ]
    
    colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0']
    bars = ax.bar(metric_names, metric_values, color=colors, 
                  edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Adicionar valores nas barras
    for bar, value in zip(bars, metric_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{value:.2f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    ax.set_ylabel('Percentual (%)', fontsize=13, fontweight='bold')
    ax.set_title('Métricas de Desempenho - Validação com Twitter US Airline Sentiment',
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_ylim(0, max(metric_values) * 1.15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    os.makedirs('graphs', exist_ok=True)
    filename = f'graphs/metrics_twitter_airline_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gerado: {filename}")

def generate_per_class_metrics(results, timestamp):
    """Gera gráfico de métricas por classe."""
    print("📊 Gerando gráfico de métricas por classe...")
    
    # Calcular métricas por classe da matriz de confusão
    cm = np.array(results['confusion_matrix'])
    labels = results['confusion_matrix_labels']
    
    precision_per_class = []
    recall_per_class = []
    f1_per_class = []
    
    for i, label in enumerate(labels):
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        precision_per_class.append(precision * 100)
        recall_per_class.append(recall * 100)
        f1_per_class.append(f1 * 100)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(len(labels))
    width = 0.25
    
    bars1 = ax.bar(x - width, precision_per_class, width, label='Precision',
                   color='#4CAF50', edgecolor='black', linewidth=1.5, alpha=0.8)
    bars2 = ax.bar(x, recall_per_class, width, label='Recall',
                   color='#2196F3', edgecolor='black', linewidth=1.5, alpha=0.8)
    bars3 = ax.bar(x + width, f1_per_class, width, label='F1-Score',
                   color='#FF9800', edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Adicionar valores nas barras
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax.set_xlabel('Classe de Sentimento', fontsize=13, fontweight='bold')
    ax.set_ylabel('Percentual (%)', fontsize=13, fontweight='bold')
    ax.set_title('Métricas por Classe - Validação com Twitter US Airline Sentiment',
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    os.makedirs('graphs', exist_ok=True)
    filename = f'graphs/per_class_metrics_twitter_airline_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gerado: {filename}")

def generate_confusion_matrix_normalized(results, timestamp):
    """Gera matriz de confusão normalizada (percentuais)."""
    print("📊 Gerando matriz de confusão normalizada...")
    
    cm = np.array(results['confusion_matrix'])
    labels = results['confusion_matrix_labels']
    
    # Normalizar por linha (percentual de cada classe real)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(cm_normalized, annot=True, fmt='.1f', cmap='YlOrRd',
                xticklabels=labels, yticklabels=labels,
                cbar_kws={'label': 'Percentual (%)'},
                linewidths=0.5, linecolor='gray', ax=ax,
                vmin=0, vmax=100)
    
    ax.set_xlabel('Predito', fontsize=13, fontweight='bold')
    ax.set_ylabel('Real (Ground Truth)', fontsize=13, fontweight='bold')
    ax.set_title('Matriz de Confusão Normalizada (%) - Twitter US Airline Sentiment',
                 fontsize=15, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    os.makedirs('graphs', exist_ok=True)
    filename = f'graphs/confusion_matrix_normalized_twitter_airline_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Gerado: {filename}")

def main():
    """Função principal."""
    print("="*80)
    print("GERAÇÃO DE GRÁFICOS - VALIDAÇÃO TWITTER US AIRLINE SENTIMENT")
    print("="*80)
    print()
    
    # Encontrar arquivo de resultados mais recente
    result_files = sorted(glob.glob('results/validation_twitter_airline_*.json'))
    if not result_files:
        print("❌ Nenhum arquivo de resultados encontrado!")
        print("   Execute primeiro o script validate_with_twitter_airline.py")
        return
    
    latest_file = result_files[-1]
    print(f"📊 Carregando resultados de: {latest_file}")
    
    results = load_results(latest_file)
    timestamp = results['timestamp']
    
    print(f"✅ Dataset: {results['dataset']}")
    print(f"✅ Total de amostras: {results['total_samples']:,}")
    print(f"✅ Accuracy: {results['metrics']['accuracy']*100:.2f}%")
    print()
    
    print("Gerando visualizações...\n")
    
    # Gerar todos os gráficos
    generate_confusion_matrix_heatmap(results, timestamp)
    generate_metrics_comparison_bar(results, timestamp)
    generate_per_class_metrics(results, timestamp)
    generate_confusion_matrix_normalized(results, timestamp)
    
    print()
    print("="*80)
    print("✅ TODOS OS GRÁFICOS GERADOS COM SUCESSO!")
    print("="*80)
    print()
    print("Arquivos gerados:")
    print(f"  1. graphs/confusion_matrix_twitter_airline_{timestamp}.png")
    print(f"  2. graphs/metrics_twitter_airline_{timestamp}.png")
    print(f"  3. graphs/per_class_metrics_twitter_airline_{timestamp}.png")
    print(f"  4. graphs/confusion_matrix_normalized_twitter_airline_{timestamp}.png")
    print()
    print("📝 Prontos para inclusão na monografia")

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geração de Gráficos para Validação Independente

Este script gera gráficos acadêmicos a partir dos resultados de validação
independente obtidos com diferentes datasets.

Suporta:
- Twitter US Airline Sentiment
- Tweets em Português (Hugging Face)
- IMDB Movie Reviews
- Outros datasets de validação
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import glob
from sklearn.metrics import classification_report
import pandas as pd

# Configuração para gráficos acadêmicos
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
sns.set_style("whitegrid")

def load_latest_results(dataset_name=None):
    """
    Carrega o arquivo de resultados mais recente.
    
    Args:
        dataset_name: Nome do dataset (opcional). Se None, carrega o mais recente.
    """
    results_dir = 'results'
    
    if dataset_name:
        pattern = os.path.join(results_dir, f'validation_{dataset_name}_*.json')
    else:
        pattern = os.path.join(results_dir, 'validation_*.json')
    
    list_of_files = glob.glob(pattern)
    if not list_of_files:
        raise FileNotFoundError(f"Nenhum arquivo de resultado encontrado em {results_dir}")
    
    latest_file = max(list_of_files, key=os.path.getctime)
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Carregando resultados de: {latest_file}")
    return data, latest_file

def create_graphs_directory():
    """Cria o diretório de gráficos se não existir."""
    graphs_dir = 'graphs'
    os.makedirs(graphs_dir, exist_ok=True)
    return graphs_dir

def plot_confusion_matrix(cm, labels, filename, title="Matriz de Confusão", dataset_name=""):
    """Plota matriz de confusão."""
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels, 
                cbar=False, linewidths=0.5)
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Predito', fontsize=12, fontweight='bold')
    plt.ylabel('Real', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gerado: {filename}")

def plot_normalized_confusion_matrix(cm, labels, filename, title="Matriz de Confusão Normalizada", dataset_name=""):
    """Plota matriz de confusão normalizada."""
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    cm_normalized = np.nan_to_num(cm_normalized)  # Tratar divisão por zero
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Blues',
                xticklabels=labels, yticklabels=labels,
                cbar=False, linewidths=0.5)
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Predito', fontsize=12, fontweight='bold')
    plt.ylabel('Real', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gerado: {filename}")

def plot_general_metrics(metrics, filename, title="Métricas Gerais de Classificação", dataset_name=""):
    """Plota métricas gerais."""
    labels = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    values = [metrics['accuracy'], metrics['precision'], 
              metrics['recall'], metrics['f1_score']]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'], 
                   edgecolor='black', linewidth=1.5)
    
    # Adicionar valores nas barras
    for bar, value in zip(bars, values):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{value:.3f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.ylim(0, 1.0)
    plt.ylabel('Valor da Métrica', fontsize=12, fontweight='bold')
    plt.title(title, fontsize=16, fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gerado: {filename}")

def calculate_per_class_metrics_from_cm(cm, labels):
    """
    Calcula métricas por classe a partir da matriz de confusão.
    Retorna um dicionário no formato esperado pelo plot_per_class_metrics.
    """
    per_class_metrics = {}
    total_samples = cm.sum()
    
    for i, label in enumerate(labels):
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp
        tn = total_samples - tp - fp - fn
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        # Accuracy por classe: (TP + TN) / Total
        accuracy = (tp + tn) / total_samples if total_samples > 0 else 0
        support = tp + fn
        
        per_class_metrics[label] = {
            'precision': precision,
            'recall': recall,
            'f1-score': f1,
            'accuracy': accuracy,
            'support': support
        }
    
    return per_class_metrics

def plot_per_class_metrics(per_class_metrics, labels, filename, title="Métricas por Classe", dataset_name=""):
    """Plota métricas por classe incluindo Precision, Recall, F1-Score e Accuracy."""
    # Preparar dados - incluir todas as classes, mesmo as que não existem no ground truth
    # (porque o modelo pode prever essas classes)
    metrics_data = []
    classes_without_gt = []
    
    for label in labels:
        if label in per_class_metrics:
            support = per_class_metrics[label].get('support', 0)
            # Se support = 0, a classe não existe no ground truth, mas ainda mostramos
            # porque o modelo pode ter feito predições para essa classe
            if support == 0:
                classes_without_gt.append(label)
            
            metrics_data.append({
                'Classe': label,
                'Precision': per_class_metrics[label]['precision'],
                'Recall': per_class_metrics[label]['recall'],
                'F1-Score': per_class_metrics[label]['f1-score'],
                'Accuracy': per_class_metrics[label]['accuracy']
            })
    
    if not metrics_data:
        print(f"⚠️  Não foi possível gerar gráfico de métricas por classe")
        return
    
    df = pd.DataFrame(metrics_data)
    df = df.set_index('Classe')
    
    # Plotar todas as 4 métricas
    metrics_to_plot = ['Precision', 'Recall', 'F1-Score', 'Accuracy']
    df[metrics_to_plot].plot(kind='bar', figsize=(14, 7), 
                             colormap='Paired', 
                             edgecolor='black', linewidth=1.5,
                             width=0.8)
    
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Classe', fontsize=12, fontweight='bold')
    plt.ylabel('Valor da Métrica', fontsize=12, fontweight='bold')
    plt.ylim(0, 1.0)
    plt.xticks(rotation=45, ha='right')
    plt.legend(['Precision', 'Recall', 'F1-Score', 'Accuracy'], 
               title='Métricas de Desempenho', fontsize=10, loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adicionar nota se houver classes sem ground truth
    if classes_without_gt:
        note_text = f"Nota: Classes {', '.join(classes_without_gt)} não existem no ground truth do dataset (métricas zeradas), mas o modelo pode fazer predições para essas classes"
        plt.figtext(0.5, 0.01, note_text, ha='center', fontsize=9, style='italic', color='gray', wrap=True)
    
    # Adicionar valores nas barras
    for i, (idx, row) in enumerate(df.iterrows()):
        for j, metric in enumerate(metrics_to_plot):
            value = row[metric]
            if not np.isnan(value) and value >= 0:
                # Posicionar texto acima da barra
                offset = (j - 1.5) * 0.2  # Ajustar posição horizontal
                plt.text(i + offset, value + 0.02,
                        f'{value:.2f}', ha='center', va='bottom',
                        fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Gerado: {filename}")

def main():
    """Função principal."""
    import sys
    
    print("="*80)
    print("GERAÇÃO DE GRÁFICOS - VALIDAÇÃO INDEPENDENTE")
    print("="*80)
    
    # Permitir especificar dataset via argumento
    dataset_name = None
    if len(sys.argv) > 1:
        dataset_name = sys.argv[1]
        print(f"📌 Dataset especificado: {dataset_name}")
    
    try:
        results_data, results_file = load_latest_results(dataset_name)
    except FileNotFoundError as e:
        print(f"❌ Erro: {e}")
        print("\n💡 Dica: Execute o script de validação primeiro para gerar os resultados.")
        return
    
    # Suportar diferentes formatos de JSON
    if 'metrics' in results_data:
        # Formato novo (com metrics aninhado)
        metrics = results_data['metrics']
        cm = np.array(metrics['confusion_matrix'])
        labels = metrics.get('labels', metrics.get('confusion_matrix_labels', ['NEGATIVE', 'NEUTRAL', 'POSITIVE']))
    else:
        # Formato antigo (dados no nível raiz)
        metrics = results_data.get('metrics', results_data)
        cm = np.array(results_data.get('confusion_matrix', metrics.get('confusion_matrix')))
        labels = results_data.get('confusion_matrix_labels', metrics.get('labels', ['NEGATIVE', 'NEUTRAL', 'POSITIVE']))
    
    timestamp = results_data['timestamp']
    dataset = results_data.get('dataset', 'Unknown')
    language = results_data.get('language', 'Unknown')
    
    print(f"✅ Dataset: {dataset}")
    print(f"✅ Idioma: {language}")
    print(f"✅ Total de amostras: {results_data['total_samples']:,}")
    print(f"✅ Accuracy: {metrics['accuracy']*100:.2f}%")
    print("\nGerando visualizações...\n")
    
    graphs_dir = create_graphs_directory()
    
    # Identificar nome do dataset para nomes de arquivo
    if 'twitter' in dataset.lower() and 'airline' in dataset.lower():
        dataset_short = 'twitter_airline'
    elif 'tweets' in dataset.lower() and ('portuguese' in language.lower() or 'pt' in dataset.lower()):
        dataset_short = 'tweets_pt'
    elif 'imdb' in dataset.lower():
        dataset_short = 'imdb'
    elif 'airespucrs' in dataset.lower() or 'airespucrs' in results_file.lower():
        dataset_short = 'airespucrs'
    else:
        dataset_short = dataset.lower().replace(' ', '_')[:20]
    
    # Calcular métricas por classe a partir da matriz de confusão
    per_class_metrics = calculate_per_class_metrics_from_cm(cm, labels)
    
    # Gerar gráficos
    plot_confusion_matrix(
        cm, labels,
        os.path.join(graphs_dir, f'confusion_matrix_{dataset_short}_{timestamp}.png'),
        title=f"Matriz de Confusão ({dataset})",
        dataset_name=dataset_short
    )
    
    plot_normalized_confusion_matrix(
        cm, labels,
        os.path.join(graphs_dir, f'confusion_matrix_normalized_{dataset_short}_{timestamp}.png'),
        title=f"Matriz de Confusão Normalizada ({dataset})",
        dataset_name=dataset_short
    )
    
    plot_general_metrics(
        metrics,
        os.path.join(graphs_dir, f'metrics_{dataset_short}_{timestamp}.png'),
        title=f"Métricas Gerais ({dataset})",
        dataset_name=dataset_short
    )
    
    plot_per_class_metrics(
        per_class_metrics, labels,
        os.path.join(graphs_dir, f'per_class_metrics_{dataset_short}_{timestamp}.png'),
        title=f"Métricas por Classe ({dataset})",
        dataset_name=dataset_short
    )
    
    print("\n" + "="*80)
    print("✅ TODOS OS GRÁFICOS GERADOS COM SUCESSO!")
    print("="*80)
    print("\nArquivos gerados:")
    print(f"  1. {graphs_dir}/confusion_matrix_{dataset_short}_{timestamp}.png")
    print(f"  2. {graphs_dir}/confusion_matrix_normalized_{dataset_short}_{timestamp}.png")
    print(f"  3. {graphs_dir}/metrics_{dataset_short}_{timestamp}.png")
    print(f"  4. {graphs_dir}/per_class_metrics_{dataset_short}_{timestamp}.png")
    print("\n📝 Prontos para inclusão na monografia")

if __name__ == "__main__":
    main()


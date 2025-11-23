#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera tabela e gráfico comparando métricas do benchmark vs validação
"""

import json
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Carregar resultados (usar o mais recente) - tenta results/, depois api_load_testing, depois local
json_files = glob.glob('results/metrics_comparison_benchmark_*.json')
if not json_files:
    json_files = glob.glob('../api_load_testing/metrics_comparison_benchmark_*.json')
if not json_files:
    json_files = glob.glob('metrics_comparison_benchmark_*.json')
if json_files:
    latest_file = max(json_files, key=os.path.getctime)
    print(f"Carregando: {latest_file}")
    with open(latest_file, 'r') as f:
        data = json.load(f)
else:
    raise FileNotFoundError("Nenhum arquivo de resultados encontrado")

benchmark = data['benchmark_metrics']
validation = data['overall_validation_metrics']
comparison = data['comparison']

# Criar tabela comparativa
print("="*80)
print("TABELA COMPARATIVA: BENCHMARK vs VALIDAÇÃO")
print("="*80)
print()
print(f"{'Métrica':<15} {'Benchmark':<12} {'Validação':<12} {'Diferença':<15} {'Status':<15}")
print("-"*80)

metrics = [
    ('Accuracy', 'accuracy'),
    ('Precision', 'precision'),
    ('Recall', 'recall'),
    ('F1-Score', 'f1_score')
]

for name, key in metrics:
    bench_val = benchmark[key]
    valid_val = validation[key]
    diff = comparison['differences'][key]
    rel_diff = comparison['relative_differences_pct'][key]
    similar = comparison['similar'][key]
    status = "✓ Similar" if similar else "⚠ Diferente"
    
    print(f"{name:<15} {bench_val:>11.2%} {valid_val:>11.2%} {diff:>+14.4f} ({rel_diff:>+6.2f}%) {status:<15}")

print()
print(f"Total de comentários analisados: {validation['total_comments']:,}")
print(f"Total de vídeos analisados: {data['total_videos_analyzed']}")
print()

# Criar gráfico comparativo
fig, ax = plt.subplots(1, 1, figsize=(12, 7))

# Comparação lado a lado
metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
metrics_keys = ['accuracy', 'precision', 'recall', 'f1_score']

x = np.arange(len(metrics_names))
width = 0.35

benchmark_values = [benchmark[key] * 100 for key in metrics_keys]
validation_values = [validation[key] * 100 for key in metrics_keys]

bars1 = ax.bar(x - width/2, benchmark_values, width, label='Benchmark Inicial', 
                color='#2196F3', edgecolor='black', linewidth=1.5, alpha=0.8)
bars2 = ax.bar(x + width/2, validation_values, width, label='Validação Atual', 
                color='#FF9800', edgecolor='black', linewidth=1.5, alpha=0.8)

ax.set_xlabel('Métrica', fontsize=12, fontweight='bold')
ax.set_ylabel('Valor (%)', fontsize=12, fontweight='bold')
total_videos = data.get('total_videos_analyzed', 0)
total_comments = data.get('overall_validation_metrics', {}).get('total_comments', 0)
ax.set_title(f'Comparação de Métricas: Benchmark vs Validação\n({total_videos} vídeos, {total_comments:,} comentários)', 
              fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(metrics_names, rotation=0)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_ylim([0, 100])

# Adicionar valores nas barras
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom',
                fontsize=9, fontweight='bold')

plt.tight_layout()
os.makedirs('graphs', exist_ok=True)
output_file = f'graphs/metrics_comparison_benchmark_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Gráfico salvo: {output_file}")

# Criar tabela em formato LaTeX/Markdown para documento
print()
print("="*80)
print("TABELA PARA DOCUMENTO (Markdown)")
print("="*80)
print()
print("| Métrica | Benchmark | Validação | Diferença | Diferença Relativa | Status |")
print("|---------|-----------|-----------|-----------|-------------------|--------|")

for name, key in metrics:
    bench_val = benchmark[key]
    valid_val = validation[key]
    diff = comparison['differences'][key]
    rel_diff = comparison['relative_differences_pct'][key]
    similar = "✓ Similar" if comparison['similar'][key] else "⚠ Diferente"
    
    print(f"| {name} | {bench_val:.2%} | {valid_val:.2%} | {diff:+.4f} | {rel_diff:+.2f}% | {similar} |")

print()
print(f"**Nota:** Validação realizada com {total_videos} vídeos e {total_comments:,} comentários.")


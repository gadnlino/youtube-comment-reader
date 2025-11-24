#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Confusion Matrix Visualization for TF-IDF + Logistic Regression Model

Based on the evaluation results from the benchmark comparison.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Confusion Matrix data from MODEL_EVALUATION_METHODOLOGY.md
# These are the actual results from the TF-IDF + Logistic Regression benchmark
confusion_matrix = np.array([
    [45639, 17057, 6519],   # Actual Negative
    [14217, 44848, 9502],   # Actual Neutral
    [8725, 13885, 46053]    # Actual Positive
])

# Labels
class_labels = ['Negativo', 'Neutro', 'Positivo']
class_labels_en = ['Negative', 'Neutral', 'Positive']

# Calculate totals for percentage calculation
row_sums = confusion_matrix.sum(axis=1, keepdims=True)
confusion_matrix_pct = (confusion_matrix / row_sums * 100).round(1)

# Calculate metrics from confusion matrix
total_samples = confusion_matrix.sum()
correct_predictions = np.trace(confusion_matrix)
accuracy = (correct_predictions / total_samples * 100)

# Per-class metrics
recalls = []
precisions = []
for i in range(3):
    # Recall: TP / (TP + FN) - row-wise
    recall = confusion_matrix[i, i] / confusion_matrix[i, :].sum() * 100
    recalls.append(recall)
    
    # Precision: TP / (TP + FP) - column-wise
    precision = confusion_matrix[i, i] / confusion_matrix[:, i].sum() * 100
    precisions.append(precision)

print("="*80)
print("MATRIZ DE CONFUSÃO - TF-IDF + Logistic Regression")
print("="*80)
print()
print(f"Acurácia Geral: {accuracy:.2f}%")
print()
print("Métricas por Classe:")
for i, label in enumerate(class_labels):
    print(f"  {label:10s}: Recall = {recalls[i]:5.2f}%  |  Precision = {precisions[i]:5.2f}%")
print()

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# ===== Subplot 1: Absolute counts =====
sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues', 
            xticklabels=class_labels, yticklabels=class_labels,
            cbar_kws={'label': 'Número de Comentários'},
            ax=ax1, square=True, linewidths=0.5, linecolor='gray')
ax1.set_xlabel('Predito', fontsize=12, fontweight='bold')
ax1.set_ylabel('Real (Ground Truth)', fontsize=12, fontweight='bold')
ax1.set_title('Matriz de Confusão - Contagens Absolutas\n' + 
              f'Acurácia: {accuracy:.2f}% | Total: {total_samples:,} comentários',
              fontsize=13, fontweight='bold', pad=15)

# ===== Subplot 2: Percentages =====
# Create annotations with both count and percentage
annotations = []
for i in range(3):
    row = []
    for j in range(3):
        count = confusion_matrix[i, j]
        pct = confusion_matrix_pct[i, j]
        row.append(f'{count:,}\n({pct:.1f}%)')
    annotations.append(row)

sns.heatmap(confusion_matrix_pct, annot=annotations, fmt='', cmap='RdYlGn_r',
            xticklabels=class_labels, yticklabels=class_labels,
            cbar_kws={'label': 'Porcentagem da Classe Real (%)'},
            ax=ax2, square=True, linewidths=0.5, linecolor='gray',
            vmin=0, vmax=100)
ax2.set_xlabel('Predito', fontsize=12, fontweight='bold')
ax2.set_ylabel('Real (Ground Truth)', fontsize=12, fontweight='bold')
ax2.set_title('Matriz de Confusão - Porcentagens Normalizadas por Linha\n' + 
              '(% de cada classe real que foi predita como cada classe)',
              fontsize=13, fontweight='bold', pad=15)

# Add metrics text
metrics_text = (
    f"Recall (Sensibilidade):\n"
    f"  • Negativo: {recalls[0]:.1f}%\n"
    f"  • Neutro: {recalls[1]:.1f}%\n"
    f"  • Positivo: {recalls[2]:.1f}%\n\n"
    f"Precision (Precisão):\n"
    f"  • Negativo: {precisions[0]:.1f}%\n"
    f"  • Neutro: {precisions[1]:.1f}%\n"
    f"  • Positivo: {precisions[2]:.1f}%"
)

fig.text(0.5, -0.02, metrics_text, ha='center', va='top', 
         fontsize=10, family='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.suptitle('Desempenho do Modelo TF-IDF + Logistic Regression', 
             fontsize=15, fontweight='bold', y=0.98)

plt.tight_layout(rect=[0, 0.08, 1, 0.96])

# Save figure
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f'confusion_matrix_tfidf_logistic_{timestamp}.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Matriz de confusão salva: {output_file}")
print()

# ===== Also create a simple version (Portuguese only) =====
fig2, ax = plt.subplots(figsize=(10, 8))

# Create annotations with both count and percentage
annotations_simple = []
for i in range(3):
    row = []
    for j in range(3):
        count = confusion_matrix[i, j]
        pct = confusion_matrix_pct[i, j]
        row.append(f'{count:,}\n({pct:.1f}%)')
    annotations_simple.append(row)

sns.heatmap(confusion_matrix, annot=annotations_simple, fmt='', cmap='Blues',
            xticklabels=class_labels, yticklabels=class_labels,
            cbar_kws={'label': 'Número de Comentários'},
            ax=ax, square=True, linewidths=1, linecolor='white',
            annot_kws={'fontsize': 11, 'fontweight': 'bold'})

ax.set_xlabel('Sentimento Predito', fontsize=13, fontweight='bold')
ax.set_ylabel('Sentimento Real', fontsize=13, fontweight='bold')
ax.set_title(f'Matriz de Confusão - TF-IDF + Logistic Regression\n' +
             f'Acurácia: {accuracy:.2f}% | Dataset: {total_samples:,} comentários',
             fontsize=14, fontweight='bold', pad=20)

# Add recall values on the right
for i, (label, recall) in enumerate(zip(class_labels, recalls)):
    ax.text(3.3, i + 0.5, f'Recall:\n{recall:.1f}%', 
            va='center', ha='left', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))

# Add precision values on the bottom
for i, (label, precision) in enumerate(zip(class_labels, precisions)):
    ax.text(i + 0.5, 3.3, f'Precision:\n{precision:.1f}%', 
            va='top', ha='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))

plt.tight_layout()

# Save simple version
output_file_simple = f'confusion_matrix_tfidf_pt.png'
plt.savefig(output_file_simple, dpi=300, bbox_inches='tight')
print(f"✓ Matriz de confusão simplificada salva: {output_file_simple}")
print()

print("="*80)
print("INTERPRETAÇÃO DA MATRIZ DE CONFUSÃO")
print("="*80)
print()
print("• Diagonal principal (azul escuro): Predições CORRETAS")
print(f"  - {confusion_matrix[0,0]:,} negativos identificados corretamente")
print(f"  - {confusion_matrix[1,1]:,} neutros identificados corretamente")
print(f"  - {confusion_matrix[2,2]:,} positivos identificados corretamente")
print()
print("• Fora da diagonal: Predições INCORRETAS (confusões)")
print(f"  - Maior confusão: Negativo → Neutro ({confusion_matrix[0,1]:,} casos, {confusion_matrix_pct[0,1]:.1f}%)")
print(f"  - Segunda maior: Neutro → Positivo ({confusion_matrix[1,2]:,} casos, {confusion_matrix_pct[1,2]:.1f}%)")
print(f"  - Terceira maior: Neutro → Negativo ({confusion_matrix[1,0]:,} casos, {confusion_matrix_pct[1,0]:.1f}%)")
print()
print("• Observações:")
print(f"  - Classe POSITIVA tem melhor recall ({recalls[2]:.1f}%)")
print(f"  - Classe NEGATIVA tem pior recall ({recalls[0]:.1f}%)")
print(f"  - Modelo tende a confundir comentários polares (pos/neg) com neutros")
print()

plt.show()


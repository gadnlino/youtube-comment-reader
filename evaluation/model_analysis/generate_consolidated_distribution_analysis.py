#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Consolidated Distribution Analysis Graphs

Creates academic-quality visualizations showing the systematic bias
of the TF-IDF + Logistic Regression model.
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Load results
with open('distribution_validation_results_20251118_103853.json', 'r') as f:
    results = json.load(f)

print(f"Loaded {len(results)} video results")

# Extract data
video_titles = []
gt_pos_pct = []
gt_neg_pct = []
gt_neu_pct = []
pred_pos_pct = []
pred_neg_pct = []
pred_neu_pct = []
diff_pos = []
diff_neg = []
diff_neu = []

for r in results:
    video_titles.append(r['video_title'][:40] + '...' if len(r['video_title']) > 40 else r['video_title'])
    
    gt_pos_pct.append(r['ground_truth']['POSITIVE_PCT'])
    gt_neg_pct.append(r['ground_truth']['NEGATIVE_PCT'])
    gt_neu_pct.append(r['ground_truth']['NEUTRAL_PCT'])
    
    pred_pos_pct.append(r['predicted']['POSITIVE_PCT'])
    pred_neg_pct.append(r['predicted']['NEGATIVE_PCT'])
    pred_neu_pct.append(r['predicted']['NEUTRAL_PCT'])
    
    diff_pos.append(r['predicted']['POSITIVE_PCT'] - r['ground_truth']['POSITIVE_PCT'])
    diff_neg.append(r['predicted']['NEGATIVE_PCT'] - r['ground_truth']['NEGATIVE_PCT'])
    diff_neu.append(r['predicted']['NEUTRAL_PCT'] - r['ground_truth']['NEUTRAL_PCT'])

# ============================================================================
# GRAPH 1: Average Distribution Comparison (Ground Truth vs Predicted)
# ============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

categories = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
gt_avg = [np.mean(gt_pos_pct), np.mean(gt_neg_pct), np.mean(gt_neu_pct)]
pred_avg = [np.mean(pred_pos_pct), np.mean(pred_neg_pct), np.mean(pred_neu_pct)]

x = np.arange(len(categories))
width = 0.35

bars1 = ax.bar(x - width/2, gt_avg, width, label='Ground Truth (Dataset)', 
               color='#4A90E2', edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x + width/2, pred_avg, width, label='Predição do Modelo (API)',
               color='#E94B3C', edgecolor='black', linewidth=1.5)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('Percentual Médio (%)', fontsize=13, fontweight='bold')
ax.set_title('Comparação de Distribuição Média: Ground Truth vs Predição do Modelo\n(N=18 vídeos)',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
ax.legend(fontsize=11, loc='upper left')
ax.set_ylim(0, max(max(gt_avg), max(pred_avg)) + 10)
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('consolidated_avg_distribution_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: consolidated_avg_distribution_comparison.png")
plt.close()

# ============================================================================
# GRAPH 2: Bias Boxplot (Difference: Predicted - Ground Truth)
# ============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

bias_data = [diff_pos, diff_neg, diff_neu]
colors = ['#4CAF50', '#F44336', '#FF9800']

bp = ax.boxplot(bias_data, labels=categories, patch_artist=True,
                widths=0.6, showmeans=True, meanline=True,
                boxprops=dict(linewidth=1.5),
                whiskerprops=dict(linewidth=1.5),
                capprops=dict(linewidth=1.5),
                medianprops=dict(color='black', linewidth=2),
                meanprops=dict(color='blue', linewidth=2, linestyle='--'))

for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Add zero line
ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='Sem Viés (0%)')

ax.set_ylabel('Viés do Modelo (Predição - Ground Truth, %)', fontsize=13, fontweight='bold')
ax.set_xlabel('Sentimento', fontsize=13, fontweight='bold')
ax.set_title('Viés Sistemático do Modelo TF-IDF + Logistic Regression\n(N=18 vídeos)',
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.legend(fontsize=11)

# Add annotation
textstr = f'''Observação:
• NEUTRAL: Viés POSITIVO (+{np.mean(diff_neu):.1f}%)
• NEGATIVE: Viés NEGATIVO ({np.mean(diff_neg):.1f}%)
• POSITIVE: Relativamente balanceado ({np.mean(diff_pos):.1f}%)'''

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.98, 0.97, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right', bbox=props)

plt.tight_layout()
plt.savefig('consolidated_model_bias_boxplot.png', dpi=300, bbox_inches='tight')
print("✓ Saved: consolidated_model_bias_boxplot.png")
plt.close()

# ============================================================================
# GRAPH 3: Scatter Plot - Ground Truth vs Predicted (per sentiment)
# ============================================================================

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

sentiments = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
gt_data = [gt_pos_pct, gt_neg_pct, gt_neu_pct]
pred_data = [pred_pos_pct, pred_neg_pct, pred_neu_pct]
colors_scatter = ['#4CAF50', '#F44336', '#FF9800']

for i, (ax, sentiment, gt, pred, color) in enumerate(zip(axes, sentiments, gt_data, pred_data, colors_scatter)):
    ax.scatter(gt, pred, s=100, alpha=0.6, color=color, edgecolors='black', linewidth=1.5)
    
    # Add perfect prediction line (y=x)
    max_val = max(max(gt), max(pred))
    ax.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='Predição Perfeita (y=x)')
    
    # Add best fit line
    z = np.polyfit(gt, pred, 1)
    p = np.poly1d(z)
    ax.plot(gt, p(gt), 'b-', linewidth=2, alpha=0.7, label=f'Linha de Tendência (y={z[0]:.2f}x+{z[1]:.2f})')
    
    # Calculate correlation
    corr = np.corrcoef(gt, pred)[0, 1]
    
    ax.set_xlabel(f'Ground Truth ({sentiment}, %)', fontsize=11, fontweight='bold')
    ax.set_ylabel(f'Predição do Modelo ({sentiment}, %)', fontsize=11, fontweight='bold')
    ax.set_title(f'{sentiment}\nCorrelação: {corr:.3f}', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='upper left')
    ax.grid(alpha=0.3, linestyle='--')
    ax.set_xlim(0, max_val + 5)
    ax.set_ylim(0, max_val + 5)

fig.suptitle('Correlação: Ground Truth vs Predição do Modelo (N=18 vídeos)',
             fontsize=15, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('consolidated_correlation_scatter.png', dpi=300, bbox_inches='tight')
print("✓ Saved: consolidated_correlation_scatter.png")
plt.close()

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)
print()
print(f"Number of videos: {len(results)}")
print()
print("Average Ground Truth Distribution:")
print(f"  POSITIVE: {np.mean(gt_pos_pct):.2f}% (σ={np.std(gt_pos_pct):.2f}%)")
print(f"  NEGATIVE: {np.mean(gt_neg_pct):.2f}% (σ={np.std(gt_neg_pct):.2f}%)")
print(f"  NEUTRAL:  {np.mean(gt_neu_pct):.2f}% (σ={np.std(gt_neu_pct):.2f}%)")
print()
print("Average Predicted Distribution:")
print(f"  POSITIVE: {np.mean(pred_pos_pct):.2f}% (σ={np.std(pred_pos_pct):.2f}%)")
print(f"  NEGATIVE: {np.mean(pred_neg_pct):.2f}% (σ={np.std(pred_neg_pct):.2f}%)")
print(f"  NEUTRAL:  {np.mean(pred_neu_pct):.2f}% (σ={np.std(pred_neu_pct):.2f}%)")
print()
print("Average Bias (Predicted - Ground Truth):")
print(f"  POSITIVE: {np.mean(diff_pos):+.2f}% (σ={np.std(diff_pos):.2f}%)")
print(f"  NEGATIVE: {np.mean(diff_neg):+.2f}% (σ={np.std(diff_neg):.2f}%)")
print(f"  NEUTRAL:  {np.mean(diff_neu):+.2f}% (σ={np.std(diff_neu):.2f}%)")
print()
print("Chi-square Test Results:")
avg_chi2_pval = np.mean([r['comparison']['chi2_pvalue'] for r in results])
print(f"  Average p-value: {avg_chi2_pval:.4f}")
print(f"  Videos with p>0.05 (similar distributions): {sum(1 for r in results if r['comparison']['chi2_pvalue'] > 0.05)}/{len(results)}")
print()
print("="*80)


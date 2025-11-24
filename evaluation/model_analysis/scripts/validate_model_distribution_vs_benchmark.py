#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model Distribution Validation vs Benchmark Initial

Este script compara a distribuição de sentimento observada na validação atual
(145 vídeos, ~72.500 comentários) com a distribuição observada no benchmark
inicial quando o modelo foi selecionado.

Objetivo: Verificar se o modelo mantém a mesma distribuição de sentimento
(quantidades de comentários classificados como positivo, negativo e neutro)
que foi observada durante a seleção do modelo no benchmark inicial.

Benchmark inicial (calculado a partir da matriz de confusão):
- Total de comentários no test set: 206,445
- Predicted POSITIVE: 62,074 (30.04%)
- Predicted NEGATIVE: 68,581 (33.23%)
- Predicted NEUTRAL: 75,790 (36.73%)
"""

import requests
import pandas as pd
import json
import time
import os
import numpy as np
from datetime import datetime
from scipy.stats import chisquare
import matplotlib.pyplot as plt
import seaborn as sns

# API Configuration
API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod"

# Sentiment mapping
SENTIMENT_MAP = {
    'Positive': 'POSITIVE',
    'Negative': 'NEGATIVE',
    'Neutral': 'NEUTRAL'
}

# Benchmark Initial Distribution (calculated from confusion matrix)
# Confusion Matrix:
#                  Predicted
#              Neg    Neu    Pos
# Actual Neg  45639  17057  6519
#         Neu  14217  44848  9502
#         Pos  8725   13885  46053
#
# Predicted totals:
# - NEGATIVE: 45639 + 14217 + 8725 = 68,581 (33.23%)
# - NEUTRAL:  17057 + 44848 + 13885 = 75,790 (36.73%)
# - POSITIVE: 6519 + 9502 + 46053 = 62,074 (30.04%)
# Total: 206,445

BENCHMARK_INITIAL_DISTRIBUTION = {
    'POSITIVE': 62074,
    'NEGATIVE': 68581,
    'NEUTRAL': 75790,
    'TOTAL': 206445,
    'POSITIVE_PCT': 30.04,
    'NEGATIVE_PCT': 33.23,
    'NEUTRAL_PCT': 36.73
}

# Configuration
N_SETS = 5  # Number of random sets
M_VIDEOS_PER_SET = 29  # Videos per set (145 / 5 = 29)
MIN_COMMENTS = 500  # Minimum comments per video
# Pre-filtered working videos - tenta data/, depois api_load_testing, depois local
WORKING_VIDEOS_FILE = 'data/working_videos_20251118_121130.json'
if not os.path.exists(WORKING_VIDEOS_FILE):
    WORKING_VIDEOS_FILE = '../api_load_testing/working_videos_20251118_121130.json'
if not os.path.exists(WORKING_VIDEOS_FILE):
    WORKING_VIDEOS_FILE = 'working_videos_20251118_121130.json'

def fetch_comments_with_sentiment(video_id, max_results=500, retries=3):
    """Fetch comments with sentiment analysis from API."""
    endpoint = f"{API_BASE_URL}/video/comments"
    params = {
        'videoId': video_id,
        'maxResults': max_results,
        'part': 'snippet',
        'showPositives': 'true',
        'showNegatives': 'true',
        'showNeutral': 'true'
    }
    
    last_error = None
    for attempt in range(retries):
        try:
            response = requests.get(endpoint, params=params, timeout=60)
            response.raise_for_status()
            return response.json().get('items', []), None
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            if attempt == retries - 1:
                return [], last_error
            time.sleep(2)
    return [], last_error

def get_distribution(comments_list, label_key='sentiment'):
    """Calculate sentiment distribution from a list."""
    sentiments = [c.get(label_key, 'UNKNOWN') for c in comments_list]
    total = len(sentiments)
    
    pos = sentiments.count('POSITIVE')
    neg = sentiments.count('NEGATIVE')
    neu = sentiments.count('NEUTRAL')
    
    return {
        'POSITIVE': pos,
        'NEGATIVE': neg,
        'NEUTRAL': neu,
        'POSITIVE_PCT': (pos / total * 100) if total > 0 else 0,
        'NEGATIVE_PCT': (neg / total * 100) if total > 0 else 0,
        'NEUTRAL_PCT': (neu / total * 100) if total > 0 else 0,
        'TOTAL': total
    }

def compare_with_benchmark(validation_dist, benchmark_dist):
    """
    Compare validation distribution with benchmark initial distribution.
    
    Args:
        validation_dist: Distribution from current validation
        benchmark_dist: Distribution from initial benchmark
        
    Returns:
        Comparison metrics including chi-square test and differences
    """
    validation_total = validation_dist['TOTAL']
    benchmark_total = benchmark_dist['TOTAL']
    
    # Observed (current validation)
    observed = [
        validation_dist['POSITIVE'],
        validation_dist['NEGATIVE'],
        validation_dist['NEUTRAL']
    ]
    
    # Expected (benchmark distribution scaled to validation total)
    expected = [
        (benchmark_dist['POSITIVE'] / benchmark_total) * validation_total,
        (benchmark_dist['NEGATIVE'] / benchmark_total) * validation_total,
        (benchmark_dist['NEUTRAL'] / benchmark_total) * validation_total
    ]
    
    # Chi-square test
    chi2_stat, chi2_pval = chisquare(observed, expected)
    
    # Percentage differences (validation - benchmark)
    pct_diff = {
        'POSITIVE': validation_dist['POSITIVE_PCT'] - benchmark_dist['POSITIVE_PCT'],
        'NEGATIVE': validation_dist['NEGATIVE_PCT'] - benchmark_dist['NEGATIVE_PCT'],
        'NEUTRAL': validation_dist['NEUTRAL_PCT'] - benchmark_dist['NEUTRAL_PCT']
    }
    
    avg_abs_diff = np.mean([abs(v) for v in pct_diff.values()])
    
    return {
        'chi2_statistic': chi2_stat,
        'chi2_pvalue': chi2_pval,
        'percentage_differences': pct_diff,
        'avg_absolute_difference': avg_abs_diff,
        'distributions_similar': chi2_pval > 0.05  # p-value > 0.05 means similar distributions
    }

def process_video(video_data, df_ground_truth, verbose=False):
    """Process a single video and get predicted distribution."""
    video_id = video_data['id']
    video_title = video_data['title']
    
    if verbose:
        print(f"\n  Processing: {video_title[:60]}...")
    
    # Fetch comments from API
    api_comments, error = fetch_comments_with_sentiment(video_id, max_results=500)
    
    if len(api_comments) == 0:
        if verbose:
            print(f"    ✗ Failed to fetch comments")
            if error:
                print(f"       Error: {error}")
        return {'error': error, 'video_id': video_id, 'video_title': video_title}
    
    predicted_dist = get_distribution(api_comments)
    
    # Compare with benchmark
    benchmark_comparison = compare_with_benchmark(predicted_dist, BENCHMARK_INITIAL_DISTRIBUTION)
    
    if verbose:
        print(f"    ✓ API: {predicted_dist['POSITIVE_PCT']:.1f}% POS, {predicted_dist['NEGATIVE_PCT']:.1f}% NEG, {predicted_dist['NEUTRAL_PCT']:.1f}% NEU")
        print(f"    ✓ Benchmark: {BENCHMARK_INITIAL_DISTRIBUTION['POSITIVE_PCT']:.1f}% POS, {BENCHMARK_INITIAL_DISTRIBUTION['NEGATIVE_PCT']:.1f}% NEG, {BENCHMARK_INITIAL_DISTRIBUTION['NEUTRAL_PCT']:.1f}% NEU")
        print(f"    ✓ Diff: {benchmark_comparison['percentage_differences']['POSITIVE']:+.1f}% POS, {benchmark_comparison['percentage_differences']['NEGATIVE']:+.1f}% NEG, {benchmark_comparison['percentage_differences']['NEUTRAL']:+.1f}% NEU")
    
    return {
        'video_id': video_id,
        'video_title': video_title,
        'predicted': predicted_dist,
        'benchmark_comparison': benchmark_comparison
    }

def select_video_sets(n_sets, m_videos_per_set, working_videos_file):
    """Select N random sets of M videos each from pre-filtered working videos."""
    print(f"\nSelecting {n_sets} random sets of {m_videos_per_set} videos each...")
    
    # Load pre-filtered working videos
    if not os.path.exists(working_videos_file):
        raise FileNotFoundError(f"Working videos file not found: {working_videos_file}")
    
    with open(working_videos_file, 'r', encoding='utf-8') as f:
        working_videos = json.load(f)
    
    print(f"✓ Loaded {len(working_videos)} pre-filtered working videos")
    
    # Shuffle videos for random selection
    import random
    random.seed(42)
    random.shuffle(working_videos)
    
    # Calculate how many videos we need and can use
    total_needed = n_sets * m_videos_per_set
    total_available = len(working_videos)
    
    if total_available < total_needed:
        print(f"⚠️  Warning: Only {total_available} videos available, needed {total_needed}")
        print(f"    Adjusting to use all available videos...")
        n_sets = total_available // m_videos_per_set
        total_needed = n_sets * m_videos_per_set
    
    # Use only the needed videos
    selected_videos = working_videos[:total_needed]
    
    # Split into N sets
    sets = []
    for i in range(n_sets):
        start_idx = i * m_videos_per_set
        end_idx = start_idx + m_videos_per_set
        set_videos = selected_videos[start_idx:end_idx]
        sets.append(set_videos)
        print(f"✓ Set {i+1}: {len(set_videos)} videos")
    
    return sets

def process_set(set_idx, videos, df_ground_truth):
    """Process all videos in a set."""
    print(f"\n{'='*80}")
    print(f"PROCESSING SET {set_idx + 1}/{N_SETS}")
    print(f"{'='*80}")
    
    results = []
    errors = []
    successful = 0
    failed = 0
    
    for i, video in enumerate(videos, 1):
        print(f"\n  [{i}/{len(videos)}]", end=" ")
        result = process_video(video, df_ground_truth, verbose=True)
        
        if result and 'error' in result:
            # Failed video
            errors.append(result)
            failed += 1
        elif result:
            # Successful video
            results.append(result)
            successful += 1
        else:
            # Unexpected None
            failed += 1
        
        # Rate limiting
        if i < len(videos):
            time.sleep(2)
    
    print(f"\n  Set {set_idx + 1} Summary: {successful} successful, {failed} failed")
    
    return results, errors

def calculate_set_statistics(set_results):
    """Calculate aggregate statistics for a set comparing with benchmark."""
    if len(set_results) == 0:
        return None
    
    # Extract predicted percentages
    pred_pos = [r['predicted']['POSITIVE_PCT'] for r in set_results]
    pred_neg = [r['predicted']['NEGATIVE_PCT'] for r in set_results]
    pred_neu = [r['predicted']['NEUTRAL_PCT'] for r in set_results]
    
    # Extract differences from benchmark
    diff_pos = [r['benchmark_comparison']['percentage_differences']['POSITIVE'] for r in set_results]
    diff_neg = [r['benchmark_comparison']['percentage_differences']['NEGATIVE'] for r in set_results]
    diff_neu = [r['benchmark_comparison']['percentage_differences']['NEUTRAL'] for r in set_results]
    
    # Chi-square p-values
    chi2_pvalues = [r['benchmark_comparison']['chi2_pvalue'] for r in set_results]
    
    # Aggregate distribution (sum all comments)
    total_comments = sum(r['predicted']['TOTAL'] for r in set_results)
    total_pos = sum(r['predicted']['POSITIVE'] for r in set_results)
    total_neg = sum(r['predicted']['NEGATIVE'] for r in set_results)
    total_neu = sum(r['predicted']['NEUTRAL'] for r in set_results)
    
    aggregated_dist = {
        'POSITIVE': total_pos,
        'NEGATIVE': total_neg,
        'NEUTRAL': total_neu,
        'TOTAL': total_comments,
        'POSITIVE_PCT': (total_pos / total_comments * 100) if total_comments > 0 else 0,
        'NEGATIVE_PCT': (total_neg / total_comments * 100) if total_comments > 0 else 0,
        'NEUTRAL_PCT': (total_neu / total_comments * 100) if total_comments > 0 else 0
    }
    
    # Compare aggregated distribution with benchmark
    aggregated_comparison = compare_with_benchmark(aggregated_dist, BENCHMARK_INITIAL_DISTRIBUTION)
    
    return {
        'n_videos': len(set_results),
        'aggregated_distribution': aggregated_dist,
        'aggregated_comparison': aggregated_comparison,
        'predicted': {
            'POSITIVE': {'mean': np.mean(pred_pos), 'std': np.std(pred_pos)},
            'NEGATIVE': {'mean': np.mean(pred_neg), 'std': np.std(pred_neg)},
            'NEUTRAL': {'mean': np.mean(pred_neu), 'std': np.std(pred_neu)}
        },
        'difference_from_benchmark': {
            'POSITIVE': {'mean': np.mean(diff_pos), 'std': np.std(diff_pos)},
            'NEGATIVE': {'mean': np.mean(diff_neg), 'std': np.std(diff_neg)},
            'NEUTRAL': {'mean': np.mean(diff_neu), 'std': np.std(diff_neu)}
        },
        'chi2_pvalue_mean': np.mean(chi2_pvalues),
        'chi2_pvalue_std': np.std(chi2_pvalues),
        'similar_to_benchmark_count': sum(1 for p in chi2_pvalues if p > 0.05)
    }

def generate_comparison_graphs(all_set_stats, timestamp):
    """Generate visualizations comparing validation with benchmark."""
    print("\n" + "="*80)
    print("GENERATING BENCHMARK COMPARISON VISUALIZATIONS")
    print("="*80)
    
    n_sets = len(all_set_stats)
    
    # Extract aggregated distributions for each set
    set_agg_pos = [s['aggregated_distribution']['POSITIVE_PCT'] for s in all_set_stats]
    set_agg_neg = [s['aggregated_distribution']['NEGATIVE_PCT'] for s in all_set_stats]
    set_agg_neu = [s['aggregated_distribution']['NEUTRAL_PCT'] for s in all_set_stats]
    
    # Extract differences from benchmark
    diff_pos_means = [s['difference_from_benchmark']['POSITIVE']['mean'] for s in all_set_stats]
    diff_neg_means = [s['difference_from_benchmark']['NEGATIVE']['mean'] for s in all_set_stats]
    diff_neu_means = [s['difference_from_benchmark']['NEUTRAL']['mean'] for s in all_set_stats]
    
    # ============================================================================
    # GRAPH 1: Distribution comparison (Validation vs Benchmark)
    # ============================================================================
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(3)  # POSITIVE, NEGATIVE, NEUTRAL
    width = 0.35
    
    # Benchmark bars
    benchmark_values = [
        BENCHMARK_INITIAL_DISTRIBUTION['POSITIVE_PCT'],
        BENCHMARK_INITIAL_DISTRIBUTION['NEGATIVE_PCT'],
        BENCHMARK_INITIAL_DISTRIBUTION['NEUTRAL_PCT']
    ]
    
    # Validation average (across all sets)
    validation_avg = [
        np.mean(set_agg_pos),
        np.mean(set_agg_neg),
        np.mean(set_agg_neu)
    ]
    
    validation_std = [
        np.std(set_agg_pos),
        np.std(set_agg_neg),
        np.std(set_agg_neu)
    ]
    
    bars1 = ax.bar(x - width/2, benchmark_values, width, label='Benchmark Inicial',
                   color='#2196F3', edgecolor='black', linewidth=1.5, alpha=0.8)
    bars2 = ax.bar(x + width/2, validation_avg, width, label='Validação Atual (Média)',
                   yerr=validation_std, capsize=5, color='#FF9800',
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    
    ax.set_xlabel('Sentimento', fontsize=13, fontweight='bold')
    ax.set_ylabel('Percentual (%)', fontsize=13, fontweight='bold')
    ax.set_title('Comparação: Distribuição Benchmark vs Validação Atual\n(145 vídeos, ~72.500 comentários)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(['POSITIVE', 'NEGATIVE', 'NEUTRAL'])
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%', ha='center', va='bottom',
                   fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    output_file = f'benchmark_vs_validation_distribution_{timestamp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()
    
    # ============================================================================
    # GRAPH 2: Differences from benchmark by set
    # ============================================================================
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    set_indices = list(range(1, n_sets + 1))
    x = np.arange(n_sets)
    width = 0.25
    
    bars1 = ax.bar(x - width, diff_pos_means, width, label='POSITIVE',
                   color='#4CAF50', edgecolor='black', linewidth=1.5, alpha=0.8)
    bars2 = ax.bar(x, diff_neg_means, width, label='NEGATIVE',
                   color='#F44336', edgecolor='black', linewidth=1.5, alpha=0.8)
    bars3 = ax.bar(x + width, diff_neu_means, width, label='NEUTRAL',
                   color='#FF9800', edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Add zero line
    ax.axhline(y=0, color='blue', linestyle='--', linewidth=2, 
               label='Benchmark Inicial (0%)')
    
    ax.set_xlabel('Conjunto de Vídeos', fontsize=13, fontweight='bold')
    ax.set_ylabel('Diferença vs Benchmark (Validação - Benchmark, %)', 
                  fontsize=13, fontweight='bold')
    ax.set_title('Diferença da Distribuição vs Benchmark por Conjunto\n(Valores positivos = validação maior que benchmark)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels([f'Set {i}' for i in set_indices])
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    output_file = f'benchmark_difference_by_set_{timestamp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()
    
    # ============================================================================
    # GRAPH 3: Overall comparison with confidence intervals
    # ============================================================================
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Calculate overall differences
    overall_diff_pos = np.mean(diff_pos_means)
    overall_diff_neg = np.mean(diff_neg_means)
    overall_diff_neu = np.mean(diff_neu_means)
    
    # 95% CI
    sem_pos = np.std(diff_pos_means) / np.sqrt(n_sets)
    sem_neg = np.std(diff_neg_means) / np.sqrt(n_sets)
    sem_neu = np.std(diff_neu_means) / np.sqrt(n_sets)
    
    ci95_pos = 1.96 * sem_pos
    ci95_neg = 1.96 * sem_neg
    ci95_neu = 1.96 * sem_neu
    
    categories = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
    means = [overall_diff_pos, overall_diff_neg, overall_diff_neu]
    ci95s = [ci95_pos, ci95_neg, ci95_neu]
    colors = ['#4CAF50', '#F44336', '#FF9800']
    
    bars = ax.bar(categories, means, yerr=ci95s, capsize=10,
                  color=colors, edgecolor='black', linewidth=2, alpha=0.8)
    
    # Add value labels
    for bar, mean, ci in zip(bars, means, ci95s):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + (ci if height > 0 else -ci),
               f'{mean:+.2f}%\n±{ci:.2f}%', ha='center',
               va='bottom' if height > 0 else 'top',
               fontsize=12, fontweight='bold')
    
    # Add zero line
    ax.axhline(y=0, color='blue', linestyle='--', linewidth=2,
               label='Benchmark Inicial (0%)')
    
    ax.set_ylabel('Diferença Média vs Benchmark (Validação - Benchmark, %)',
                  fontsize=13, fontweight='bold')
    ax.set_title('Comparação Geral: Validação vs Benchmark Inicial\n(N=5 conjuntos, M=29 vídeos cada, IC 95%)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add annotation
    similar_count = sum(s['aggregated_comparison']['distributions_similar'] for s in all_set_stats)
    textstr = f'''Interpretação:
• Diferenças próximas de 0% = modelo mantém distribuição do benchmark
• {similar_count}/{n_sets} conjuntos com distribuição similar ao benchmark
• Se diferença > ±5%: modelo pode ter mudado comportamento'''
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)
    ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=10,
           verticalalignment='bottom', horizontalalignment='right', bbox=props)
    
    plt.tight_layout()
    output_file = f'benchmark_overall_comparison_ci95_{timestamp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

def main():
    print("="*80)
    print("MODEL DISTRIBUTION VALIDATION vs BENCHMARK INITIAL")
    print("="*80)
    print()
    print(f"Objetivo: Verificar se o modelo mantém a distribuição observada no benchmark inicial")
    print()
    print(f"Benchmark Inicial (do test set):")
    print(f"  POSITIVE: {BENCHMARK_INITIAL_DISTRIBUTION['POSITIVE_PCT']:.2f}%")
    print(f"  NEGATIVE: {BENCHMARK_INITIAL_DISTRIBUTION['NEGATIVE_PCT']:.2f}%")
    print(f"  NEUTRAL:  {BENCHMARK_INITIAL_DISTRIBUTION['NEUTRAL_PCT']:.2f}%")
    print()
    print(f"Configuration:")
    print(f"  Number of sets (N): {N_SETS}")
    print(f"  Videos per set (M): {M_VIDEOS_PER_SET}")
    print(f"  Total videos: {N_SETS * M_VIDEOS_PER_SET}")
    print(f"  Minimum comments per video: {MIN_COMMENTS}")
    print()
    print(f"Starting validation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load ground truth dataset (not used for benchmark comparison, but needed for processing)
    print("Loading ground truth dataset...")
    dataset_path = '../api_load_testing/youtube_comments_cleaned.csv'
    if not os.path.exists(dataset_path):
        dataset_path = 'youtube_comments_cleaned.csv'
    df = pd.read_csv(dataset_path)
    print(f"✓ Loaded {len(df)} comments from dataset")
    
    # Select N random sets of M videos each from pre-filtered working videos
    video_sets = select_video_sets(N_SETS, M_VIDEOS_PER_SET, WORKING_VIDEOS_FILE)
    
    # Process each set
    all_results = []
    all_errors = []
    all_set_stats = []
    
    for i, video_set in enumerate(video_sets):
        set_results, set_errors = process_set(i, video_set, df)
        
        all_errors.extend(set_errors)
        
        if len(set_results) > 0:
            set_stats = calculate_set_statistics(set_results)
            all_set_stats.append(set_stats)
            all_results.extend(set_results)
            
            print(f"\n  Set {i+1} Statistics:")
            print(f"    Aggregated Distribution:")
            print(f"      POSITIVE: {set_stats['aggregated_distribution']['POSITIVE_PCT']:.2f}%")
            print(f"      NEGATIVE: {set_stats['aggregated_distribution']['NEGATIVE_PCT']:.2f}%")
            print(f"      NEUTRAL:  {set_stats['aggregated_distribution']['NEUTRAL_PCT']:.2f}%")
            print(f"    Difference from Benchmark:")
            print(f"      POSITIVE: {set_stats['difference_from_benchmark']['POSITIVE']['mean']:+.2f}% ± {set_stats['difference_from_benchmark']['POSITIVE']['std']:.2f}%")
            print(f"      NEGATIVE: {set_stats['difference_from_benchmark']['NEGATIVE']['mean']:+.2f}% ± {set_stats['difference_from_benchmark']['NEGATIVE']['std']:.2f}%")
            print(f"      NEUTRAL:  {set_stats['difference_from_benchmark']['NEUTRAL']['mean']:+.2f}% ± {set_stats['difference_from_benchmark']['NEUTRAL']['std']:.2f}%")
            print(f"    Similar to benchmark: {set_stats['similar_to_benchmark_count']}/{set_stats['n_videos']} videos")
    
    # Overall summary
    print("\n" + "="*80)
    print("OVERALL SUMMARY: VALIDATION vs BENCHMARK")
    print("="*80)
    print()
    print(f"Total sets processed: {len(all_set_stats)}")
    print(f"Total videos analyzed: {len(all_results)}")
    total_comments = sum(r['predicted']['TOTAL'] for r in all_results)
    print(f"Total comments analyzed: {total_comments:,}")
    print()
    
    # Calculate overall aggregated distribution
    overall_total_pos = sum(r['predicted']['POSITIVE'] for r in all_results)
    overall_total_neg = sum(r['predicted']['NEGATIVE'] for r in all_results)
    overall_total_neu = sum(r['predicted']['NEUTRAL'] for r in all_results)
    overall_total_comments = overall_total_pos + overall_total_neg + overall_total_neu
    
    overall_validation_dist = {
        'POSITIVE': overall_total_pos,
        'NEGATIVE': overall_total_neg,
        'NEUTRAL': overall_total_neu,
        'TOTAL': overall_total_comments,
        'POSITIVE_PCT': (overall_total_pos / overall_total_comments * 100) if overall_total_comments > 0 else 0,
        'NEGATIVE_PCT': (overall_total_neg / overall_total_comments * 100) if overall_total_comments > 0 else 0,
        'NEUTRAL_PCT': (overall_total_neu / overall_total_comments * 100) if overall_total_comments > 0 else 0
    }
    
    overall_comparison = compare_with_benchmark(overall_validation_dist, BENCHMARK_INITIAL_DISTRIBUTION)
    
    print("Overall Aggregated Distribution:")
    print(f"  Validation (145 vídeos, {overall_total_comments:,} comentários):")
    print(f"    POSITIVE: {overall_validation_dist['POSITIVE_PCT']:.2f}% ({overall_total_pos:,} comentários)")
    print(f"    NEGATIVE: {overall_validation_dist['NEGATIVE_PCT']:.2f}% ({overall_total_neg:,} comentários)")
    print(f"    NEUTRAL:  {overall_validation_dist['NEUTRAL_PCT']:.2f}% ({overall_total_neu:,} comentários)")
    print()
    print(f"  Benchmark Inicial (206,445 comentários):")
    print(f"    POSITIVE: {BENCHMARK_INITIAL_DISTRIBUTION['POSITIVE_PCT']:.2f}% ({BENCHMARK_INITIAL_DISTRIBUTION['POSITIVE']:,} comentários)")
    print(f"    NEGATIVE: {BENCHMARK_INITIAL_DISTRIBUTION['NEGATIVE_PCT']:.2f}% ({BENCHMARK_INITIAL_DISTRIBUTION['NEGATIVE']:,} comentários)")
    print(f"    NEUTRAL:  {BENCHMARK_INITIAL_DISTRIBUTION['NEUTRAL_PCT']:.2f}% ({BENCHMARK_INITIAL_DISTRIBUTION['NEUTRAL']:,} comentários)")
    print()
    print("Differences (Validation - Benchmark):")
    print(f"  POSITIVE: {overall_comparison['percentage_differences']['POSITIVE']:+.2f}%")
    print(f"  NEGATIVE: {overall_comparison['percentage_differences']['NEGATIVE']:+.2f}%")
    print(f"  NEUTRAL:  {overall_comparison['percentage_differences']['NEUTRAL']:+.2f}%")
    print()
    print(f"Chi-square test (p-value): {overall_comparison['chi2_pvalue']:.6f}")
    if overall_comparison['distributions_similar']:
        print("  ✓ Distribuições são estatisticamente similares (p > 0.05)")
    else:
        print("  ✗ Distribuições são estatisticamente diferentes (p ≤ 0.05)")
    print()
    
    # Calculate overall differences across sets
    overall_diff_pos = np.mean([s['difference_from_benchmark']['POSITIVE']['mean'] for s in all_set_stats])
    overall_diff_neg = np.mean([s['difference_from_benchmark']['NEGATIVE']['mean'] for s in all_set_stats])
    overall_diff_neu = np.mean([s['difference_from_benchmark']['NEUTRAL']['mean'] for s in all_set_stats])
    
    overall_diff_pos_std = np.std([s['difference_from_benchmark']['POSITIVE']['mean'] for s in all_set_stats])
    overall_diff_neg_std = np.std([s['difference_from_benchmark']['NEGATIVE']['mean'] for s in all_set_stats])
    overall_diff_neu_std = np.std([s['difference_from_benchmark']['NEUTRAL']['mean'] for s in all_set_stats])
    
    # 95% Confidence Interval
    sem_pos = overall_diff_pos_std / np.sqrt(len(all_set_stats))
    sem_neg = overall_diff_neg_std / np.sqrt(len(all_set_stats))
    sem_neu = overall_diff_neu_std / np.sqrt(len(all_set_stats))
    
    ci95_pos = 1.96 * sem_pos
    ci95_neg = 1.96 * sem_neg
    ci95_neu = 1.96 * sem_neu
    
    print("Overall Differences (mean across sets ± 95% CI):")
    print(f"  POSITIVE: {overall_diff_pos:+.2f}% ± {ci95_pos:.2f}%")
    print(f"  NEGATIVE: {overall_diff_neg:+.2f}% ± {ci95_neg:.2f}%")
    print(f"  NEUTRAL:  {overall_diff_neu:+.2f}% ± {ci95_neu:.2f}%")
    print()
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    output_data = {
        'config': {
            'n_sets': N_SETS,
            'm_videos_per_set': M_VIDEOS_PER_SET,
            'min_comments': MIN_COMMENTS,
            'timestamp': timestamp
        },
        'benchmark_initial': BENCHMARK_INITIAL_DISTRIBUTION,
        'overall_validation_distribution': overall_validation_dist,
        'overall_comparison': overall_comparison,
        'set_statistics': all_set_stats,
        'overall_differences': {
            'POSITIVE': {
                'mean': overall_diff_pos,
                'std': overall_diff_pos_std,
                'ci95': ci95_pos
            },
            'NEGATIVE': {
                'mean': overall_diff_neg,
                'std': overall_diff_neg_std,
                'ci95': ci95_neg
            },
            'NEUTRAL': {
                'mean': overall_diff_neu,
                'std': overall_diff_neu_std,
                'ci95': ci95_neu
            }
        },
        'all_video_results': all_results
    }
    
    # Save in results directory
    os.makedirs('results', exist_ok=True)
    output_file = f'results/benchmark_comparison_results_{timestamp}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Detailed results saved: {output_file}")
    print()
    
    # Generate visualizations
    generate_comparison_graphs(all_set_stats, timestamp)
    
    print()
    print("="*80)
    print("VALIDATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()


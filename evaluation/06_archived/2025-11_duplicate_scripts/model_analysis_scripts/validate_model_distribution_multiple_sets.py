#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model Distribution Validation with Multiple Random Sets

This script validates model distribution bias using N random sets of M videos each.
This approach reduces selection bias and provides robust statistical evidence.

Strategy:
- Select N=10 random sets of M=30 videos each (300 unique videos total)
- For each set, compare ground truth vs predicted distributions
- Calculate aggregate statistics across all sets
- Generate consolidated visualizations
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

def compare_distributions(ground_truth_dist, predicted_dist):
    """Compare two distributions using chi-square test."""
    predicted_total = predicted_dist['TOTAL']
    ground_truth_total = ground_truth_dist['TOTAL']
    
    # Observed (predicted)
    observed = [
        predicted_dist['POSITIVE'],
        predicted_dist['NEGATIVE'],
        predicted_dist['NEUTRAL']
    ]
    
    # Expected (ground truth scaled to predicted total)
    expected = [
        (ground_truth_dist['POSITIVE'] / ground_truth_total) * predicted_total,
        (ground_truth_dist['NEGATIVE'] / ground_truth_total) * predicted_total,
        (ground_truth_dist['NEUTRAL'] / ground_truth_total) * predicted_total
    ]
    
    # Chi-square test
    chi2_stat, chi2_pval = chisquare(observed, expected)
    
    # Percentage differences
    pct_diff = {
        'POSITIVE': abs(predicted_dist['POSITIVE_PCT'] - ground_truth_dist['POSITIVE_PCT']),
        'NEGATIVE': abs(predicted_dist['NEGATIVE_PCT'] - ground_truth_dist['NEGATIVE_PCT']),
        'NEUTRAL': abs(predicted_dist['NEUTRAL_PCT'] - ground_truth_dist['NEUTRAL_PCT'])
    }
    
    # Bias (signed difference: predicted - ground_truth)
    bias = {
        'POSITIVE': predicted_dist['POSITIVE_PCT'] - ground_truth_dist['POSITIVE_PCT'],
        'NEGATIVE': predicted_dist['NEGATIVE_PCT'] - ground_truth_dist['NEGATIVE_PCT'],
        'NEUTRAL': predicted_dist['NEUTRAL_PCT'] - ground_truth_dist['NEUTRAL_PCT']
    }
    
    avg_diff = np.mean(list(pct_diff.values()))
    
    return {
        'chi2_statistic': chi2_stat,
        'chi2_pvalue': chi2_pval,
        'percentage_differences': pct_diff,
        'avg_percentage_difference': avg_diff,
        'bias': bias
    }

def process_video(video_data, df_ground_truth, verbose=False):
    """Process a single video and compare distributions."""
    video_id = video_data['id']
    video_title = video_data['title']
    
    if verbose:
        print(f"\n  Processing: {video_title[:60]}...")
    
    # Get ground truth distribution from dataset
    video_comments = df_ground_truth[df_ground_truth['VideoID'] == video_id]
    
    ground_truth_list = []
    for _, row in video_comments.iterrows():
        ground_truth_list.append({'sentiment': SENTIMENT_MAP[row['Sentiment']]})
    
    ground_truth_dist = get_distribution(ground_truth_list)
    
    # Fetch comments from API
    api_comments, error = fetch_comments_with_sentiment(video_id, max_results=500)
    
    if len(api_comments) == 0:
        if verbose:
            print(f"    ✗ Failed to fetch comments")
            if error:
                print(f"       Error: {error}")
        return {'error': error, 'video_id': video_id, 'video_title': video_title}
    
    predicted_dist = get_distribution(api_comments)
    
    # Statistical comparison
    comparison = compare_distributions(ground_truth_dist, predicted_dist)
    
    if verbose:
        print(f"    ✓ GT: {ground_truth_dist['POSITIVE_PCT']:.1f}% POS, {ground_truth_dist['NEGATIVE_PCT']:.1f}% NEG, {ground_truth_dist['NEUTRAL_PCT']:.1f}% NEU")
        print(f"    ✓ API: {predicted_dist['POSITIVE_PCT']:.1f}% POS, {predicted_dist['NEGATIVE_PCT']:.1f}% NEG, {predicted_dist['NEUTRAL_PCT']:.1f}% NEU")
        print(f"    ✓ Bias: {comparison['bias']['POSITIVE']:+.1f}% POS, {comparison['bias']['NEGATIVE']:+.1f}% NEG, {comparison['bias']['NEUTRAL']:+.1f}% NEU")
    
    return {
        'video_id': video_id,
        'video_title': video_title,
        'ground_truth': ground_truth_dist,
        'predicted': predicted_dist,
        'comparison': comparison
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
    """Calculate aggregate statistics for a set."""
    if len(set_results) == 0:
        return None
    
    # Extract biases
    biases_pos = [r['comparison']['bias']['POSITIVE'] for r in set_results]
    biases_neg = [r['comparison']['bias']['NEGATIVE'] for r in set_results]
    biases_neu = [r['comparison']['bias']['NEUTRAL'] for r in set_results]
    
    # Extract ground truth and predicted percentages
    gt_pos = [r['ground_truth']['POSITIVE_PCT'] for r in set_results]
    gt_neg = [r['ground_truth']['NEGATIVE_PCT'] for r in set_results]
    gt_neu = [r['ground_truth']['NEUTRAL_PCT'] for r in set_results]
    
    pred_pos = [r['predicted']['POSITIVE_PCT'] for r in set_results]
    pred_neg = [r['predicted']['NEGATIVE_PCT'] for r in set_results]
    pred_neu = [r['predicted']['NEUTRAL_PCT'] for r in set_results]
    
    # Chi-square p-values
    chi2_pvalues = [r['comparison']['chi2_pvalue'] for r in set_results]
    
    return {
        'n_videos': len(set_results),
        'bias': {
            'POSITIVE': {'mean': np.mean(biases_pos), 'std': np.std(biases_pos)},
            'NEGATIVE': {'mean': np.mean(biases_neg), 'std': np.std(biases_neg)},
            'NEUTRAL': {'mean': np.mean(biases_neu), 'std': np.std(biases_neu)}
        },
        'ground_truth': {
            'POSITIVE': {'mean': np.mean(gt_pos), 'std': np.std(gt_pos)},
            'NEGATIVE': {'mean': np.mean(gt_neg), 'std': np.std(gt_neg)},
            'NEUTRAL': {'mean': np.mean(gt_neu), 'std': np.std(gt_neu)}
        },
        'predicted': {
            'POSITIVE': {'mean': np.mean(pred_pos), 'std': np.std(pred_pos)},
            'NEGATIVE': {'mean': np.mean(pred_neg), 'std': np.std(pred_neg)},
            'NEUTRAL': {'mean': np.mean(pred_neu), 'std': np.std(pred_neu)}
        },
        'chi2_pvalue_mean': np.mean(chi2_pvalues),
        'chi2_pvalue_std': np.std(chi2_pvalues),
        'similar_distributions_count': sum(1 for p in chi2_pvalues if p > 0.05)
    }

def generate_consolidated_graphs(all_set_stats, timestamp):
    """Generate consolidated visualizations across all sets."""
    print("\n" + "="*80)
    print("GENERATING CONSOLIDATED VISUALIZATIONS")
    print("="*80)
    
    n_sets = len(all_set_stats)
    
    # Extract data for plotting
    set_indices = list(range(1, n_sets + 1))
    
    bias_pos_means = [s['bias']['POSITIVE']['mean'] for s in all_set_stats]
    bias_neg_means = [s['bias']['NEGATIVE']['mean'] for s in all_set_stats]
    bias_neu_means = [s['bias']['NEUTRAL']['mean'] for s in all_set_stats]
    
    bias_pos_stds = [s['bias']['POSITIVE']['std'] for s in all_set_stats]
    bias_neg_stds = [s['bias']['NEGATIVE']['std'] for s in all_set_stats]
    bias_neu_stds = [s['bias']['NEUTRAL']['std'] for s in all_set_stats]
    
    # ============================================================================
    # GRAPH 1: Bias across sets with error bars
    # ============================================================================
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    x = np.arange(n_sets)
    width = 0.25
    
    bars1 = ax.bar(x - width, bias_pos_means, width, label='POSITIVE', 
                   yerr=bias_pos_stds, capsize=5, color='#4CAF50', 
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    bars2 = ax.bar(x, bias_neg_means, width, label='NEGATIVE',
                   yerr=bias_neg_stds, capsize=5, color='#F44336',
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    bars3 = ax.bar(x + width, bias_neu_means, width, label='NEUTRAL',
                   yerr=bias_neu_stds, capsize=5, color='#FF9800',
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Add zero line
    ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='Sem Viés (0%)')
    
    ax.set_xlabel('Conjunto de Vídeos', fontsize=13, fontweight='bold')
    ax.set_ylabel('Viés Médio (Predição - Ground Truth, %)', fontsize=13, fontweight='bold')
    ax.set_title(f'Viés do Modelo por Conjunto de Vídeos (N={n_sets} conjuntos, M=30 vídeos cada)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels([f'Set {i}' for i in set_indices])
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    output_file = f'multiple_sets_bias_by_set_{timestamp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()
    
    # ============================================================================
    # GRAPH 2: Overall average bias with 95% CI
    # ============================================================================
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Calculate overall statistics
    overall_bias_pos = np.mean(bias_pos_means)
    overall_bias_neg = np.mean(bias_neg_means)
    overall_bias_neu = np.mean(bias_neu_means)
    
    # 95% CI = 1.96 * SEM (Standard Error of Mean)
    sem_pos = np.std(bias_pos_means) / np.sqrt(n_sets)
    sem_neg = np.std(bias_neg_means) / np.sqrt(n_sets)
    sem_neu = np.std(bias_neu_means) / np.sqrt(n_sets)
    
    ci95_pos = 1.96 * sem_pos
    ci95_neg = 1.96 * sem_neg
    ci95_neu = 1.96 * sem_neu
    
    categories = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
    means = [overall_bias_pos, overall_bias_neg, overall_bias_neu]
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
    ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='Sem Viés (0%)')
    
    ax.set_ylabel('Viés Médio (Predição - Ground Truth, %)', fontsize=13, fontweight='bold')
    ax.set_title(f'Viés Sistemático do Modelo TF-IDF + Logistic Regression\n(N={n_sets} conjuntos × M=30 vídeos = {n_sets*30} vídeos analisados, IC 95%)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add annotation box
    textstr = f'''Interpretação:
• NEUTRAL: Viés POSITIVO de {overall_bias_neu:+.2f}% ± {ci95_neu:.2f}%
  (modelo superestima classificação neutra)
• NEGATIVE: Viés NEGATIVO de {overall_bias_neg:+.2f}% ± {ci95_neg:.2f}%
  (modelo subestima classificação negativa)
• POSITIVE: Viés de {overall_bias_pos:+.2f}% ± {ci95_pos:.2f}%
  (relativamente balanceado)'''
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)
    ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', horizontalalignment='right', bbox=props)
    
    plt.tight_layout()
    output_file = f'multiple_sets_overall_bias_ci95_{timestamp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()
    
    # ============================================================================
    # GRAPH 3: Distribution of bias across all sets (boxplot)
    # ============================================================================
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    bias_data = [bias_pos_means, bias_neg_means, bias_neu_means]
    
    bp = ax.boxplot(bias_data, labels=categories, patch_artist=True,
                    widths=0.6, showmeans=True, meanline=True,
                    boxprops=dict(linewidth=2),
                    whiskerprops=dict(linewidth=2),
                    capprops=dict(linewidth=2),
                    medianprops=dict(color='black', linewidth=3),
                    meanprops=dict(color='blue', linewidth=3, linestyle='--'))
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Add zero line
    ax.axhline(y=0, color='red', linestyle='--', linewidth=2, label='Sem Viés (0%)')
    
    # Add individual points
    for i, data in enumerate(bias_data, 1):
        y = data
        x = np.random.normal(i, 0.04, size=len(y))
        ax.plot(x, y, 'o', alpha=0.5, markersize=8, color='darkblue')
    
    ax.set_ylabel('Viés (Predição - Ground Truth, %)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Sentimento', fontsize=13, fontweight='bold')
    ax.set_title(f'Distribuição do Viés entre {n_sets} Conjuntos de Vídeos\n(cada ponto = média de um conjunto de 30 vídeos)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    output_file = f'multiple_sets_bias_distribution_{timestamp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

def main():
    print("="*80)
    print("MODEL DISTRIBUTION VALIDATION WITH MULTIPLE RANDOM SETS")
    print("="*80)
    print()
    print(f"Configuration:")
    print(f"  Number of sets (N): {N_SETS}")
    print(f"  Videos per set (M): {M_VIDEOS_PER_SET}")
    print(f"  Total videos: {N_SETS * M_VIDEOS_PER_SET}")
    print(f"  Minimum comments per video: {MIN_COMMENTS}")
    print()
    print(f"Starting validation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load ground truth dataset
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
            print(f"    Bias POSITIVE: {set_stats['bias']['POSITIVE']['mean']:+.2f}% ± {set_stats['bias']['POSITIVE']['std']:.2f}%")
            print(f"    Bias NEGATIVE: {set_stats['bias']['NEGATIVE']['mean']:+.2f}% ± {set_stats['bias']['NEGATIVE']['std']:.2f}%")
            print(f"    Bias NEUTRAL:  {set_stats['bias']['NEUTRAL']['mean']:+.2f}% ± {set_stats['bias']['NEUTRAL']['std']:.2f}%")
    
    # Overall summary
    print("\n" + "="*80)
    print("OVERALL SUMMARY ACROSS ALL SETS")
    print("="*80)
    print()
    print(f"Total sets processed: {len(all_set_stats)}")
    print(f"Total videos analyzed: {len(all_results)}")
    print()
    
    # Calculate overall statistics
    overall_bias_pos_mean = np.mean([s['bias']['POSITIVE']['mean'] for s in all_set_stats])
    overall_bias_neg_mean = np.mean([s['bias']['NEGATIVE']['mean'] for s in all_set_stats])
    overall_bias_neu_mean = np.mean([s['bias']['NEUTRAL']['mean'] for s in all_set_stats])
    
    overall_bias_pos_std = np.std([s['bias']['POSITIVE']['mean'] for s in all_set_stats])
    overall_bias_neg_std = np.std([s['bias']['NEGATIVE']['mean'] for s in all_set_stats])
    overall_bias_neu_std = np.std([s['bias']['NEUTRAL']['mean'] for s in all_set_stats])
    
    # 95% Confidence Interval
    sem_pos = overall_bias_pos_std / np.sqrt(len(all_set_stats))
    sem_neg = overall_bias_neg_std / np.sqrt(len(all_set_stats))
    sem_neu = overall_bias_neu_std / np.sqrt(len(all_set_stats))
    
    ci95_pos = 1.96 * sem_pos
    ci95_neg = 1.96 * sem_neg
    ci95_neu = 1.96 * sem_neu
    
    print("Overall Bias (mean across sets ± 95% CI):")
    print(f"  POSITIVE: {overall_bias_pos_mean:+.2f}% ± {ci95_pos:.2f}%")
    print(f"  NEGATIVE: {overall_bias_neg_mean:+.2f}% ± {ci95_neg:.2f}%")
    print(f"  NEUTRAL:  {overall_bias_neu_mean:+.2f}% ± {ci95_neu:.2f}%")
    print()
    
    print("Inter-set variability (std of set means):")
    print(f"  POSITIVE: σ = {overall_bias_pos_std:.2f}%")
    print(f"  NEGATIVE: σ = {overall_bias_neg_std:.2f}%")
    print(f"  NEUTRAL:  σ = {overall_bias_neu_std:.2f}%")
    print()
    
    # Error analysis
    if len(all_errors) > 0:
        print("="*80)
        print("ERROR ANALYSIS")
        print("="*80)
        print()
        print(f"Total failed videos: {len(all_errors)}")
        print(f"Success rate: {len(all_results)/(len(all_results)+len(all_errors))*100:.1f}%")
        print()
        
        # Count error types
        error_types = {}
        for err in all_errors:
            error_msg = err.get('error', 'Unknown error')
            # Extract error type
            if '502' in error_msg:
                error_type = 'HTTP 502 Bad Gateway'
            elif '503' in error_msg:
                error_type = 'HTTP 503 Service Unavailable'
            elif '504' in error_msg:
                error_type = 'HTTP 504 Gateway Timeout'
            elif '403' in error_msg:
                error_type = 'HTTP 403 Forbidden'
            elif '404' in error_msg:
                error_type = 'HTTP 404 Not Found'
            elif 'timeout' in error_msg.lower():
                error_type = 'Request Timeout'
            else:
                error_type = 'Other'
            
            if error_type not in error_types:
                error_types[error_type] = []
            error_types[error_type].append(err)
        
        print("Error types:")
        for error_type, errors in sorted(error_types.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  {error_type}: {len(errors)} ({len(errors)/len(all_errors)*100:.1f}%)")
        
        print()
        print("Sample of failed videos:")
        for i, err in enumerate(all_errors[:10], 1):
            print(f"  {i}. {err.get('video_title', 'Unknown')[:60]}")
            print(f"     VideoID: {err.get('video_id', 'Unknown')}")
            print(f"     Error: {err.get('error', 'Unknown')[:80]}")
        
        if len(all_errors) > 10:
            print(f"  ... and {len(all_errors) - 10} more")
        print()
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save detailed results
    output_data = {
        'config': {
            'n_sets': N_SETS,
            'm_videos_per_set': M_VIDEOS_PER_SET,
            'min_comments': MIN_COMMENTS,
            'timestamp': timestamp
        },
        'set_statistics': all_set_stats,
        'overall_statistics': {
            'bias': {
                'POSITIVE': {
                    'mean': overall_bias_pos_mean,
                    'std': overall_bias_pos_std,
                    'ci95': ci95_pos
                },
                'NEGATIVE': {
                    'mean': overall_bias_neg_mean,
                    'std': overall_bias_neg_std,
                    'ci95': ci95_neg
                },
                'NEUTRAL': {
                    'mean': overall_bias_neu_mean,
                    'std': overall_bias_neu_std,
                    'ci95': ci95_neu
                }
            }
        },
        'all_video_results': all_results
    }
    
    # Save in results directory
    os.makedirs('results', exist_ok=True)
    output_file = f'results/multiple_sets_validation_results_{timestamp}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Detailed results saved: {output_file}")
    print()
    
    # Generate visualizations
    generate_consolidated_graphs(all_set_stats, timestamp)
    
    print()
    print("="*80)
    print("VALIDATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model Distribution Validation

This script validates if the sentiment distribution predicted by the model
follows the same statistical pattern as the ground truth dataset.

Instead of matching individual comments, we compare:
- Ground Truth Distribution: % POSITIVE, % NEGATIVE, % NEUTRAL
- API Predicted Distribution: % POSITIVE, % NEGATIVE, % NEUTRAL

If distributions are similar, the model generalizes well!
"""

import requests
import pandas as pd
import json
import time
import os
from datetime import datetime
from scipy.stats import chisquare, ks_2samp
import numpy as np
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
    
    for attempt in range(retries):
        try:
            print(f"    Attempt {attempt + 1}/{retries}...", end=" ")
            response = requests.get(endpoint, params=params, timeout=60)
            response.raise_for_status()
            print(f"✓ Success - {len(response.json().get('items', []))} comments")
            return response.json().get('items', [])
        except requests.exceptions.RequestException as e:
            print(f"✗ Error: {e}")
            time.sleep(2)
    return []

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
    """
    Compare two distributions using statistical tests.
    
    Returns:
    - chi2_statistic: Chi-square test statistic
    - chi2_pvalue: Chi-square p-value (>0.05 = distributions are similar)
    - percentage_difference: Absolute difference in percentages
    """
    # Use percentages for chi-square test (normalize to same scale)
    # Scale ground truth to predicted total
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
    
    avg_diff = np.mean(list(pct_diff.values()))
    
    return {
        'chi2_statistic': chi2_stat,
        'chi2_pvalue': chi2_pval,
        'percentage_differences': pct_diff,
        'avg_percentage_difference': avg_diff
    }

def visualize_comparison(video_title, ground_truth_dist, predicted_dist, output_file):
    """Generate comparison visualization."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Data
    categories = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
    ground_truth_pcts = [
        ground_truth_dist['POSITIVE_PCT'],
        ground_truth_dist['NEGATIVE_PCT'],
        ground_truth_dist['NEUTRAL_PCT']
    ]
    predicted_pcts = [
        predicted_dist['POSITIVE_PCT'],
        predicted_dist['NEGATIVE_PCT'],
        predicted_dist['NEUTRAL_PCT']
    ]
    
    colors = ['#4CAF50', '#F44336', '#FF9800']
    
    # Ground Truth
    ax1.bar(categories, ground_truth_pcts, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Percentual (%)', fontsize=12, fontweight='bold')
    ax1.set_title(f'Ground Truth (Dataset)\n{ground_truth_dist["TOTAL"]} comentários', fontsize=13, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    for i, (cat, pct) in enumerate(zip(categories, ground_truth_pcts)):
        ax1.text(i, pct + 2, f'{pct:.1f}%', ha='center', fontsize=11, fontweight='bold')
    
    # Predicted
    ax2.bar(categories, predicted_pcts, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Percentual (%)', fontsize=12, fontweight='bold')
    ax2.set_title(f'Predição do Modelo (API)\n{predicted_dist["TOTAL"]} comentários', fontsize=13, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    for i, (cat, pct) in enumerate(zip(categories, predicted_pcts)):
        ax2.text(i, pct + 2, f'{pct:.1f}%', ha='center', fontsize=11, fontweight='bold')
    
    fig.suptitle(f'Comparação de Distribuição de Sentimentos\n{video_title}', 
                 fontsize=15, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Visualization saved: {output_file}")

def process_video(video_data, df_ground_truth):
    """Process a single video and compare distributions."""
    video_id = video_data['id']
    video_title = video_data['title']
    
    print(f"\n{'='*80}")
    print(f"Video: {video_title}")
    print(f"VideoID: {video_id}")
    print(f"{'='*80}")
    
    # Get ground truth distribution from dataset
    video_comments = df_ground_truth[df_ground_truth['VideoID'] == video_id]
    
    ground_truth_list = []
    for _, row in video_comments.iterrows():
        ground_truth_list.append({'sentiment': SENTIMENT_MAP[row['Sentiment']]})
    
    ground_truth_dist = get_distribution(ground_truth_list)
    
    print(f"\n  Ground Truth Distribution:")
    print(f"    POSITIVE: {ground_truth_dist['POSITIVE']} ({ground_truth_dist['POSITIVE_PCT']:.1f}%)")
    print(f"    NEGATIVE: {ground_truth_dist['NEGATIVE']} ({ground_truth_dist['NEGATIVE_PCT']:.1f}%)")
    print(f"    NEUTRAL:  {ground_truth_dist['NEUTRAL']} ({ground_truth_dist['NEUTRAL_PCT']:.1f}%)")
    print(f"    TOTAL:    {ground_truth_dist['TOTAL']}")
    
    # Fetch comments from API
    print(f"\n  Fetching comments from API...")
    api_comments = fetch_comments_with_sentiment(video_id, max_results=500)
    
    if len(api_comments) == 0:
        print("  ✗ Failed to fetch comments")
        return None
    
    predicted_dist = get_distribution(api_comments)
    
    print(f"\n  API Predicted Distribution:")
    print(f"    POSITIVE: {predicted_dist['POSITIVE']} ({predicted_dist['POSITIVE_PCT']:.1f}%)")
    print(f"    NEGATIVE: {predicted_dist['NEGATIVE']} ({predicted_dist['NEGATIVE_PCT']:.1f}%)")
    print(f"    NEUTRAL:  {predicted_dist['NEUTRAL']} ({predicted_dist['NEUTRAL_PCT']:.1f}%)")
    print(f"    TOTAL:    {predicted_dist['TOTAL']}")
    
    # Statistical comparison
    comparison = compare_distributions(ground_truth_dist, predicted_dist)
    
    print(f"\n  Statistical Comparison:")
    print(f"    Chi-square statistic: {comparison['chi2_statistic']:.4f}")
    print(f"    Chi-square p-value:   {comparison['chi2_pvalue']:.4f}", end="")
    
    if comparison['chi2_pvalue'] > 0.05:
        print(" ✓ (distributions are similar)")
    else:
        print(" ✗ (distributions differ significantly)")
    
    print(f"\n  Percentage Differences:")
    print(f"    POSITIVE: {comparison['percentage_differences']['POSITIVE']:.2f}%")
    print(f"    NEGATIVE: {comparison['percentage_differences']['NEGATIVE']:.2f}%")
    print(f"    NEUTRAL:  {comparison['percentage_differences']['NEUTRAL']:.2f}%")
    print(f"    Average:  {comparison['avg_percentage_difference']:.2f}%")
    
    # Generate visualization
    output_file = f"distribution_comparison_{video_id}.png"
    visualize_comparison(video_title, ground_truth_dist, predicted_dist, output_file)
    
    return {
        'video_id': video_id,
        'video_title': video_title,
        'ground_truth': ground_truth_dist,
        'predicted': predicted_dist,
        'comparison': comparison,
        'visualization': output_file
    }

def main():
    print("="*80)
    print("MODEL DISTRIBUTION VALIDATION")
    print("="*80)
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
    print()
    
    # Load video list
    video_file = 'dataset_videos_20_for_validation.json'
    print(f"Loading videos from: {video_file}")
    with open(video_file, 'r') as f:
        videos = json.load(f)
    
    print(f"Testing {len(videos)} videos from dataset")
    print()
    
    results = []
    successful = 0
    
    for i, video in enumerate(videos, 1):
        print(f"\n{'='*80}")
        print(f"Video {i}/{len(videos)}")
        print(f"{'='*80}")
        
        result = process_video(video, df)
        
        if result:
            results.append(result)
            successful += 1
        
        # Rate limiting
        if i < len(videos):
            print("\n  Waiting 2 seconds...")
            time.sleep(2)
    
    # Summary
    print("\n" + "="*80)
    print("OVERALL VALIDATION RESULTS")
    print("="*80)
    print()
    print(f"Videos tested: {successful}/{len(videos)}")
    print()
    
    if successful > 0:
        # Calculate average metrics
        avg_chi2_pval = np.mean([r['comparison']['chi2_pvalue'] for r in results])
        avg_pct_diff = np.mean([r['comparison']['avg_percentage_difference'] for r in results])
        
        similar_count = sum(1 for r in results if r['comparison']['chi2_pvalue'] > 0.05)
        
        print(f"Average Chi-square p-value: {avg_chi2_pval:.4f}")
        print(f"Average percentage difference: {avg_pct_diff:.2f}%")
        print(f"Videos with similar distributions (p>0.05): {similar_count}/{successful}")
        print()
        
        # Save detailed results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'distribution_validation_results_{timestamp}.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Detailed results saved: {output_file}")
    else:
        print("❌ No successful validations")
    
    print()
    print("="*80)
    print("VALIDATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()


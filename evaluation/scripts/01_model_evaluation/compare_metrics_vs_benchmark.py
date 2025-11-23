#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparação de Métricas: Validação vs Benchmark Inicial

Este script compara as métricas básicas do modelo (Acurácia, Precisão, F1-Score)
observadas na validação atual (145 vídeos, ~72.500 comentários) com as métricas
observadas no benchmark inicial quando o modelo foi selecionado.

Objetivo: Verificar se o modelo mantém as métricas de desempenho (accuracy, precision, F1)
quando aplicado a vídeos diferentes dos usados no benchmark inicial.
"""

import requests
import pandas as pd
import json
import time
import os
import re
from datetime import datetime
from difflib import SequenceMatcher
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# API configuration
API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod"

# Dataset path - tenta api_load_testing primeiro, depois local
DATASET_PATH = '../api_load_testing/youtube_comments_cleaned.csv'
if not os.path.exists(DATASET_PATH):
    DATASET_PATH = 'youtube_comments_cleaned.csv'

# Benchmark Initial Metrics (from test set)
BENCHMARK_METRICS = {
    'accuracy': 0.6614,    # 66.14%
    'precision': 0.6664,   # 66.64% (weighted average)
    'recall': 0.6614,      # 66.14% (weighted average)
    'f1_score': 0.6628     # 66.28%
}

# Sentiment mapping
SENTIMENT_MAP = {
    'Positive': 'POSITIVE',
    'Negative': 'NEGATIVE',
    'Neutral': 'NEUTRAL'
}

# Configuration
N_SETS = 5  # Number of random sets
M_VIDEOS_PER_SET = 29  # Videos per set (145 / 5 = 29)
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

def normalize_text(text):
    """Normalize text for better matching."""
    if not text:
        return ""
    # Convert to lowercase
    text = str(text).lower()
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?]', '', text)
    # Normalize multiple spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def load_ground_truth(video_id, df_dataset):
    """Load ground truth labels from dataset for a video."""
    video_df = df_dataset[df_dataset['VideoID'] == video_id].copy()
    
    # Create mapping of normalized comment text to sentiment
    ground_truth = {}
    for _, row in video_df.iterrows():
        text = normalize_text(row['CommentText'])
        if text:  # Only add non-empty texts
            sentiment = SENTIMENT_MAP.get(row['Sentiment'], 'UNKNOWN')
            # Store both original and normalized for flexibility
            ground_truth[text] = sentiment
    
    return ground_truth

def find_best_match(text, ground_truth_dict, threshold=0.85):
    """Find best matching comment in ground truth using similarity."""
    normalized = normalize_text(text)
    
    # First try exact match
    if normalized in ground_truth_dict:
        return ground_truth_dict[normalized], normalized
    
    # Try fuzzy matching if exact match fails
    best_match = None
    best_ratio = 0
    
    for gt_text in ground_truth_dict.keys():
        ratio = SequenceMatcher(None, normalized, gt_text).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = gt_text
    
    # Only return if similarity is above threshold
    if best_ratio >= threshold:
        return ground_truth_dict[best_match], best_match
    
    return None, None

def validate_video(video_data, df_dataset, verbose=False):
    """Validate model predictions for a single video and calculate metrics."""
    video_id = video_data['id']
    video_title = video_data['title']
    
    if verbose:
        print(f"\n  Processing: {video_title[:60]}...")
    
    # Fetch predictions from API (increase to get more comments)
    api_comments, error = fetch_comments_with_sentiment(video_id, max_results=1000)
    
    if len(api_comments) == 0:
        if verbose:
            print(f"    ✗ Failed to fetch comments: {error}")
        return {'error': error, 'video_id': video_id, 'video_title': video_title}
    
    # Load ground truth
    ground_truth = load_ground_truth(video_id, df_dataset)
    
    if len(ground_truth) == 0:
        if verbose:
            print(f"    ✗ No ground truth found in dataset")
        return {'error': 'No ground truth', 'video_id': video_id, 'video_title': video_title}
    
    # Match predictions with ground truth (improved matching)
    y_true = []
    y_pred = []
    matched = 0
    exact_matches = 0
    fuzzy_matches = 0
    
    for comment in api_comments:
        # Get comment text from API response
        text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
        predicted = comment.get('sentiment', 'UNKNOWN')
        
        # Find best match (exact or fuzzy)
        true_label, matched_text = find_best_match(text, ground_truth)
        
        if true_label:
            y_true.append(true_label)
            y_pred.append(predicted)
            matched += 1
            if normalize_text(text) == matched_text:
                exact_matches += 1
            else:
                fuzzy_matches += 1
    
    if len(y_true) < 5:  # Reduced threshold to allow more videos
        if verbose:
            print(f"    ✗ Too few matches ({len(y_true)}/{len(api_comments)}) - skipping")
        return {'error': 'Too few matches', 'video_id': video_id, 'video_title': video_title}
    
    # Calculate metrics
    labels = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    
    if verbose:
        print(f"    ✓ Matched {matched}/{len(api_comments)} comments ({exact_matches} exact, {fuzzy_matches} fuzzy)")
        print(f"    ✓ Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"    ✓ Precision: {precision:.4f}")
        print(f"    ✓ Recall: {recall:.4f}")
        print(f"    ✓ F1-Score: {f1:.4f}")
    
    return {
        'video_id': video_id,
        'video_title': video_title,
        'total_matched': len(y_true),
        'total_api_comments': len(api_comments),
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'y_true': y_true,
        'y_pred': y_pred
    }

def select_video_sets(n_sets, m_videos_per_set, working_videos_file):
    """Select N random sets of M videos each from pre-filtered working videos."""
    print(f"\nSelecting {n_sets} random sets of {m_videos_per_set} videos each...")
    
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

def process_set(set_idx, videos, df_dataset):
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
        result = validate_video(video, df_dataset, verbose=True)
        
        if result and 'error' in result:
            errors.append(result)
            failed += 1
        elif result:
            results.append(result)
            successful += 1
        else:
            failed += 1
        
        # Rate limiting
        if i < len(videos):
            time.sleep(2)
    
    print(f"\n  Set {set_idx + 1} Summary: {successful} successful, {failed} failed")
    
    return results, errors

def calculate_aggregate_metrics(results):
    """Calculate aggregate metrics across all results."""
    if len(results) == 0:
        return None
    
    # Aggregate all predictions and labels
    all_y_true = []
    all_y_pred = []
    
    for result in results:
        all_y_true.extend(result['y_true'])
        all_y_pred.extend(result['y_pred'])
    
    if len(all_y_true) == 0:
        return None
    
    # Calculate overall metrics
    labels = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
    accuracy = accuracy_score(all_y_true, all_y_pred)
    precision = precision_score(all_y_true, all_y_pred, labels=labels, average='weighted', zero_division=0)
    recall = recall_score(all_y_true, all_y_pred, labels=labels, average='weighted', zero_division=0)
    f1 = f1_score(all_y_true, all_y_pred, labels=labels, average='weighted', zero_division=0)
    
    return {
        'total_comments': len(all_y_true),
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1)
    }

def compare_with_benchmark(validation_metrics, benchmark_metrics):
    """Compare validation metrics with benchmark metrics."""
    differences = {
        'accuracy': validation_metrics['accuracy'] - benchmark_metrics['accuracy'],
        'precision': validation_metrics['precision'] - benchmark_metrics['precision'],
        'recall': validation_metrics['recall'] - benchmark_metrics['recall'],
        'f1_score': validation_metrics['f1_score'] - benchmark_metrics['f1_score']
    }
    
    # Calculate relative differences (%)
    relative_diff = {
        'accuracy': (differences['accuracy'] / benchmark_metrics['accuracy']) * 100,
        'precision': (differences['precision'] / benchmark_metrics['precision']) * 100,
        'recall': (differences['recall'] / benchmark_metrics['recall']) * 100,
        'f1_score': (differences['f1_score'] / benchmark_metrics['f1_score']) * 100
    }
    
    # Check if metrics are similar (within 5% difference)
    similar = {
        'accuracy': abs(relative_diff['accuracy']) <= 5.0,
        'precision': abs(relative_diff['precision']) <= 5.0,
        'recall': abs(relative_diff['recall']) <= 5.0,
        'f1_score': abs(relative_diff['f1_score']) <= 5.0
    }
    
    return {
        'differences': differences,
        'relative_differences_pct': relative_diff,
        'similar': similar
    }

def main():
    print("="*80)
    print("COMPARAÇÃO DE MÉTRICAS: VALIDAÇÃO vs BENCHMARK INICIAL")
    print("="*80)
    print()
    print("Objetivo: Verificar se o modelo mantém as métricas de desempenho")
    print("          (Accuracy, Precision, F1-Score) quando aplicado a vídeos")
    print("          diferentes dos usados no benchmark inicial.")
    print()
    print("Benchmark Inicial (test set):")
    print(f"  Accuracy:  {BENCHMARK_METRICS['accuracy']:.4f} ({BENCHMARK_METRICS['accuracy']*100:.2f}%)")
    print(f"  Precision: {BENCHMARK_METRICS['precision']:.4f} ({BENCHMARK_METRICS['precision']*100:.2f}%)")
    print(f"  Recall:    {BENCHMARK_METRICS['recall']:.4f} ({BENCHMARK_METRICS['recall']*100:.2f}%)")
    print(f"  F1-Score:  {BENCHMARK_METRICS['f1_score']:.4f} ({BENCHMARK_METRICS['f1_score']*100:.2f}%)")
    print()
    print(f"Configuration:")
    print(f"  Number of sets (N): {N_SETS}")
    print(f"  Videos per set (M): {M_VIDEOS_PER_SET}")
    print(f"  Total videos: {N_SETS * M_VIDEOS_PER_SET}")
    print()
    print(f"Starting validation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load dataset
    print("Loading ground truth dataset...")
    df = pd.read_csv(DATASET_PATH, low_memory=False)
    print(f"✓ Loaded {len(df)} comments from dataset")
    
    # Select N random sets of M videos each from pre-filtered working videos
    video_sets = select_video_sets(N_SETS, M_VIDEOS_PER_SET, WORKING_VIDEOS_FILE)
    
    # Process each set
    all_results = []
    all_errors = []
    all_set_metrics = []
    
    for i, video_set in enumerate(video_sets):
        set_results, set_errors = process_set(i, video_set, df)
        
        all_errors.extend(set_errors)
        
        if len(set_results) > 0:
            set_metrics = calculate_aggregate_metrics(set_results)
            if set_metrics:
                all_set_metrics.append(set_metrics)
                all_results.extend(set_results)
                
                set_comparison = compare_with_benchmark(set_metrics, BENCHMARK_METRICS)
                
                print(f"\n  Set {i+1} Metrics:")
                print(f"    Comments: {set_metrics['total_comments']:,}")
                print(f"    Accuracy:  {set_metrics['accuracy']:.4f} ({set_metrics['accuracy']*100:.2f}%)")
                print(f"    Precision: {set_metrics['precision']:.4f} ({set_metrics['precision']*100:.2f}%)")
                print(f"    Recall:    {set_metrics['recall']:.4f} ({set_metrics['recall']*100:.2f}%)")
                print(f"    F1-Score:  {set_metrics['f1_score']:.4f} ({set_metrics['f1_score']*100:.2f}%)")
                print(f"    Differences vs Benchmark:")
                print(f"      Accuracy:  {set_comparison['differences']['accuracy']:+.4f} ({set_comparison['relative_differences_pct']['accuracy']:+.2f}%)")
                print(f"      Precision: {set_comparison['differences']['precision']:+.4f} ({set_comparison['relative_differences_pct']['precision']:+.2f}%)")
                print(f"      Recall:    {set_comparison['differences']['recall']:+.4f} ({set_comparison['relative_differences_pct']['recall']:+.2f}%)")
                print(f"      F1-Score:  {set_comparison['differences']['f1_score']:+.4f} ({set_comparison['relative_differences_pct']['f1_score']:+.2f}%)")
    
    # Overall summary
    print("\n" + "="*80)
    print("OVERALL SUMMARY: VALIDATION vs BENCHMARK")
    print("="*80)
    print()
    
    if len(all_results) == 0:
        print("❌ No successful validations - cannot compare metrics")
        return
    
    # Calculate overall aggregate metrics
    overall_metrics = calculate_aggregate_metrics(all_results)
    overall_comparison = compare_with_benchmark(overall_metrics, BENCHMARK_METRICS)
    
    print(f"Total videos analyzed: {len(all_results)}")
    print(f"Total comments analyzed: {overall_metrics['total_comments']:,}")
    print()
    
    print("=" * 60)
    print("MÉTRICAS - BENCHMARK vs VALIDAÇÃO")
    print("=" * 60)
    print()
    print(f"{'Métrica':<12} {'Benchmark':<12} {'Validação':<12} {'Diferença':<12} {'Status':<15}")
    print("-" * 60)
    
    metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    metrics_keys = ['accuracy', 'precision', 'recall', 'f1_score']
    
    for name, key in zip(metrics_names, metrics_keys):
        bench_val = BENCHMARK_METRICS[key]
        valid_val = overall_metrics[key]
        diff = overall_comparison['differences'][key]
        rel_diff = overall_comparison['relative_differences_pct'][key]
        similar = overall_comparison['similar'][key]
        status = "✓ Similar" if similar else "⚠ Diferente"
        
        print(f"{name:<12} {bench_val:>11.2%} {valid_val:>11.2%} {diff:>+11.4f} ({rel_diff:>+5.2f}%) {status:<15}")
    
    print()
    print("=" * 60)
    print("CONCLUSÃO")
    print("=" * 60)
    
    all_similar = all(overall_comparison['similar'].values())
    if all_similar:
        print("✅ O modelo MANTÉM as métricas do benchmark inicial.")
        print("   Todas as métricas estão dentro de 5% de diferença relativa.")
    else:
        print("⚠️  O modelo NÃO mantém todas as métricas do benchmark inicial.")
        print("   Algumas métricas diferem em mais de 5%.")
        print()
        print("Métricas que diferem:")
        for name, key in zip(metrics_names, metrics_keys):
            if not overall_comparison['similar'][key]:
                rel_diff = overall_comparison['relative_differences_pct'][key]
                print(f"  - {name}: {rel_diff:+.2f}% de diferença")
    
    print()
    
    # Calculate statistics across sets
    if len(all_set_metrics) > 1:
        print("=" * 60)
        print("VARIABILIDADE ENTRE CONJUNTOS")
        print("=" * 60)
        print()
        
        import numpy as np
        
        for name, key in zip(metrics_names, metrics_keys):
            set_values = [s[key] for s in all_set_metrics]
            mean_val = np.mean(set_values)
            std_val = np.std(set_values)
            
            print(f"{name}:")
            print(f"  Média: {mean_val:.4f} ({mean_val*100:.2f}%)")
            print(f"  Desvio Padrão: {std_val:.4f} ({std_val*100:.2f}%)")
            print(f"  Intervalo: [{min(set_values):.4f}, {max(set_values):.4f}]")
            print()
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    output_data = {
        'config': {
            'n_sets': N_SETS,
            'm_videos_per_set': M_VIDEOS_PER_SET,
            'timestamp': timestamp
        },
        'benchmark_metrics': BENCHMARK_METRICS,
        'overall_validation_metrics': overall_metrics,
        'comparison': overall_comparison,
        'set_metrics': all_set_metrics,
        'total_videos_analyzed': len(all_results),
        'total_comments_analyzed': overall_metrics['total_comments']
    }
    
    # Save in results directory
    os.makedirs('results', exist_ok=True)
    output_file = f'results/metrics_comparison_benchmark_{timestamp}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Detailed results saved: {output_file}")
    print()
    print("="*80)
    print("VALIDATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()


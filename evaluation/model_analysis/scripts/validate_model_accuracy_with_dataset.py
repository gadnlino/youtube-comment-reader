#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model Accuracy Validation with Dataset Ground Truth

This script validates the TF-IDF + Logistic Regression model accuracy
by comparing API predictions with ground truth labels from the dataset.
"""

import requests
import pandas as pd
import json
import time
import os
from datetime import datetime
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

# Dataset path
DATASET_PATH = '/Users/guiavenas/.cache/kagglehub/datasets/amaanpoonawala/youtube-comments-sentiment-dataset/versions/1/youtube_comments_cleaned.csv'

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
        'showNeutral': 'true'  # Show all sentiments to get complete data
    }
    
    for attempt in range(retries):
        try:
            print(f"    Attempt {attempt + 1}/{retries}...", end=" ")
            response = requests.get(endpoint, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                print(f"✓ Success - {len(data['items'])} comments")
                return data['items']
            else:
                print(f"✗ No comments")
                return []
                
        except Exception as e:
            print(f"✗ Error: {e}")
            if attempt < retries - 1:
                time.sleep(2)
    
    return []


def load_ground_truth(video_id):
    """Load ground truth labels from dataset."""
    df = pd.read_csv(DATASET_PATH, low_memory=False)
    video_df = df[df['VideoID'] == video_id].copy()
    
    # Create mapping of comment text to sentiment
    ground_truth = {}
    for _, row in video_df.iterrows():
        text = str(row['CommentText']).strip().lower()
        sentiment = SENTIMENT_MAP.get(row['Sentiment'], 'UNKNOWN')
        ground_truth[text] = sentiment
    
    return ground_truth


def validate_video(video_info):
    """Validate model predictions for a single video."""
    print(f"\n{'─'*80}")
    print(f"Video: {video_info['title'][:60]}")
    print(f"VideoID: {video_info['id']}")
    print(f"Ground Truth: {video_info['total']} comments")
    print(f"{'─'*80}")
    
    # Fetch predictions from API
    api_comments = fetch_comments_with_sentiment(video_info['id'], max_results=100)
    
    if not api_comments:
        print("  ⚠️  Failed to fetch comments from API")
        return None
    
    # Load ground truth
    print(f"  Loading ground truth from dataset...")
    ground_truth = load_ground_truth(video_info['id'])
    print(f"  ✓ Loaded {len(ground_truth)} ground truth labels")
    
    # Match predictions with ground truth
    y_true = []
    y_pred = []
    matched = 0
    
    for comment in api_comments:
        text = comment['snippet']['topLevelComment']['snippet']['textDisplay'].strip().lower()
        predicted = comment.get('sentiment', 'UNKNOWN')
        
        if text in ground_truth:
            true_label = ground_truth[text]
            y_true.append(true_label)
            y_pred.append(predicted)
            matched += 1
    
    print(f"  ✓ Matched {matched}/{len(api_comments)} comments with ground truth")
    
    if len(y_true) < 5:
        print(f"  ⚠️  Too few matches ({len(y_true)}) - skipping")
        return None
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    
    # Calculate per-class metrics (handle zero division)
    labels = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
    precision = precision_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    
    print(f"\n  📊 Metrics:")
    print(f"     Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"     Precision: {precision:.4f}")
    print(f"     Recall:    {recall:.4f}")
    print(f"     F1-Score:  {f1:.4f}")
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    print(f"\n  📈 Confusion Matrix:")
    print(f"     {'':>12} {'POS':>8} {'NEG':>8} {'NEU':>8}")
    for i, label in enumerate(['POSITIVE', 'NEGATIVE', 'NEUTRAL']):
        print(f"     {label:>12} {cm[i][0]:>8} {cm[i][1]:>8} {cm[i][2]:>8}")
    
    return {
        'video_id': video_info['id'],
        'video_title': video_info['title'],
        'total_comments': len(y_true),
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'confusion_matrix': cm.tolist(),
        'y_true': y_true,
        'y_pred': y_pred
    }


def main():
    """Main validation function."""
    print("=" * 80)
    print("MODEL ACCURACY VALIDATION WITH DATASET GROUND TRUTH")
    print("=" * 80)
    print()
    print(f"Starting validation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load video list
    # Load selected videos (use test file for quick validation)
    test_file = 'test_3_videos.json'
    if os.path.exists(test_file):
        print(f"Using test file: {test_file}")
        with open(test_file, 'r') as f:
            videos = json.load(f)
    else:
        with open('dataset_videos_for_accuracy_validation.json', 'r') as f:
            videos = json.load(f)
    
    print(f"Testing {len(videos)} videos from dataset")
    print()
    
    results = []
    for i, video in enumerate(videos, 1):
        print(f"\n{'='*80}")
        print(f"Video {i}/{len(videos)}")
        print(f"{'='*80}")
        
        result = validate_video(video)
        if result:
            results.append(result)
        
        # Rate limiting
        if i < len(videos):
            time.sleep(2)
    
    # Overall statistics
    print(f"\n\n{'='*80}")
    print("OVERALL VALIDATION RESULTS")
    print(f"{'='*80}")
    print()
    print(f"Videos tested: {len(results)}/{len(videos)}")
    print(f"Total comments validated: {sum(r['total_comments'] for r in results)}")
    print()
    
    if results:
        avg_accuracy = sum(r['accuracy'] for r in results) / len(results)
        avg_precision = sum(r['precision'] for r in results) / len(results)
        avg_recall = sum(r['recall'] for r in results) / len(results)
        avg_f1 = sum(r['f1_score'] for r in results) / len(results)
        
        print(f"Average Metrics:")
        print(f"  Accuracy:  {avg_accuracy:.4f} ({avg_accuracy*100:.2f}%)")
        print(f"  Precision: {avg_precision:.4f}")
        print(f"  Recall:    {avg_recall:.4f}")
        print(f"  F1-Score:  {avg_f1:.4f}")
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'model_accuracy_validation_{timestamp}.json'
        
        summary = {
            'timestamp': timestamp,
            'videos_tested': len(results),
            'total_comments': sum(r['total_comments'] for r in results),
            'average_accuracy': avg_accuracy,
            'average_precision': avg_precision,
            'average_recall': avg_recall,
            'average_f1_score': avg_f1,
            'results': results
        }
        
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✅ Results saved to: {output_file}")
    else:
        print("❌ No successful validations")
    
    print(f"\n{'='*80}")
    print("VALIDATION COMPLETE")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()


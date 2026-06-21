#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pre-filter Working Videos

Test all videos from the dataset to identify which ones work with the API.
This avoids wasting time on videos that return HTTP 502.
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime

API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod"
MIN_COMMENTS = 500

def test_video_quick(video_id, retries=2):
    """Quick test if video works with API."""
    endpoint = f"{API_BASE_URL}/video/comments"
    params = {
        'videoId': video_id,
        'maxResults': 10,  # Just 10 comments for quick test
        'part': 'snippet'
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(endpoint, params=params, timeout=30)
            if response.status_code == 200:
                items = response.json().get('items', [])
                return len(items) > 0, None
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            if attempt == retries - 1:
                return False, str(e)
            time.sleep(1)
    return False, "Unknown error"

def main():
    print("="*80)
    print("PRE-FILTERING WORKING VIDEOS")
    print("="*80)
    print()
    
    # Load dataset
    print("Loading dataset...")
    dataset_path = '../api_load_testing/youtube_comments_cleaned.csv'
    if not os.path.exists(dataset_path):
        dataset_path = 'youtube_comments_cleaned.csv'
    df = pd.read_csv(dataset_path)
    print(f"✓ Loaded {len(df)} comments")
    print()
    
    # Group by video
    video_stats = df.groupby('VideoID').agg({
        'CommentID': 'count',
        'VideoTitle': 'first',
        'Sentiment': lambda x: {
            'positive': (x == 'Positive').sum(),
            'negative': (x == 'Negative').sum(),
            'neutral': (x == 'Neutral').sum()
        }
    }).reset_index()
    
    video_stats.columns = ['video_id', 'total', 'title', 'sentiment_dist']
    video_stats = video_stats[video_stats['total'] >= MIN_COMMENTS].copy()
    
    print(f"✓ Found {len(video_stats)} videos with ≥{MIN_COMMENTS} comments")
    print()
    print("Testing each video with API...")
    print()
    
    working_videos = []
    failed_videos = []
    
    for i, row in video_stats.iterrows():
        video_id = row['video_id']
        title = row['title']
        total = row['total']
        dist = row['sentiment_dist']
        
        print(f"[{i+1}/{len(video_stats)}] Testing {title[:50]}...", end=" ", flush=True)
        
        works, error = test_video_quick(video_id)
        
        if works:
            print("✓")
            working_videos.append({
                'id': video_id,
                'title': title,
                'total': int(total),
                'positive': int(dist['positive']),
                'negative': int(dist['negative']),
                'neutral': int(dist['neutral'])
            })
        else:
            print(f"✗ ({error})")
            failed_videos.append({
                'id': video_id,
                'title': title,
                'error': error
            })
        
        # Rate limiting
        time.sleep(0.5)
    
    print()
    print("="*80)
    print("FILTERING COMPLETE")
    print("="*80)
    print()
    print(f"Working videos: {len(working_videos)}")
    print(f"Failed videos: {len(failed_videos)}")
    print(f"Success rate: {len(working_videos)/len(video_stats)*100:.1f}%")
    print()
    
    # Save working videos
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Save in data directory
    os.makedirs('data', exist_ok=True)
    output_file = f'data/working_videos_{timestamp}.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(working_videos, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {len(working_videos)} working videos to: {output_file}")
    
    # Save failed videos for analysis
    failed_file = f'failed_videos_{timestamp}.json'
    with open(failed_file, 'w', encoding='utf-8') as f:
        json.dump(failed_videos, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {len(failed_videos)} failed videos to: {failed_file}")
    print()
    
    if len(working_videos) >= 150:
        print(f"✅ SUCCESS: Found {len(working_videos)} working videos (need 150 for 5 sets × 30)")
    else:
        print(f"⚠️  WARNING: Only {len(working_videos)} working videos (need 150 for 5 sets × 30)")
        print(f"   Can do {len(working_videos)//30} complete sets of 30 videos")

if __name__ == "__main__":
    main()


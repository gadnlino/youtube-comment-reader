#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze Language Distribution in YouTube Video Comments

This script fetches comments from a YouTube video via the API
and detects the language of each comment to determine the
predominant language.
"""

import requests
import time
from langdetect import detect, LangDetectException
from collections import Counter

# API configuration
API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod"

def fetch_comments(video_id, max_results=100):
    """
    Fetch comments for a video.
    
    Args:
        video_id: YouTube video ID
        max_results: Maximum number of comments to fetch
    
    Returns:
        List of comment texts
    """
    endpoint = f"{API_BASE_URL}/video/comments"
    params = {
        'videoId': video_id,
        'maxResults': max_results
    }
    
    try:
        response = requests.get(endpoint, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        comments = []
        if 'items' in data:
            for item in data['items']:
                if 'snippet' in item and 'textDisplay' in item['snippet']:
                    comments.append(item['snippet']['textDisplay'])
        
        return comments
    except Exception as e:
        print(f"Error fetching comments: {e}")
        return []


def detect_language(text):
    """
    Detect language of text.
    
    Args:
        text: Text to analyze
    
    Returns:
        Language code (e.g., 'en', 'es', 'pt') or 'unknown'
    """
    try:
        # Remove common non-linguistic elements
        cleaned = text.replace('😂', '').replace('❤️', '').replace('🔥', '')
        if len(cleaned.strip()) < 3:
            return 'unknown'
        return detect(cleaned)
    except LangDetectException:
        return 'unknown'


def analyze_video_language(video_id, video_name, max_comments=100):
    """
    Analyze language distribution in video comments.
    
    Args:
        video_id: YouTube video ID
        video_name: Video name for display
        max_comments: Maximum comments to analyze
    
    Returns:
        Dictionary with language statistics
    """
    print(f"\n{'='*80}")
    print(f"📊 Analyzing: {video_name}")
    print(f"Video ID: {video_id}")
    print(f"{'='*80}")
    
    # Fetch comments
    comments = fetch_comments(video_id, max_comments)
    
    if not comments:
        print("❌ No comments found or error fetching")
        return None
    
    print(f"✅ Fetched {len(comments)} comments")
    print("\nDetecting languages...")
    
    # Detect language for each comment
    languages = []
    for i, comment in enumerate(comments, 1):
        lang = detect_language(comment)
        languages.append(lang)
        if i % 20 == 0:
            print(f"  Processed {i}/{len(comments)} comments...")
    
    # Count languages
    lang_counts = Counter(languages)
    total = len([l for l in languages if l != 'unknown'])
    
    print(f"\n📈 Language Distribution:")
    print(f"{'Language':<15} {'Count':>6} {'Percentage':>12}")
    print("-" * 40)
    
    # Sort by count
    for lang, count in lang_counts.most_common():
        if lang == 'unknown':
            continue
        percentage = (count / total * 100) if total > 0 else 0
        lang_name = get_language_name(lang)
        print(f"{lang_name:<15} {count:>6} {percentage:>11.1f}%")
    
    if 'unknown' in lang_counts:
        print(f"{'Unknown':<15} {lang_counts['unknown']:>6} {'':>12}")
    
    # Determine predominant language
    if lang_counts:
        most_common = lang_counts.most_common(1)[0]
        if most_common[0] != 'unknown':
            predominant = most_common[0]
            predominant_pct = (most_common[1] / total * 100) if total > 0 else 0
            print(f"\n✅ Predominant language: {get_language_name(predominant)} ({predominant_pct:.1f}%)")
            
            return {
                'video_id': video_id,
                'video_name': video_name,
                'total_comments': len(comments),
                'predominant_language': predominant,
                'predominant_percentage': predominant_pct,
                'language_distribution': dict(lang_counts)
            }
    
    return None


def get_language_name(code):
    """Get language name from code."""
    lang_map = {
        'en': 'English',
        'es': 'Spanish',
        'pt': 'Portuguese',
        'ko': 'Korean',
        'ja': 'Japanese',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'ru': 'Russian',
        'zh-cn': 'Chinese',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'nl': 'Dutch',
        'tr': 'Turkish',
        'unknown': 'Unknown'
    }
    return lang_map.get(code, code.upper())


if __name__ == "__main__":
    # Test with videos from the current list
    test_videos = [
        ('kJQP7kiw5Fk', 'Luis Fonsi - Despacito'),
        ('pRpeEdMmmQ0', 'Shakira - Waka Waka'),
        ('hcm55lU9knw', 'Anitta - Envolver'),
        ('IHNzOHi8sJs', 'BLACKPINK - DDU-DU DDU-DU'),
    ]
    
    results = []
    for video_id, video_name in test_videos:
        result = analyze_video_language(video_id, video_name)
        if result:
            results.append(result)
        time.sleep(2)  # Rate limiting
    
    # Summary
    print(f"\n\n{'='*80}")
    print("📊 SUMMARY")
    print(f"{'='*80}")
    for r in results:
        print(f"\n{r['video_name']}")
        print(f"  Predominant: {get_language_name(r['predominant_language'])} ({r['predominant_percentage']:.1f}%)")


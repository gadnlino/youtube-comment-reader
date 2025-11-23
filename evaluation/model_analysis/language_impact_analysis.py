#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Language Impact Analysis on Sentiment Classification

This script analyzes how the language of YouTube comments affects
sentiment classification accuracy by comparing sentiment distributions
across videos with different primary languages:
- English-dominant video (Rick Astley)
- English-dominant historical video (Me at the zoo)
- Multilingual video (Gangnam Style - Korean/International)

Author: AI Assistant
Date: November 2, 2025
"""

import requests
import json
import time
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

# API configuration
API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod"
COMMENTS_ENDPOINT = f"{API_BASE_URL}/videos/comments"

# Test videos with different language characteristics
TEST_VIDEOS = [
    {
        'id': 'dQw4w9WgXcQ',
        'name': 'Rick Astley - Never Gonna Give You Up',
        'primary_language': 'English',
        'description': 'Classic 1987 music video - predominantly English comments',
        'expected_language_diversity': 'Low (90%+ English)'
    },
    {
        'id': 'jNQXAC9IVRw',
        'name': 'Me at the zoo',
        'primary_language': 'English',
        'description': 'First YouTube video (2005) - nostalgic English comments',
        'expected_language_diversity': 'Low (95%+ English)'
    },
    {
        'id': '9bZkp7q19f0',
        'name': 'PSY - Gangnam Style',
        'primary_language': 'Multilingual (Korean/International)',
        'description': 'Global viral phenomenon - Korean, Spanish, Portuguese, etc.',
        'expected_language_diversity': 'High (40-60% non-English)'
    }
]

def fetch_comments_with_sentiment(video_id, max_results=100):
    """
    Fetch comments for a video with sentiment analysis enabled.
    
    Args:
        video_id: YouTube video ID
        max_results: Number of comments to fetch (default 100)
    
    Returns:
        dict: API response containing comments with sentiment labels
    """
    params = {
        'videoId': video_id,
        'maxResults': max_results,
        'analyzeSentiment': 'true'  # Enable sentiment analysis
    }
    
    print(f"  Fetching {max_results} comments for video {video_id}...")
    start_time = time.time()
    
    try:
        response = requests.get(COMMENTS_ENDPOINT, params=params, timeout=30)
        elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Success ({elapsed_time:.2f}ms) - {len(data.get('comments', []))} comments")
            return {
                'success': True,
                'data': data,
                'response_time_ms': elapsed_time
            }
        else:
            print(f"  ✗ Error: HTTP {response.status_code}")
            return {
                'success': False,
                'error': f"HTTP {response.status_code}",
                'response_time_ms': elapsed_time
            }
    except Exception as e:
        print(f"  ✗ Exception: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'response_time_ms': 0
        }

def analyze_sentiment_distribution(comments):
    """
    Analyze sentiment distribution in a list of comments.
    
    Args:
        comments: List of comment objects with 'sentiment' field
    
    Returns:
        dict: Counts and percentages for each sentiment category
    """
    sentiment_counts = defaultdict(int)
    total = len(comments)
    
    for comment in comments:
        sentiment = comment.get('sentiment', 'UNKNOWN')
        sentiment_counts[sentiment] += 1
    
    # Calculate percentages
    sentiment_stats = {}
    for sentiment, count in sentiment_counts.items():
        percentage = (count / total * 100) if total > 0 else 0
        sentiment_stats[sentiment] = {
            'count': count,
            'percentage': percentage
        }
    
    return sentiment_stats

def run_language_impact_analysis():
    """
    Main analysis function: fetch comments for each video and compare
    sentiment distributions to identify language-related biases.
    """
    print("=" * 80)
    print("LANGUAGE IMPACT ANALYSIS ON SENTIMENT CLASSIFICATION")
    print("=" * 80)
    print(f"\nStarting analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing {len(TEST_VIDEOS)} videos with different language profiles\n")
    
    results = []
    
    # Fetch and analyze each video
    for video in TEST_VIDEOS:
        print(f"\n{'─' * 80}")
        print(f"Video: {video['name']}")
        print(f"  ID: {video['id']}")
        print(f"  Primary Language: {video['primary_language']}")
        print(f"  Expected Diversity: {video['expected_language_diversity']}")
        print(f"{'─' * 80}")
        
        # Fetch comments with sentiment analysis
        response = fetch_comments_with_sentiment(video['id'], max_results=100)
        
        if response['success']:
            comments = response['data'].get('comments', [])
            sentiment_stats = analyze_sentiment_distribution(comments)
            
            # Store results
            result = {
                'video_id': video['id'],
                'video_name': video['name'],
                'primary_language': video['primary_language'],
                'language_diversity': video['expected_language_diversity'],
                'total_comments': len(comments),
                'sentiment_distribution': sentiment_stats,
                'response_time_ms': response['response_time_ms']
            }
            results.append(result)
            
            # Print distribution
            print("\n  Sentiment Distribution:")
            for sentiment, stats in sorted(sentiment_stats.items()):
                print(f"    {sentiment:10s}: {stats['count']:3d} ({stats['percentage']:5.1f}%)")
        else:
            print(f"  Failed to fetch comments: {response.get('error', 'Unknown error')}")
    
    # Save raw results to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"language_impact_results_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': timestamp,
            'test_date': datetime.now().isoformat(),
            'videos_analyzed': len(results),
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 80}")
    print(f"✓ Analysis complete!")
    print(f"✓ Results saved to: {output_file}")
    print(f"{'=' * 80}\n")
    
    # Generate visualization
    generate_comparison_chart(results, timestamp)
    
    # Generate analysis report
    generate_analysis_report(results, timestamp)
    
    return results

def generate_comparison_chart(results, timestamp):
    """
    Generate a comparative bar chart showing sentiment distribution
    across videos with different language profiles.
    """
    if not results:
        print("No results to visualize")
        return
    
    # Prepare data for plotting
    video_names = []
    positive_pcts = []
    negative_pcts = []
    neutral_pcts = []
    
    for result in results:
        video_names.append(f"{result['video_name']}\n({result['primary_language']})")
        
        sentiment_dist = result['sentiment_distribution']
        positive_pcts.append(sentiment_dist.get('POSITIVE', {}).get('percentage', 0))
        negative_pcts.append(sentiment_dist.get('NEGATIVE', {}).get('percentage', 0))
        neutral_pcts.append(sentiment_dist.get('NEUTRAL', {}).get('percentage', 0))
    
    # Create stacked bar chart
    fig, ax = plt.subplots(figsize=(12, 8))
    
    x = np.arange(len(video_names))
    width = 0.6
    
    # Create bars
    p1 = ax.bar(x, positive_pcts, width, label='Positive', color='#2ecc71')
    p2 = ax.bar(x, negative_pcts, width, bottom=positive_pcts, 
                label='Negative', color='#e74c3c')
    p3 = ax.bar(x, neutral_pcts, width, 
                bottom=np.array(positive_pcts) + np.array(negative_pcts),
                label='Neutral', color='#95a5a6')
    
    # Customize chart
    ax.set_ylabel('Percentage of Comments (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Video (Primary Language)', fontsize=12, fontweight='bold')
    ax.set_title('Sentiment Distribution Comparison: Language Impact Analysis\n' +
                 'English vs Multilingual Videos (100 comments each)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(video_names, fontsize=10)
    ax.legend(loc='upper right', fontsize=11)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add percentage labels on bars
    for i, (pos, neg, neu) in enumerate(zip(positive_pcts, negative_pcts, neutral_pcts)):
        if pos > 5:
            ax.text(i, pos/2, f'{pos:.1f}%', ha='center', va='center', 
                   fontweight='bold', color='white', fontsize=10)
        if neg > 5:
            ax.text(i, pos + neg/2, f'{neg:.1f}%', ha='center', va='center',
                   fontweight='bold', color='white', fontsize=10)
        if neu > 5:
            ax.text(i, pos + neg + neu/2, f'{neu:.1f}%', ha='center', va='center',
                   fontweight='bold', color='white', fontsize=10)
    
    plt.tight_layout()
    
    # Save figure
    output_file = f'language_impact_comparison_{timestamp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Visualization saved to: {output_file}")
    plt.close()

def generate_analysis_report(results, timestamp):
    """
    Generate a text report with statistical analysis and conclusions.
    """
    if not results:
        print("No results to analyze")
        return
    
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("LANGUAGE IMPACT ANALYSIS REPORT")
    report_lines.append("=" * 80)
    report_lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"Videos Analyzed: {len(results)}\n")
    
    # Calculate averages for English vs Multilingual
    english_videos = [r for r in results if 'English' in r['primary_language'] and 'Multilingual' not in r['primary_language']]
    multilingual_videos = [r for r in results if 'Multilingual' in r['primary_language']]
    
    if english_videos:
        report_lines.append("\n" + "─" * 80)
        report_lines.append("ENGLISH-DOMINANT VIDEOS (Expected: Lower NEUTRAL%)")
        report_lines.append("─" * 80)
        
        avg_pos = np.mean([r['sentiment_distribution'].get('POSITIVE', {}).get('percentage', 0) for r in english_videos])
        avg_neg = np.mean([r['sentiment_distribution'].get('NEGATIVE', {}).get('percentage', 0) for r in english_videos])
        avg_neu = np.mean([r['sentiment_distribution'].get('NEUTRAL', {}).get('percentage', 0) for r in english_videos])
        
        report_lines.append(f"  Average POSITIVE: {avg_pos:.1f}%")
        report_lines.append(f"  Average NEGATIVE: {avg_neg:.1f}%")
        report_lines.append(f"  Average NEUTRAL:  {avg_neu:.1f}%")
        report_lines.append(f"  Videos: {', '.join([r['video_name'] for r in english_videos])}")
    
    if multilingual_videos:
        report_lines.append("\n" + "─" * 80)
        report_lines.append("MULTILINGUAL VIDEOS (Expected: Higher NEUTRAL%)")
        report_lines.append("─" * 80)
        
        for r in multilingual_videos:
            pos = r['sentiment_distribution'].get('POSITIVE', {}).get('percentage', 0)
            neg = r['sentiment_distribution'].get('NEGATIVE', {}).get('percentage', 0)
            neu = r['sentiment_distribution'].get('NEUTRAL', {}).get('percentage', 0)
            
            report_lines.append(f"  {r['video_name']}:")
            report_lines.append(f"    POSITIVE: {pos:.1f}%")
            report_lines.append(f"    NEGATIVE: {neg:.1f}%")
            report_lines.append(f"    NEUTRAL:  {neu:.1f}%")
    
    # Calculate NEUTRAL% difference
    if english_videos and multilingual_videos:
        english_neutral_avg = np.mean([r['sentiment_distribution'].get('NEUTRAL', {}).get('percentage', 0) for r in english_videos])
        multilingual_neutral_avg = np.mean([r['sentiment_distribution'].get('NEUTRAL', {}).get('percentage', 0) for r in multilingual_videos])
        
        neutral_diff = multilingual_neutral_avg - english_neutral_avg
        
        report_lines.append("\n" + "=" * 80)
        report_lines.append("KEY FINDINGS")
        report_lines.append("=" * 80)
        report_lines.append(f"\n1. NEUTRAL Classification Bias:")
        report_lines.append(f"   - English videos: {english_neutral_avg:.1f}% neutral")
        report_lines.append(f"   - Multilingual videos: {multilingual_neutral_avg:.1f}% neutral")
        report_lines.append(f"   - Difference: +{neutral_diff:.1f} percentage points for multilingual")
        
        if neutral_diff > 10:
            report_lines.append("\n   ⚠️  SIGNIFICANT LANGUAGE BIAS DETECTED!")
            report_lines.append("   The model classifies multilingual comments as NEUTRAL at a much")
            report_lines.append("   higher rate, likely due to unrecognized tokens in the TF-IDF")
            report_lines.append("   vocabulary trained on English corpus.")
        elif neutral_diff > 5:
            report_lines.append("\n   ⚠️  MODERATE LANGUAGE BIAS DETECTED")
            report_lines.append("   Multilingual comments show increased NEUTRAL classification.")
        else:
            report_lines.append("\n   ✓  No significant language bias detected")
            report_lines.append("   Sentiment distributions are similar across language profiles.")
        
        report_lines.append("\n2. Implications:")
        report_lines.append("   - Model accuracy of 66.14% is valid primarily for English comments")
        report_lines.append("   - Non-English comments likely receive degraded classification quality")
        report_lines.append("   - System is best suited for English-speaking audiences")
        
        report_lines.append("\n3. Recommendations:")
        report_lines.append("   - Document language limitation in system documentation")
        report_lines.append("   - Consider multilingual models (mBERT, XLM-RoBERTa) for global use")
        report_lines.append("   - Implement language detection + language-specific classifiers")
    
    report_lines.append("\n" + "=" * 80)
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 80)
    
    # Write report to file
    report_file = f"language_impact_analysis_report_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"✓ Analysis report saved to: {report_file}")
    
    # Also print to console
    print("\n" + '\n'.join(report_lines))

if __name__ == "__main__":
    try:
        results = run_language_impact_analysis()
        print("\n✓ Language impact analysis completed successfully!")
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n✗ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


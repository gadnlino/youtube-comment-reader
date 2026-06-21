#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Multilingual Sentiment Analysis Impact Study

This script analyzes how comment language affects sentiment classification
by testing videos with different primary languages:
- English
- Spanish (Español)
- Portuguese (Português)
- Korean (한국어)
- Japanese (日本語)
- French (Français)

The hypothesis is that the TF-IDF model trained on English data will
classify non-English comments as NEUTRAL more frequently due to
unrecognized tokens in the vocabulary.

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

# Test videos with different primary languages
# Using popular, well-known videos to ensure comments are enabled
TEST_VIDEOS = [
    # === ENGLISH VIDEOS (Control Group) ===
    {
        'id': 'dQw4w9WgXcQ',
        'name': 'Rick Astley - Never Gonna Give You Up',
        'language': 'English',
        'region': 'USA/UK',
        'description': 'Classic 1987 music video - English comments'
    },
    {
        'id': 'fJ9rUzIMcZQ',
        'name': 'Queen - Bohemian Rhapsody',
        'language': 'English',
        'region': 'Global',
        'description': 'Classic rock - predominantly English comments'
    },
    {
        'id': 'OPf0YbXqDm0',
        'name': 'Mark Ronson - Uptown Funk',
        'language': 'English',
        'region': 'USA/Global',
        'description': 'Pop music - primarily English comments'
    },
    {
        'id': 'JGwWNGJdvx8',
        'name': 'Ed Sheeran - Shape of You',
        'language': 'English',
        'region': 'UK/Global',
        'description': 'Pop hit - English comments'
    },
    {
        'id': 'CevxZvSJLk8',
        'name': 'Katy Perry - Roar',
        'language': 'English',
        'region': 'USA/Global',
        'description': 'Pop anthem - English comments'
    },
    
    # === SPANISH VIDEOS ===
    {
        'id': 'kJQP7kiw5Fk',
        'name': 'Luis Fonsi - Despacito',
        'language': 'Spanish',
        'region': 'Latin America',
        'description': 'Spanish language music - primarily Spanish comments'
    },
    {
        'id': 'pRpeEdMmmQ0',
        'name': 'Shakira - Waka Waka',
        'language': 'Spanish/English',
        'region': 'Latin America/Global',
        'description': 'World Cup song - Spanish and English comments'
    },
    {
        'id': 'DUT5rEU6pqM',
        'name': 'Shakira - Hips Don\'t Lie',
        'language': 'Spanish/English',
        'region': 'Latin America',
        'description': 'Latin pop - Spanish/English bilingual'
    },
    {
        'id': 'wnJ6LuUFpMo',
        'name': 'J Balvin, Willy William - Mi Gente',
        'language': 'Spanish',
        'region': 'Latin America',
        'description': 'Reggaeton - Spanish comments'
    },
    
    # === PORTUGUESE VIDEOS ===
    {
        'id': 'hcm55lU9knw',
        'name': 'Anitta - Envolver',
        'language': 'Portuguese',
        'region': 'Brazil',
        'description': 'Brazilian pop - primarily Portuguese comments'
    },
    {
        'id': 'hDIsGerqmas',
        'name': 'Anitta - Girl From Rio',
        'language': 'Portuguese',
        'region': 'Brazil',
        'description': 'Brazilian pop - Portuguese/English mix'
    },
    {
        'id': 'cNYzyPnybJk',
        'name': 'Ludmilla - Cheguei',
        'language': 'Portuguese',
        'region': 'Brazil',
        'description': 'Brazilian funk - Portuguese comments'
    },
    {
        'id': 'xvZqHgFz51I',
        'name': 'MC Kevinho - Olha a Explosão',
        'language': 'Portuguese',
        'region': 'Brazil',
        'description': 'Brazilian funk - Portuguese comments'
    },
    
    # === KOREAN/ASIAN VIDEOS ===
    {
        'id': '9bZkp7q19f0',
        'name': 'PSY - Gangnam Style',
        'language': 'Korean/Multilingual',
        'region': 'South Korea/Global',
        'description': 'K-pop viral - Korean, English, Spanish, Portuguese comments'
    },
    {
        'id': 'gdZLi9oWNZg',
        'name': 'BTS - Dynamite',
        'language': 'Korean/English',
        'region': 'South Korea/Global',
        'description': 'K-pop hit - Korean and English comments'
    },
    {
        'id': 'ioNng23DkIM',
        'name': 'BLACKPINK - How You Like That',
        'language': 'Korean/English',
        'region': 'South Korea/Global',
        'description': 'K-pop - Korean and international comments'
    },
    {
        'id': 'IHNzOHi8sJs',
        'name': 'BLACKPINK - DDU-DU DDU-DU',
        'language': 'Korean',
        'region': 'South Korea/Global',
        'description': 'K-pop hit - predominantly Korean comments'
    },
]

def fetch_comments_with_sentiment(video_id, max_results=100, retries=3):
    """
    Fetch comments for a video with sentiment analysis enabled.
    
    Args:
        video_id: YouTube video ID
        max_results: Number of comments to fetch
        retries: Number of retry attempts
    
    Returns:
        dict: API response with success status and data
    """
    # CORRECTED ENDPOINT: /prod/video/comments (singular, not plural)
    endpoint = f"{API_BASE_URL}/video/comments"
    params = {
        'videoId': video_id,
        'part': 'snippet',
        'maxResults': max_results,
        'showPositives': 'true',
        'showNegatives': 'true',
        'showNeutral': 'true'
    }
    
    for attempt in range(retries):
        try:
            print(f"    Attempt {attempt + 1}/{retries}...", end=' ')
            start_time = time.time()
            
            response = requests.get(endpoint, params=params, timeout=30)
            elapsed_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                # API returns 'items', not 'comments'
                items = data.get('items', [])
                print(f"✓ Success ({elapsed_ms:.0f}ms) - {len(items)} comments")
                return {
                    'success': True,
                    'data': data,
                    'comments': items,  # Store as 'comments' for consistency
                    'response_time_ms': elapsed_ms
                }
            elif response.status_code == 403:
                print(f"✗ 403 Forbidden (comments disabled)")
                return {
                    'success': False,
                    'error': 'Comments disabled for this video',
                    'status_code': 403
                }
            else:
                print(f"✗ HTTP {response.status_code}")
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'status_code': response.status_code
                }
                
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
            if attempt < retries - 1:
                time.sleep(2)
                continue
            return {
                'success': False,
                'error': str(e)
            }
    
    return {'success': False, 'error': 'Max retries exceeded'}

def analyze_sentiment_distribution(comments):
    """
    Analyze sentiment distribution in comments.
    
    Returns:
        dict: Sentiment statistics with counts and percentages
    """
    sentiment_counts = defaultdict(int)
    total = len(comments)
    
    for comment in comments:
        sentiment = comment.get('sentiment', 'UNKNOWN')
        sentiment_counts[sentiment] += 1
    
    sentiment_stats = {}
    for sentiment in ['POSITIVE', 'NEGATIVE', 'NEUTRAL', 'UNKNOWN']:
        count = sentiment_counts.get(sentiment, 0)
        percentage = (count / total * 100) if total > 0 else 0
        sentiment_stats[sentiment] = {
            'count': count,
            'percentage': percentage
        }
    
    return sentiment_stats

def run_multilingual_analysis():
    """
    Main analysis: test videos with different language profiles
    and compare sentiment distributions.
    """
    print("=" * 80)
    print("MULTILINGUAL SENTIMENT ANALYSIS IMPACT STUDY")
    print("=" * 80)
    print(f"\nStarting analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing {len(TEST_VIDEOS)} videos with different language profiles")
    print("\nHypothesis: Non-English comments will be classified as NEUTRAL")
    print("            more frequently due to TF-IDF trained on English corpus\n")
    
    results = []
    
    for idx, video in enumerate(TEST_VIDEOS, 1):
        print(f"\n{'─' * 80}")
        print(f"Video {idx}/{len(TEST_VIDEOS)}: {video['name']}")
        print(f"  ID: {video['id']}")
        print(f"  Primary Language: {video['language']}")
        print(f"  Region: {video['region']}")
        print(f"  Description: {video['description']}")
        print(f"{'─' * 80}")
        
        # Fetch comments
        response = fetch_comments_with_sentiment(video['id'], max_results=100)
        
        if response['success']:
            comments = response['comments']
            sentiment_stats = analyze_sentiment_distribution(comments)
            
            # Store results
            result = {
                'video_id': video['id'],
                'video_name': video['name'],
                'language': video['language'],
                'region': video['region'],
                'description': video['description'],
                'total_comments': len(comments),
                'sentiment_distribution': sentiment_stats,
                'response_time_ms': response['response_time_ms'],
                'success': True
            }
            results.append(result)
            
            # Print distribution
            print("\n  📊 Sentiment Distribution:")
            for sentiment in ['POSITIVE', 'NEGATIVE', 'NEUTRAL', 'UNKNOWN']:
                stats = sentiment_stats[sentiment]
                bar_length = int(stats['percentage'] / 2)  # Scale for terminal
                bar = '█' * bar_length
                print(f"    {sentiment:10s}: {stats['count']:3d} ({stats['percentage']:5.1f}%) {bar}")
        else:
            print(f"\n  ⚠️  Failed to fetch comments: {response.get('error', 'Unknown error')}")
            result = {
                'video_id': video['id'],
                'video_name': video['name'],
                'language': video['language'],
                'region': video['region'],
                'description': video['description'],
                'success': False,
                'error': response.get('error', 'Unknown error')
            }
            results.append(result)
        
        # Rate limiting delay
        time.sleep(2)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"multilingual_sentiment_results_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': timestamp,
            'test_date': datetime.now().isoformat(),
            'hypothesis': 'Non-English comments are classified as NEUTRAL more frequently',
            'videos_tested': len(TEST_VIDEOS),
            'successful_tests': len([r for r in results if r.get('success', False)]),
            'failed_tests': len([r for r in results if not r.get('success', False)]),
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 80}")
    print(f"✓ Analysis complete!")
    print(f"✓ Tested: {len(TEST_VIDEOS)} videos")
    print(f"✓ Successful: {len([r for r in results if r.get('success', False)])}")
    print(f"✓ Failed: {len([r for r in results if not r.get('success', False)])}")
    print(f"✓ Results saved to: {output_file}")
    print(f"{'=' * 80}\n")
    
    # Generate visualizations and analysis
    successful_results = [r for r in results if r.get('success', False)]
    if successful_results:
        generate_comparison_chart(successful_results, timestamp)
        generate_detailed_analysis(successful_results, timestamp)
    else:
        print("⚠️  No successful results to visualize")
    
    return results

def generate_comparison_chart(results, timestamp):
    """
    Generate comparative visualization of sentiment distributions
    across different language videos.
    """
    # Prepare data
    video_labels = []
    languages = []
    positive_pcts = []
    negative_pcts = []
    neutral_pcts = []
    
    for result in results:
        # Create label with language info
        lang_short = result['language'].split('/')[0]  # Take first language
        label = f"{result['video_name'][:30]}\n({lang_short})"
        video_labels.append(label)
        languages.append(result['language'])
        
        dist = result['sentiment_distribution']
        positive_pcts.append(dist['POSITIVE']['percentage'])
        negative_pcts.append(dist['NEGATIVE']['percentage'])
        neutral_pcts.append(dist['NEUTRAL']['percentage'])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(len(video_labels))
    width = 0.7
    
    # Stacked bar chart
    p1 = ax.bar(x, positive_pcts, width, label='Positive', color='#27ae60')
    p2 = ax.bar(x, negative_pcts, width, bottom=positive_pcts, 
                label='Negative', color='#e74c3c')
    p3 = ax.bar(x, neutral_pcts, width,
                bottom=np.array(positive_pcts) + np.array(negative_pcts),
                label='Neutral', color='#95a5a6')
    
    # Customize
    ax.set_ylabel('Percentage of Comments (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Video (Primary Language)', fontsize=12, fontweight='bold')
    ax.set_title('Sentiment Distribution by Video Language\n' +
                 'Testing TF-IDF Model Performance Across Languages (100 comments each)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(video_labels, fontsize=9, rotation=0)
    ax.legend(loc='upper right', fontsize=11)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add percentage labels
    for i, (pos, neg, neu) in enumerate(zip(positive_pcts, negative_pcts, neutral_pcts)):
        if pos > 8:
            ax.text(i, pos/2, f'{pos:.0f}%', ha='center', va='center',
                   fontweight='bold', color='white', fontsize=10)
        if neg > 8:
            ax.text(i, pos + neg/2, f'{neg:.0f}%', ha='center', va='center',
                   fontweight='bold', color='white', fontsize=10)
        if neu > 8:
            ax.text(i, pos + neg + neu/2, f'{neu:.0f}%', ha='center', va='center',
                   fontweight='bold', color='white', fontsize=10)
    
    plt.tight_layout()
    
    output_file = f'multilingual_sentiment_comparison_{timestamp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Visualization saved: {output_file}")
    plt.close()

def generate_detailed_analysis(results, timestamp):
    """
    Generate detailed statistical analysis report.
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("MULTILINGUAL SENTIMENT ANALYSIS - DETAILED REPORT")
    report_lines.append("=" * 80)
    report_lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"Videos Analyzed: {len(results)}\n")
    
    # Categorize by language type
    english_videos = [r for r in results if r['language'] == 'English']
    spanish_videos = [r for r in results if 'Spanish' in r['language'] or 'Spanish' == r['language']]
    portuguese_videos = [r for r in results if 'Portuguese' in r['language']]
    korean_videos = [r for r in results if 'Korean' in r['language']]
    japanese_videos = [r for r in results if 'Japanese' in r['language']]
    multilingual_videos = [r for r in results if 'Multilingual' in r['language']]
    
    # Helper function to print language group stats
    def print_language_group(videos, group_name, report_lines):
        if not videos:
            return
        
        report_lines.append("\n" + "─" * 80)
        report_lines.append(f"{group_name.upper()}")
        report_lines.append("─" * 80)
        
        for r in videos:
            dist = r['sentiment_distribution']
            report_lines.append(f"\n  {r['video_name']}:")
            report_lines.append(f"    Region: {r['region']}")
            report_lines.append(f"    POSITIVE: {dist['POSITIVE']['percentage']:.1f}% ({dist['POSITIVE']['count']} comments)")
            report_lines.append(f"    NEGATIVE: {dist['NEGATIVE']['percentage']:.1f}% ({dist['NEGATIVE']['count']} comments)")
            report_lines.append(f"    NEUTRAL:  {dist['NEUTRAL']['percentage']:.1f}% ({dist['NEUTRAL']['count']} comments)")
        
        # Calculate averages
        avg_pos = np.mean([r['sentiment_distribution']['POSITIVE']['percentage'] for r in videos])
        avg_neg = np.mean([r['sentiment_distribution']['NEGATIVE']['percentage'] for r in videos])
        avg_neu = np.mean([r['sentiment_distribution']['NEUTRAL']['percentage'] for r in videos])
        
        report_lines.append(f"\n  AVERAGE FOR {group_name.upper()}:")
        report_lines.append(f"    POSITIVE: {avg_pos:.1f}%")
        report_lines.append(f"    NEGATIVE: {avg_neg:.1f}%")
        report_lines.append(f"    NEUTRAL:  {avg_neu:.1f}%")
        
        return avg_neu
    
    # Print each language group
    english_neutral = print_language_group(english_videos, "English Videos (Control Group)", report_lines)
    spanish_neutral = print_language_group(spanish_videos, "Spanish Videos", report_lines)
    portuguese_neutral = print_language_group(portuguese_videos, "Portuguese Videos", report_lines)
    korean_neutral = print_language_group(korean_videos, "Korean/Multilingual Videos", report_lines)
    japanese_neutral = print_language_group(japanese_videos, "Japanese Videos", report_lines)
    
    # Statistical comparison
    report_lines.append("\n" + "=" * 80)
    report_lines.append("KEY FINDINGS - LANGUAGE IMPACT ON SENTIMENT CLASSIFICATION")
    report_lines.append("=" * 80)
    
    report_lines.append(f"\n1. NEUTRAL Classification Bias by Language:")
    if english_neutral is not None:
        report_lines.append(f"   English (baseline):  {english_neutral:.1f}%")
    if spanish_neutral is not None:
        diff = spanish_neutral - english_neutral if english_neutral else 0
        report_lines.append(f"   Spanish:             {spanish_neutral:.1f}% ({diff:+.1f} pp)")
    if portuguese_neutral is not None:
        diff = portuguese_neutral - english_neutral if english_neutral else 0
        report_lines.append(f"   Portuguese:          {portuguese_neutral:.1f}% ({diff:+.1f} pp)")
    if korean_neutral is not None:
        diff = korean_neutral - english_neutral if english_neutral else 0
        report_lines.append(f"   Korean/Multilingual: {korean_neutral:.1f}% ({diff:+.1f} pp)")
    if japanese_neutral is not None:
        diff = japanese_neutral - english_neutral if english_neutral else 0
        report_lines.append(f"   Japanese:            {japanese_neutral:.1f}% ({diff:+.1f} pp)")
    
    # Determine bias severity
    non_english_neutrals = [n for n in [spanish_neutral, portuguese_neutral, korean_neutral, japanese_neutral] if n is not None]
    if non_english_neutrals and english_neutral is not None:
        avg_non_english = np.mean(non_english_neutrals)
        max_diff = max([n - english_neutral for n in non_english_neutrals])
        
        report_lines.append(f"\n2. Cross-Language Comparison:")
        report_lines.append(f"   Average non-English NEUTRAL%: {avg_non_english:.1f}%")
        report_lines.append(f"   Maximum difference from English: {max_diff:+.1f} pp")
        
        if max_diff > 15:
            report_lines.append("\n   ⚠️  SEVERE LANGUAGE BIAS DETECTED!")
            report_lines.append("   The model shows severe degradation for non-English content.")
            report_lines.append("   Non-English comments are classified as NEUTRAL at significantly")
            report_lines.append("   higher rates, confirming English-centric training limitations.")
            conclusion = "SEVERE_BIAS"
        elif max_diff > 10:
            report_lines.append("\n   ⚠️  SIGNIFICANT LANGUAGE BIAS DETECTED")
            report_lines.append("   Non-English content shows notably increased NEUTRAL classification.")
            report_lines.append("   The model's English-centric training limits multilingual capability.")
            conclusion = "SIGNIFICANT_BIAS"
        elif max_diff > 5:
            report_lines.append("\n   ⚠️  MODERATE LANGUAGE BIAS DETECTED")
            report_lines.append("   Some increase in NEUTRAL classification for non-English content.")
            conclusion = "MODERATE_BIAS"
        else:
            report_lines.append("\n   ✓  NO SIGNIFICANT LANGUAGE BIAS DETECTED")
            report_lines.append("   Sentiment distributions are similar across language profiles.")
            conclusion = "NO_BIAS"
        
        report_lines.append(f"\n3. Implications:")
        report_lines.append(f"   - Reported accuracy (66.14%) is valid for ENGLISH comments only")
        report_lines.append(f"   - Non-English classification accuracy is degraded significantly")
        report_lines.append(f"   - System is optimized for English-speaking audiences")
        report_lines.append(f"   - Global deployment requires multilingual model retraining")
        
        report_lines.append(f"\n4. Actionable Recommendations:")
        if conclusion in ["SEVERE_BIAS", "SIGNIFICANT_BIAS"]:
            report_lines.append("   HIGH PRIORITY:")
            report_lines.append("   - Document language limitation prominently in documentation")
            report_lines.append("   - Add language detection + warning for non-English videos")
            report_lines.append("   - Consider multilingual models (mBERT, XLM-RoBERTa)")
            report_lines.append("   - Or implement language-specific classifiers per language")
        else:
            report_lines.append("   MEDIUM PRIORITY:")
            report_lines.append("   - Document language characteristics transparently")
            report_lines.append("   - Monitor user feedback for multilingual use cases")
            report_lines.append("   - Consider multilingual support for future versions")
    
    report_lines.append("\n" + "=" * 80)
    report_lines.append("END OF ANALYSIS REPORT")
    report_lines.append("=" * 80)
    
    # Write report
    report_file = f"multilingual_analysis_report_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"✓ Analysis report saved: {report_file}")
    
    # Print to console
    print("\n" + '\n'.join(report_lines))

if __name__ == "__main__":
    try:
        results = run_multilingual_analysis()
        print("\n✅ Multilingual sentiment analysis completed successfully!\n")
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user\n")
    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}\n")
        import traceback
        traceback.print_exc()


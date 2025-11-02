#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate Academic Visualizations for Multilingual Sentiment Analysis

Creates publication-quality graphs showing language impact on sentiment
classification for inclusion in academic thesis/monograph.

Author: AI Assistant
Date: November 2, 2025
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime

# Set professional style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")

def load_results(filename):
    """Load results from JSON file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_language_comparison_bar_chart(data, timestamp):
    """
    Generate bar chart comparing NEUTRAL% across languages.
    """
    # Organize data by language
    languages = {
        'English': [],
        'Spanish': [],
        'Portuguese': [],
        'Korean/Multi': []
    }
    
    for result in data['results']:
        if not result.get('success', False):
            continue
        
        lang = result['language']
        neutral_pct = result['sentiment_distribution']['NEUTRAL']['percentage']
        
        if lang == 'English':
            languages['English'].append(neutral_pct)
        elif 'Spanish' in lang:
            languages['Spanish'].append(neutral_pct)
        elif 'Portuguese' in lang:
            languages['Portuguese'].append(neutral_pct)
        elif 'Korean' in lang or 'Multilingual' in lang:
            languages['Korean/Multi'].append(neutral_pct)
    
    # Calculate averages
    lang_names = []
    avg_neutrals = []
    std_neutrals = []
    colors = []
    
    for lang, values in languages.items():
        if values:
            lang_names.append(lang)
            avg_neutrals.append(np.mean(values))
            std_neutrals.append(np.std(values) if len(values) > 1 else 0)
            colors.append('#3498db' if lang == 'English' else '#e74c3c')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(lang_names))
    bars = ax.bar(x, avg_neutrals, yerr=std_neutrals, capsize=5,
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
    
    # Customize
    ax.set_ylabel('Average NEUTRAL Classification (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Language', fontsize=12, fontweight='bold')
    ax.set_title('Language Impact on Sentiment Classification\nNEUTRAL Class Bias Across Languages',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(lang_names, fontsize=11)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for i, (bar, val, std) in enumerate(zip(bars, avg_neutrals, std_neutrals)):
        height = bar.get_height()
        label = f'{val:.1f}%'
        if std > 0:
            label += f'\n(σ={std:.1f})'
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
               label, ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Add baseline reference line
    english_avg = avg_neutrals[0] if lang_names[0] == 'English' else None
    if english_avg:
        ax.axhline(y=english_avg, color='blue', linestyle='--', alpha=0.5,
                  label=f'English Baseline ({english_avg:.1f}%)')
        ax.legend(loc='upper right', fontsize=10)
    
    plt.tight_layout()
    filename = f'language_neutral_bias_comparison_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: {filename}")
    plt.close()

def generate_individual_video_chart(data, timestamp):
    """
    Generate chart showing NEUTRAL% for each individual video.
    """
    videos = []
    neutrals = []
    colors = []
    languages = []
    
    for result in data['results']:
        if not result.get('success', False):
            continue
        
        video_name = result['video_name'][:30]  # Truncate long names
        neutral_pct = result['sentiment_distribution']['NEUTRAL']['percentage']
        lang = result['language']
        
        videos.append(video_name)
        neutrals.append(neutral_pct)
        languages.append(lang)
        
        # Color by language
        if lang == 'English':
            colors.append('#3498db')
        elif 'Spanish' in lang:
            colors.append('#e67e22')
        elif 'Portuguese' in lang:
            colors.append('#9b59b6')
        else:
            colors.append('#e74c3c')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    y_pos = np.arange(len(videos))
    bars = ax.barh(y_pos, neutrals, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    
    # Customize
    ax.set_yticks(y_pos)
    ax.set_yticklabels(videos, fontsize=9)
    ax.set_xlabel('NEUTRAL Classification (%)', fontsize=12, fontweight='bold')
    ax.set_title('Sentiment Classification by Video\nNEUTRAL Percentage Across Different Language Content',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 100)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add value labels
    for i, (bar, val, lang) in enumerate(zip(bars, neutrals, languages)):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2,
               f'{val:.0f}% ({lang})', va='center', fontsize=8)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#3498db', label='English'),
        Patch(facecolor='#e67e22', label='Spanish'),
        Patch(facecolor='#9b59b6', label='Portuguese'),
        Patch(facecolor='#e74c3c', label='Korean/Multi')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    filename = f'individual_video_neutral_rates_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: {filename}")
    plt.close()

def generate_sentiment_distribution_heatmap(data, timestamp):
    """
    Generate heatmap showing full sentiment distribution across videos.
    """
    videos = []
    positives = []
    negatives = []
    neutrals = []
    
    for result in data['results']:
        if not result.get('success', False):
            continue
        
        video_name = result['video_name'][:25]
        lang = result['language']
        video_label = f"{video_name}\n({lang})"
        
        videos.append(video_label)
        positives.append(result['sentiment_distribution']['POSITIVE']['percentage'])
        negatives.append(result['sentiment_distribution']['NEGATIVE']['percentage'])
        neutrals.append(result['sentiment_distribution']['NEUTRAL']['percentage'])
    
    # Create matrix for heatmap
    data_matrix = np.array([positives, negatives, neutrals])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    
    im = ax.imshow(data_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(videos)))
    ax.set_yticks(np.arange(3))
    ax.set_xticklabels(videos, rotation=45, ha='right', fontsize=8)
    ax.set_yticklabels(['POSITIVE', 'NEGATIVE', 'NEUTRAL'], fontsize=11, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Percentage (%)', rotation=270, labelpad=20, fontsize=11, fontweight='bold')
    
    # Add text annotations
    for i in range(3):
        for j in range(len(videos)):
            text = ax.text(j, i, f'{data_matrix[i, j]:.0f}%',
                          ha="center", va="center", color="black", fontsize=8, fontweight='bold')
    
    ax.set_title('Sentiment Distribution Heatmap Across Videos\nFull Classification Breakdown by Language',
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    filename = f'sentiment_distribution_heatmap_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: {filename}")
    plt.close()

def generate_language_bias_statistical_plot(data, timestamp):
    """
    Generate box plot showing distribution of NEUTRAL% by language.
    """
    # Organize data by language
    language_data = {
        'English': [],
        'Spanish': [],
        'Portuguese': [],
        'Korean/Multi': []
    }
    
    for result in data['results']:
        if not result.get('success', False):
            continue
        
        lang = result['language']
        neutral_pct = result['sentiment_distribution']['NEUTRAL']['percentage']
        
        if lang == 'English':
            language_data['English'].append(neutral_pct)
        elif 'Spanish' in lang:
            language_data['Spanish'].append(neutral_pct)
        elif 'Portuguese' in lang:
            language_data['Portuguese'].append(neutral_pct)
        elif 'Korean' in lang or 'Multilingual' in lang:
            language_data['Korean/Multi'].append(neutral_pct)
    
    # Filter out empty categories
    languages = []
    data_for_plot = []
    for lang, values in language_data.items():
        if values:
            languages.append(lang)
            data_for_plot.append(values)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Create box plot
    bp = ax.boxplot(data_for_plot, labels=languages, patch_artist=True,
                    notch=True, showmeans=True,
                    boxprops=dict(facecolor='lightblue', alpha=0.7),
                    medianprops=dict(color='red', linewidth=2),
                    meanprops=dict(marker='D', markerfacecolor='green', markersize=8))
    
    # Customize colors
    colors = ['#3498db', '#e67e22', '#9b59b6', '#e74c3c']
    for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    
    # Overlay individual points
    for i, (lang_data, x_pos) in enumerate(zip(data_for_plot, range(1, len(data_for_plot) + 1))):
        y = lang_data
        x = np.random.normal(x_pos, 0.04, size=len(y))
        ax.scatter(x, y, alpha=0.6, s=60, edgecolors='black', linewidths=0.5)
    
    # Customize
    ax.set_ylabel('NEUTRAL Classification (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Language', fontsize=12, fontweight='bold')
    ax.set_title('Statistical Distribution of NEUTRAL Classification by Language\n' +
                 'Box Plot with Individual Data Points',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(40, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='red', linewidth=2, label='Median'),
        Line2D([0], [0], marker='D', color='w', markerfacecolor='green', markersize=8, label='Mean'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=8, 
               alpha=0.6, markeredgecolor='black', label='Individual Videos')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    filename = f'language_bias_boxplot_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Generated: {filename}")
    plt.close()

def main():
    print("=" * 80)
    print("GENERATING ACADEMIC VISUALIZATIONS FOR MULTILINGUAL ANALYSIS")
    print("=" * 80)
    
    # Load latest results
    import glob
    result_files = sorted(glob.glob('multilingual_sentiment_results_*.json'))
    if not result_files:
        print("❌ No result files found!")
        return
    
    latest_file = result_files[-1]
    print(f"\n📊 Loading data from: {latest_file}")
    
    data = load_results(latest_file)
    timestamp = data['timestamp']
    
    print(f"✓ Loaded {len(data['results'])} video results")
    print(f"✓ Successful tests: {data['successful_tests']}")
    print(f"✓ Failed tests: {data['failed_tests']}\n")
    
    print("Generating visualizations...\n")
    
    # Generate all charts
    generate_language_comparison_bar_chart(data, timestamp)
    generate_individual_video_chart(data, timestamp)
    generate_sentiment_distribution_heatmap(data, timestamp)
    generate_language_bias_statistical_plot(data, timestamp)
    
    print("\n" + "=" * 80)
    print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
    print("=" * 80)
    print("\nGenerated files:")
    print(f"  1. language_neutral_bias_comparison_{timestamp}.png")
    print(f"  2. individual_video_neutral_rates_{timestamp}.png")
    print(f"  3. sentiment_distribution_heatmap_{timestamp}.png")
    print(f"  4. language_bias_boxplot_{timestamp}.png")
    print("\n📝 Ready for inclusion in academic thesis/monograph")

if __name__ == "__main__":
    main()


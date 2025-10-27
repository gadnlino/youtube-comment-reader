"""
Generate Academic-Quality Graphs for Multi-Video Performance Report

This script creates publication-ready visualizations for the performance
evaluation report, including response time distributions, trends, and
comparative analyses.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import json

# Set style for academic publications
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'

def load_data():
    """Load test results from CSV and JSON files."""
    csv_file = 'multi_video_results_20251026_212004.csv'
    json_file = 'multi_video_summary_20251026_212004.json'
    
    # Load CSV data
    df = pd.read_csv(csv_file)
    
    # Load JSON summary
    with open(json_file, 'r') as f:
        summary = json.load(f)
    
    return df, summary

def create_response_time_distribution(df):
    """Create box plot showing response time distribution across all requests."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Prepare data by video
    video_data = []
    video_labels = []
    
    for video_name in df['video_name'].unique():
        video_df = df[df['video_name'] == video_name]
        video_data.append(video_df['response_time_ms'].values)
        # Shorten labels for readability
        if 'Music Video' in video_name:
            video_labels.append('Music Video\n(Rick Astley)')
        elif 'Educational' in video_name:
            video_labels.append('Documentary\n(Me at the zoo)')
        else:
            video_labels.append('Viral Music\n(Gangnam Style)')
    
    # Create box plot
    bp = ax.boxplot(video_data, labels=video_labels, patch_artist=True,
                    showmeans=True, meanline=True)
    
    # Customize colors
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Formatting
    ax.set_ylabel('Response Time (ms)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Video Type', fontsize=12, fontweight='bold')
    ax.set_title('Response Time Distribution by Video Type', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(bottom=0)
    
    # Add legend
    ax.legend([bp['boxes'][0], bp['medians'][0], bp['means'][0]], 
              ['IQR', 'Median', 'Mean'],
              loc='upper right')
    
    plt.tight_layout()
    plt.savefig('response_time_boxplot.png', dpi=300, bbox_inches='tight')
    print("✓ Created: response_time_boxplot.png")
    plt.close()

def create_video_specific_trends(df):
    """Create individual trend lines for each video."""
    videos = df['video_name'].unique()
    
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    
    for idx, (video_name, color) in enumerate(zip(videos, colors)):
        ax = axes[idx]
        video_df = df[df['video_name'] == video_name].sort_values('request_number')
        
        # Plot trend line
        ax.plot(video_df['request_number'], video_df['response_time_ms'], 
               marker='o', color=color, linewidth=2, markersize=6, 
               label='Response Time')
        
        # Add mean line
        mean_time = video_df['response_time_ms'].mean()
        ax.axhline(y=mean_time, color='red', linestyle='--', 
                  linewidth=1.5, alpha=0.7, label=f'Mean: {mean_time:.0f}ms')
        
        # Formatting
        ax.set_ylabel('Response Time (ms)', fontsize=11, fontweight='bold')
        ax.set_title(f'{video_name}', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
        ax.set_xlim(0, 21)
        
        # Only show x-label on bottom plot
        if idx == 2:
            ax.set_xlabel('Request Number', fontsize=11, fontweight='bold')
    
    plt.suptitle('Response Time Trends by Video', 
                fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig('video_specific_trends.png', dpi=300, bbox_inches='tight')
    print("✓ Created: video_specific_trends.png")
    plt.close()

def create_temporal_performance(df):
    """Create scatter plot showing all requests over time."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Convert timestamp to relative seconds
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    start_time = df['timestamp'].min()
    df['elapsed_seconds'] = (df['timestamp'] - start_time).dt.total_seconds()
    
    # Plot by video type
    colors = {'Music': '#3498db', 'Documentary': '#2ecc71'}
    markers = {'Music': 'o', 'Documentary': 's'}
    
    for content_type in df['content_type'].unique():
        type_df = df[df['content_type'] == content_type]
        ax.scatter(type_df['elapsed_seconds'], type_df['response_time_ms'],
                  c=colors[content_type], marker=markers[content_type],
                  s=80, alpha=0.7, label=content_type, edgecolors='black',
                  linewidth=0.5)
    
    # Add threshold lines
    ax.axhline(y=500, color='orange', linestyle='--', alpha=0.5, 
              label='Good Threshold (500ms)')
    ax.axhline(y=1000, color='red', linestyle='--', alpha=0.5,
              label='Acceptable Threshold (1000ms)')
    
    # Formatting
    ax.set_xlabel('Elapsed Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Response Time (ms)', fontsize=12, fontweight='bold')
    ax.set_title('Response Time Evolution During Test Execution', 
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    plt.savefig('temporal_performance.png', dpi=300, bbox_inches='tight')
    print("✓ Created: temporal_performance.png")
    plt.close()

def create_cumulative_distribution(df):
    """Create CDF of response times."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Overall CDF
    sorted_times = np.sort(df['response_time_ms'].values)
    cumulative_prob = np.arange(1, len(sorted_times) + 1) / len(sorted_times)
    ax.plot(sorted_times, cumulative_prob * 100, linewidth=2.5, 
           color='#2c3e50', label='All Requests')
    
    # Add percentile markers
    percentiles = [50, 95, 99]
    for p in percentiles:
        value = np.percentile(sorted_times, p)
        ax.axvline(x=value, color='red', linestyle='--', alpha=0.5)
        ax.axhline(y=p, color='red', linestyle='--', alpha=0.5)
        ax.plot(value, p, 'ro', markersize=8)
        ax.text(value + 50, p - 5, f'P{p}: {value:.0f}ms', 
               fontsize=10, fontweight='bold')
    
    # Formatting
    ax.set_xlabel('Response Time (ms)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cumulative Probability (%)', fontsize=12, fontweight='bold')
    ax.set_title('Cumulative Distribution Function of Response Times', 
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='lower right')
    ax.set_xlim(left=0)
    ax.set_ylim(0, 105)
    
    plt.tight_layout()
    plt.savefig('cdf_response_times.png', dpi=300, bbox_inches='tight')
    print("✓ Created: cdf_response_times.png")
    plt.close()

def create_histogram_distribution(df):
    """Create histogram showing response time frequency distribution."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create histogram
    n, bins, patches = ax.hist(df['response_time_ms'], bins=20, 
                               color='#3498db', alpha=0.7, edgecolor='black',
                               linewidth=1.2)
    
    # Add mean and median lines
    mean_time = df['response_time_ms'].mean()
    median_time = df['response_time_ms'].median()
    
    ax.axvline(mean_time, color='red', linestyle='--', linewidth=2,
              label=f'Mean: {mean_time:.0f}ms')
    ax.axvline(median_time, color='green', linestyle='--', linewidth=2,
              label=f'Median: {median_time:.0f}ms')
    
    # Formatting
    ax.set_xlabel('Response Time (ms)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency (Count)', fontsize=12, fontweight='bold')
    ax.set_title('Response Time Frequency Distribution', 
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig('multi_video_response_time_distribution.png', dpi=300, 
                bbox_inches='tight')
    print("✓ Created: multi_video_response_time_distribution.png")
    plt.close()

def create_comparative_bar_chart(summary):
    """Create bar chart comparing average response times."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Extract data
    videos = []
    avg_times = []
    std_devs = []
    
    for result in summary['video_results']:
        videos.append(result['video_name'][:30])  # Truncate long names
        avg_times.append(result['avg_response_time'])
        std_devs.append(result['std_dev'])
    
    # Create bar chart
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    bars = ax.bar(range(len(videos)), avg_times, color=colors, alpha=0.7,
                  edgecolor='black', linewidth=1.5, yerr=std_devs, capsize=10)
    
    # Add value labels on bars
    for i, (bar, avg) in enumerate(zip(bars, avg_times)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{avg:.0f}ms', ha='center', va='bottom', 
               fontsize=11, fontweight='bold')
    
    # Add threshold line
    ax.axhline(y=500, color='orange', linestyle='--', alpha=0.5,
              linewidth=2, label='Good Threshold (500ms)')
    
    # Formatting
    ax.set_ylabel('Average Response Time (ms)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Video', fontsize=12, fontweight='bold')
    ax.set_title('Average Response Time Comparison with Standard Deviation', 
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(range(len(videos)))
    ax.set_xticklabels(videos, rotation=15, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend()
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    plt.savefig('average_response_time_comparison.png', dpi=300, 
                bbox_inches='tight')
    print("✓ Created: average_response_time_comparison.png")
    plt.close()

def create_performance_summary_table(summary):
    """Create a visual table summarizing key metrics."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('tight')
    ax.axis('off')
    
    # Prepare table data
    headers = ['Metric', 'Music Video\n(Rick Astley)', 
              'Documentary\n(Me at the zoo)', 'Viral Music\n(Gangnam Style)']
    
    video_results = summary['video_results']
    
    table_data = [
        ['Avg Response Time', 
         f"{video_results[0]['avg_response_time']:.0f} ms",
         f"{video_results[1]['avg_response_time']:.0f} ms",
         f"{video_results[2]['avg_response_time']:.0f} ms"],
        ['Median Response Time',
         f"{video_results[0]['median_response_time']:.0f} ms",
         f"{video_results[1]['median_response_time']:.0f} ms",
         f"{video_results[2]['median_response_time']:.0f} ms"],
        ['Min Response Time',
         f"{video_results[0]['min_response_time']:.0f} ms",
         f"{video_results[1]['min_response_time']:.0f} ms",
         f"{video_results[2]['min_response_time']:.0f} ms"],
        ['Max Response Time',
         f"{video_results[0]['max_response_time']:.0f} ms",
         f"{video_results[1]['max_response_time']:.0f} ms",
         f"{video_results[2]['max_response_time']:.0f} ms"],
        ['Std Deviation',
         f"±{video_results[0]['std_dev']:.0f} ms",
         f"±{video_results[1]['std_dev']:.0f} ms",
         f"±{video_results[2]['std_dev']:.0f} ms"],
        ['Success Rate',
         f"{video_results[0]['successful_requests']}/20 (100%)",
         f"{video_results[1]['successful_requests']}/20 (100%)",
         f"{video_results[2]['successful_requests']}/20 (100%)"],
    ]
    
    # Create table
    table = ax.table(cellText=table_data, colLabels=headers, 
                    cellLoc='center', loc='center',
                    colWidths=[0.3, 0.23, 0.23, 0.24])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.5)
    
    # Style header row
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_facecolor('#2c3e50')
        cell.set_text_props(weight='bold', color='white')
    
    # Style data rows
    colors = ['#ecf0f1', '#ffffff']
    for i in range(1, len(table_data) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            cell.set_facecolor(colors[i % 2])
            if j == 0:  # First column (metric names)
                cell.set_text_props(weight='bold')
    
    plt.title('Performance Metrics Summary Table', 
             fontsize=14, fontweight='bold', pad=20)
    
    plt.savefig('performance_summary_table.png', dpi=300, bbox_inches='tight')
    print("✓ Created: performance_summary_table.png")
    plt.close()

def main():
    """Generate all academic graphs for the report."""
    print("\n" + "="*60)
    print("Generating Academic-Quality Graphs")
    print("="*60 + "\n")
    
    # Load data
    print("Loading data...")
    df, summary = load_data()
    print(f"✓ Loaded {len(df)} data points\n")
    
    # Generate all graphs
    print("Creating visualizations...\n")
    
    create_histogram_distribution(df)
    create_response_time_distribution(df)
    create_video_specific_trends(df)
    create_temporal_performance(df)
    create_cumulative_distribution(df)
    create_comparative_bar_chart(summary)
    create_performance_summary_table(summary)
    
    print("\n" + "="*60)
    print("✅ All graphs generated successfully!")
    print("="*60)
    print("\nGenerated files:")
    print("  1. multi_video_response_time_distribution.png - Histogram")
    print("  2. response_time_boxplot.png - Box plot comparison")
    print("  3. video_specific_trends.png - Individual video trends")
    print("  4. temporal_performance.png - Time-series scatter plot")
    print("  5. cdf_response_times.png - Cumulative distribution")
    print("  6. average_response_time_comparison.png - Bar chart")
    print("  7. performance_summary_table.png - Metrics table")
    print("\nThese graphs can now be referenced in the academic report.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

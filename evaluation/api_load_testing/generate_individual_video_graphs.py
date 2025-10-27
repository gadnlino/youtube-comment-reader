"""
Generate individual video performance trend graphs for academic report

Creates separate high-quality graphs for each video's response time trends.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set style for academic publications
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'

def create_individual_video_graphs():
    """Create separate graphs for each video."""
    # Load data
    df = pd.read_csv('multi_video_results_20251026_212004.csv')
    
    video_info = [
        {
            'name': 'Music Video - High Engagement',
            'short_name': 'Music Video (Rick Astley)',
            'filename': 'music_video_response_times.png',
            'color': '#3498db'
        },
        {
            'name': 'Educational - Me at the zoo',
            'short_name': 'Documentary (Me at the zoo)',
            'filename': 'documentary_response_times.png',
            'color': '#2ecc71'
        },
        {
            'name': 'Music - Gangnam Style',
            'short_name': 'Viral Music (Gangnam Style)',
            'filename': 'viral_music_response_times.png',
            'color': '#e74c3c'
        }
    ]
    
    for video in video_info:
        video_df = df[df['video_name'] == video['name']].sort_values('request_number')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot response times
        ax.plot(video_df['request_number'], video_df['response_time_ms'],
               marker='o', color=video['color'], linewidth=2.5, markersize=8,
               label='Response Time', markeredgecolor='black', 
               markeredgewidth=0.5)
        
        # Calculate and plot statistics
        mean_time = video_df['response_time_ms'].mean()
        median_time = video_df['response_time_ms'].median()
        min_time = video_df['response_time_ms'].min()
        max_time = video_df['response_time_ms'].max()
        
        # Add mean line
        ax.axhline(y=mean_time, color='red', linestyle='--', 
                  linewidth=2, alpha=0.7, 
                  label=f'Mean: {mean_time:.0f}ms')
        
        # Add median line
        ax.axhline(y=median_time, color='orange', linestyle='--',
                  linewidth=2, alpha=0.7,
                  label=f'Median: {median_time:.0f}ms')
        
        # Add threshold lines
        ax.axhline(y=500, color='green', linestyle=':', alpha=0.5,
                  linewidth=1.5, label='Good Threshold (500ms)')
        
        # Formatting
        ax.set_xlabel('Request Number', fontsize=12, fontweight='bold')
        ax.set_ylabel('Response Time (ms)', fontsize=12, fontweight='bold')
        ax.set_title(f'Response Time Trend: {video["short_name"]}',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlim(0, 21)
        ax.set_ylim(bottom=0, top=max(max_time * 1.1, 600))
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', framealpha=0.9)
        
        # Add statistics text box
        stats_text = f'Statistics:\n'
        stats_text += f'  Min: {min_time:.0f}ms\n'
        stats_text += f'  Max: {max_time:.0f}ms\n'
        stats_text += f'  Range: {max_time - min_time:.0f}ms\n'
        stats_text += f'  Std Dev: ±{video_df["response_time_ms"].std():.0f}ms'
        
        ax.text(0.02, 0.98, stats_text,
               transform=ax.transAxes,
               fontsize=9,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(video['filename'], dpi=300, bbox_inches='tight')
        print(f"✓ Created: {video['filename']}")
        plt.close()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Generating Individual Video Trend Graphs")
    print("="*60 + "\n")
    
    create_individual_video_graphs()
    
    print("\n" + "="*60)
    print("✅ All individual video graphs created!")
    print("="*60 + "\n")


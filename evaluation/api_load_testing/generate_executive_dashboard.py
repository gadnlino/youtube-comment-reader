"""
Generate Executive Summary Dashboard for Academic Report

Creates a comprehensive one-page visual summary of all key findings.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'serif'

def create_executive_dashboard():
    """Create comprehensive executive summary dashboard."""
    # Load data
    df = pd.read_csv('multi_video_results_20251026_212004.csv')
    with open('multi_video_summary_20251026_212004.json', 'r') as f:
        summary = json.load(f)
    
    # Create figure with custom layout
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Title
    fig.suptitle('YouTube Comment Reader API - Multi-Video Performance Evaluation\n' + 
                'Executive Summary Dashboard',
                fontsize=18, fontweight='bold', y=0.98)
    
    # 1. Key Metrics Panel (top-left)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.axis('off')
    
    overall = summary['overall_stats']
    metrics_text = f"""
    KEY PERFORMANCE METRICS
    {'='*35}
    
    Total Requests:      {overall['total_requests']}
    Success Rate:        {overall['success_rate']:.1f}%
    
    Response Times:
      • Average:         {overall['avg_response_time']:.0f} ms
      • Median:          {overall['median_response_time']:.0f} ms
      • P95:             {overall['p95']:.0f} ms
      • P99:             {overall['p99']:.0f} ms
    
    Variability:
      • Std Deviation:   ±{overall['std_dev']:.0f} ms
      • Min:             {overall['min_response_time']:.0f} ms
      • Max:             {overall['max_response_time']:.0f} ms
    """
    
    ax1.text(0.05, 0.95, metrics_text, 
            transform=ax1.transAxes,
            fontsize=10,
            verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#ecf0f1', 
                     edgecolor='#2c3e50', linewidth=2))
    
    # 2. Test Configuration (top-middle)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.axis('off')
    
    config_text = f"""
    TEST CONFIGURATION
    {'='*35}
    
    Videos Tested:       {overall['videos_tested']}
    Requests/Video:      20
    
    Test Videos:
    1. Music Video
       Rick Astley - Never Gonna 
       Give You Up
       (High engagement, mixed 
       sentiment)
    
    2. Documentary
       Me at the zoo
       (Historical, nostalgic)
    
    3. Viral Music
       Gangnam Style
       (International, very high
       engagement)
    
    Test Date:          Oct 26, 2025
    Duration:           {overall['test_duration_seconds']:.1f}s
    """
    
    ax2.text(0.05, 0.95, config_text,
            transform=ax2.transAxes,
            fontsize=9,
            verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#e8f8f5',
                     edgecolor='#27ae60', linewidth=2))
    
    # 3. Performance Assessment (top-right)
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.axis('off')
    
    assessment_text = f"""
    PERFORMANCE ASSESSMENT
    {'='*35}
    
    Overall Rating:      ✓ GOOD
    
    ✓ Reliability:       Excellent
      100% success rate
    
    ✓ Avg Response:      Good
      430ms < 500ms threshold
    
    ✓ Consistency:       Good
      82% requests < 500ms
    
    ⚠ P99 Latency:       Attention
      One outlier (2696ms)
      Likely cold start
    
    ✓ Stability:         Excellent
      No degradation over time
    
    ✓ Content-Agnostic:  Yes
      Minimal variation by
      video type
    
    RECOMMENDATION:
    Production-ready with
    cold-start mitigation
    """
    
    ax3.text(0.05, 0.95, assessment_text,
            transform=ax3.transAxes,
            fontsize=9,
            verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#fef9e7',
                     edgecolor='#f39c12', linewidth=2))
    
    # 4. Response Time Distribution (middle-left)
    ax4 = fig.add_subplot(gs[1, :2])
    
    # Box plot
    video_data = []
    video_labels = []
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    
    for result in summary['video_results']:
        video_data.append(result['response_times'])
        video_labels.append(result['video_name'][:20] + '...')
    
    bp = ax4.boxplot(video_data, labels=video_labels, patch_artist=True,
                    showmeans=True)
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    
    ax4.axhline(y=500, color='orange', linestyle='--', alpha=0.7,
               label='Good (500ms)')
    ax4.axhline(y=1000, color='red', linestyle='--', alpha=0.7,
               label='Acceptable (1000ms)')
    
    ax4.set_ylabel('Response Time (ms)', fontweight='bold')
    ax4.set_title('Response Time Distribution by Video', fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.legend(loc='upper right')
    ax4.set_ylim(bottom=0)
    
    # 5. Success Rate Pie Chart (middle-right)
    ax5 = fig.add_subplot(gs[1, 2])
    
    success_data = [overall['successful_requests'], overall['failed_requests']]
    colors_pie = ['#27ae60', '#e74c3c']
    explode = (0.05, 0)
    
    wedges, texts, autotexts = ax5.pie(success_data, 
                                        labels=['Success', 'Failed'],
                                        autopct='%1.1f%%',
                                        colors=colors_pie,
                                        explode=explode,
                                        startangle=90,
                                        textprops={'fontweight': 'bold'})
    
    ax5.set_title('Request Success Rate', fontweight='bold', pad=20)
    
    # Add center text
    ax5.text(0, 0, f'{overall["success_rate"]:.0f}%\nSuccess',
            ha='center', va='center',
            fontsize=16, fontweight='bold')
    
    # 6. Temporal Performance (bottom-left, spanning 2 columns)
    ax6 = fig.add_subplot(gs[2, :2])
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['elapsed'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds()
    
    for content_type, color in [('Music', '#3498db'), ('Documentary', '#2ecc71')]:
        type_df = df[df['content_type'] == content_type]
        ax6.scatter(type_df['elapsed'], type_df['response_time_ms'],
                   c=color, s=50, alpha=0.6, label=content_type,
                   edgecolors='black', linewidth=0.3)
    
    ax6.axhline(y=overall['avg_response_time'], color='red',
               linestyle='--', alpha=0.7, label='Overall Mean')
    
    ax6.set_xlabel('Elapsed Time (seconds)', fontweight='bold')
    ax6.set_ylabel('Response Time (ms)', fontweight='bold')
    ax6.set_title('Response Time Evolution', fontweight='bold')
    ax6.grid(True, alpha=0.3)
    ax6.legend(loc='upper right')
    ax6.set_ylim(bottom=0)
    
    # 7. Video Comparison Table (bottom-right)
    ax7 = fig.add_subplot(gs[2, 2])
    ax7.axis('off')
    
    comparison_text = """
    VIDEO COMPARISON
    
    Video #1 (Music):
      Avg: 514ms
      ★ Highest avg
      ★ One outlier
    
    Video #2 (Doc):
      Avg: 368ms
      ★ Best performance
      ★ Most consistent
    
    Video #3 (Viral):
      Avg: 408ms
      ★ Good balance
      ★ Low variability
    
    CONCLUSION:
    Content type has
    minimal impact on
    performance
    """
    
    ax7.text(0.05, 0.95, comparison_text,
            transform=ax7.transAxes,
            fontsize=9,
            verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#ebf5fb',
                     edgecolor='#3498db', linewidth=2))
    
    # Add footer
    footer_text = ('API Endpoint: https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com/prod/video/comments  |  '
                  'Test Framework: Multi-Video Performance Benchmark v1.0  |  '
                  'Report Generated: October 27, 2025')
    
    fig.text(0.5, 0.01, footer_text,
            ha='center', fontsize=7, style='italic', color='gray')
    
    plt.savefig('executive_summary_dashboard.png', dpi=300, 
                bbox_inches='tight', facecolor='white')
    print("✓ Created: executive_summary_dashboard.png")
    plt.close()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Generating Executive Summary Dashboard")
    print("="*60 + "\n")
    
    create_executive_dashboard()
    
    print("\n" + "="*60)
    print("✅ Executive dashboard created!")
    print("="*60)
    print("\nThis one-page summary includes:")
    print("  • Key performance metrics")
    print("  • Test configuration details")
    print("  • Performance assessment")
    print("  • Response time distributions")
    print("  • Success rate visualization")
    print("  • Temporal performance chart")
    print("  • Video comparison summary")
    print("\nPerfect for presentations or report cover page!")
    print("="*60 + "\n")


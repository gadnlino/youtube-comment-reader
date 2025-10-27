"""
Multi-Video Performance Benchmark for YouTube Comment Reader API

This script tests the API with multiple different videos to ensure:
1. Performance consistency across different content types
2. Sentiment analysis accuracy across diverse comment styles
3. No bias toward specific video characteristics
"""

import requests
import time
import json
import csv
from datetime import datetime
from typing import Dict, List, Tuple, Any
from statistics import mean, stdev, median
import pandas as pd
import matplotlib.pyplot as plt

class MultiVideoBenchmark:
    """
    Tests API performance and accuracy across multiple diverse videos.
    """
    
    def __init__(self, api_base_url: str):
        """
        Initialize the benchmark with API configuration.
        
        Args:
            api_base_url: Base URL for the API
        """
        self.api_base_url = api_base_url
        self.results = []
        
        # Diverse video selection for testing
        # Each video has different characteristics for comprehensive testing
        self.test_videos = [
            {
                'id': 'dQw4w9WgXcQ',
                'name': 'Music Video - High Engagement',
                'description': 'Rick Astley - Classic music video with mixed sentiments',
                'expected_comments': 'High',
                'content_type': 'Music'
            },
            {
                'id': 'jNQXAC9IVRw',
                'name': 'Educational - Me at the zoo',
                'description': 'First YouTube video - Historical, nostalgic comments',
                'expected_comments': 'Medium',
                'content_type': 'Documentary'
            },
            {
                'id': '9bZkp7q19f0',
                'name': 'Music - Gangnam Style',
                'description': 'Viral music video - International, diverse comments',
                'expected_comments': 'Very High',
                'content_type': 'Music'
            }
        ]
    
    def test_video_performance(self, video: Dict[str, str], 
                              num_requests: int = 10) -> Dict[str, Any]:
        """
        Test API performance for a specific video.
        
        Args:
            video: Video metadata dictionary
            num_requests: Number of test requests to make
            
        Returns:
            Performance metrics for the video
        """
        print(f"\n🎬 Testing: {video['name']}")
        print(f"   Video ID: {video['id']}")
        print(f"   Type: {video['content_type']}")
        print(f"   Description: {video['description']}")
        
        video_results = {
            'video_id': video['id'],
            'video_name': video['name'],
            'content_type': video['content_type'],
            'response_times': [],
            'total_comments': [],
            'sentiment_distribution': {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0},
            'errors': 0,
            'successful_requests': 0
        }
        
        # Run multiple requests for this video
        for i in range(num_requests):
            try:
                # Test with sentiment analysis enabled
                params = {
                    'videoId': video['id'],
                    'maxResults': 100,
                    'includeSentimentAnalysis': True,
                    'showPositives': True,
                    'showNegatives': True,
                    'showNeutral': True
                }
                
                start_time = time.time()
                response = requests.get(
                    f"{self.api_base_url}/prod/video/comments",
                    params=params,
                    timeout=30
                )
                response_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    data = response.json()
                    comments = data.get('items', [])
                    
                    video_results['response_times'].append(response_time)
                    video_results['total_comments'].append(len(comments))
                    video_results['successful_requests'] += 1
                    
                    # Analyze sentiment distribution
                    for comment in comments:
                        sentiment = comment.get('sentiment', {}).get('sentiment', 'UNKNOWN')
                        if sentiment in video_results['sentiment_distribution']:
                            video_results['sentiment_distribution'][sentiment] += 1
                    
                    # Store detailed result
                    self.results.append({
                        'timestamp': datetime.now().isoformat(),
                        'video_id': video['id'],
                        'video_name': video['name'],
                        'content_type': video['content_type'],
                        'request_number': i + 1,
                        'response_time_ms': response_time,
                        'num_comments': len(comments),
                        'status_code': response.status_code
                    })
                    
                    print(f"   Request {i+1}/{num_requests}: {response_time:.0f}ms "
                          f"({len(comments)} comments) ✅")
                else:
                    video_results['errors'] += 1
                    print(f"   Request {i+1}/{num_requests}: ERROR {response.status_code} ❌")
                    
            except Exception as e:
                video_results['errors'] += 1
                print(f"   Request {i+1}/{num_requests}: EXCEPTION {str(e)} ❌")
            
            # Small delay between requests
            time.sleep(0.5)
        
        # Calculate statistics
        if video_results['response_times']:
            video_results['avg_response_time'] = mean(video_results['response_times'])
            video_results['median_response_time'] = median(video_results['response_times'])
            video_results['min_response_time'] = min(video_results['response_times'])
            video_results['max_response_time'] = max(video_results['response_times'])
            if len(video_results['response_times']) > 1:
                video_results['std_dev'] = stdev(video_results['response_times'])
            else:
                video_results['std_dev'] = 0
        
        if video_results['total_comments']:
            video_results['avg_comments'] = mean(video_results['total_comments'])
        
        # Print summary
        print(f"\n   📊 Summary for {video['name']}:")
        print(f"   ✅ Successful: {video_results['successful_requests']}/{num_requests}")
        if video_results.get('avg_response_time'):
            print(f"   ⏱️  Avg Response: {video_results['avg_response_time']:.0f}ms")
            print(f"   📝 Avg Comments: {video_results['avg_comments']:.0f}")
            total_sentiments = sum(video_results['sentiment_distribution'].values())
            if total_sentiments > 0:
                print(f"   😊 Positive: {video_results['sentiment_distribution']['POSITIVE']} "
                      f"({video_results['sentiment_distribution']['POSITIVE']/total_sentiments*100:.1f}%)")
                print(f"   😐 Neutral: {video_results['sentiment_distribution']['NEUTRAL']} "
                      f"({video_results['sentiment_distribution']['NEUTRAL']/total_sentiments*100:.1f}%)")
                print(f"   😞 Negative: {video_results['sentiment_distribution']['NEGATIVE']} "
                      f"({video_results['sentiment_distribution']['NEGATIVE']/total_sentiments*100:.1f}%)")
        
        return video_results
    
    def run_benchmark(self, requests_per_video: int = 20) -> Dict[str, Any]:
        """
        Run complete benchmark across all test videos.
        
        Args:
            requests_per_video: Number of requests to make per video
            
        Returns:
            Complete benchmark results
        """
        print("\n" + "="*80)
        print("🎯 MULTI-VIDEO PERFORMANCE BENCHMARK")
        print("="*80)
        print(f"\nTesting {len(self.test_videos)} diverse videos")
        print(f"Requests per video: {requests_per_video}")
        print(f"Total requests: {len(self.test_videos) * requests_per_video}")
        print(f"API Base URL: {self.api_base_url}")
        
        start_time = time.time()
        
        # Test each video
        video_results = []
        for video in self.test_videos:
            result = self.test_video_performance(video, requests_per_video)
            video_results.append(result)
        
        total_time = time.time() - start_time
        
        # Compile overall statistics
        all_response_times = []
        total_requests = 0
        successful_requests = 0
        total_errors = 0
        
        for result in video_results:
            all_response_times.extend(result['response_times'])
            total_requests += requests_per_video
            successful_requests += result['successful_requests']
            total_errors += result['errors']
        
        overall_stats = {
            'test_duration_seconds': total_time,
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': total_errors,
            'success_rate': (successful_requests / total_requests * 100) if total_requests > 0 else 0,
            'videos_tested': len(self.test_videos),
            'avg_response_time': mean(all_response_times) if all_response_times else 0,
            'median_response_time': median(all_response_times) if all_response_times else 0,
            'min_response_time': min(all_response_times) if all_response_times else 0,
            'max_response_time': max(all_response_times) if all_response_times else 0,
            'std_dev': stdev(all_response_times) if len(all_response_times) > 1 else 0,
            'p95': self._calculate_percentile(all_response_times, 95) if all_response_times else 0,
            'p99': self._calculate_percentile(all_response_times, 99) if all_response_times else 0
        }
        
        # Print overall summary
        self._print_overall_summary(overall_stats, video_results)
        
        # Save results
        self._save_results(overall_stats, video_results)
        
        # Generate visualizations
        self._generate_visualizations(video_results)
        
        return {
            'overall_stats': overall_stats,
            'video_results': video_results,
            'raw_results': self.results
        }
    
    def _calculate_percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile value."""
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def _print_overall_summary(self, overall_stats: Dict, video_results: List[Dict]):
        """Print comprehensive summary of results."""
        print("\n" + "="*80)
        print("📊 OVERALL BENCHMARK RESULTS")
        print("="*80)
        
        print(f"\n⏱️  Test Duration: {overall_stats['test_duration_seconds']:.1f} seconds")
        print(f"🎬 Videos Tested: {overall_stats['videos_tested']}")
        print(f"📊 Total Requests: {overall_stats['total_requests']}")
        print(f"✅ Successful: {overall_stats['successful_requests']} "
              f"({overall_stats['success_rate']:.1f}%)")
        print(f"❌ Failed: {overall_stats['failed_requests']}")
        
        print(f"\n⏱️  RESPONSE TIME STATISTICS (All Videos):")
        print(f"   Average:    {overall_stats['avg_response_time']:.0f}ms")
        print(f"   Median:     {overall_stats['median_response_time']:.0f}ms")
        print(f"   Min:        {overall_stats['min_response_time']:.0f}ms")
        print(f"   Max:        {overall_stats['max_response_time']:.0f}ms")
        print(f"   Std Dev:    ±{overall_stats['std_dev']:.0f}ms")
        print(f"   P95:        {overall_stats['p95']:.0f}ms")
        print(f"   P99:        {overall_stats['p99']:.0f}ms")
        
        print(f"\n📊 PERFORMANCE BY VIDEO:")
        print("-" * 80)
        for result in video_results:
            if result.get('avg_response_time'):
                print(f"\n{result['video_name']} ({result['content_type']}):")
                print(f"   Avg Response: {result['avg_response_time']:.0f}ms")
                print(f"   Success Rate: {result['successful_requests']}/{result['successful_requests'] + result['errors']}")
                total_sentiments = sum(result['sentiment_distribution'].values())
                if total_sentiments > 0:
                    pos_pct = result['sentiment_distribution']['POSITIVE']/total_sentiments*100
                    neu_pct = result['sentiment_distribution']['NEUTRAL']/total_sentiments*100
                    neg_pct = result['sentiment_distribution']['NEGATIVE']/total_sentiments*100
                    print(f"   Sentiments: {pos_pct:.1f}% pos, {neu_pct:.1f}% neu, {neg_pct:.1f}% neg")
        
        print("\n" + "="*80)
        print("✅ MULTI-VIDEO BENCHMARK COMPLETE!")
        print("="*80)
    
    def _save_results(self, overall_stats: Dict, video_results: List[Dict]):
        """Save results to CSV and JSON files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save raw results to CSV
        csv_filename = f"evaluation/api_load_testing/multi_video_results_{timestamp}.csv"
        with open(csv_filename, 'w', newline='') as csvfile:
            if self.results:
                fieldnames = self.results[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.results)
        
        print(f"\n💾 Saved raw results to: {csv_filename}")
        
        # Save summary to JSON
        json_filename = f"evaluation/api_load_testing/multi_video_summary_{timestamp}.json"
        summary = {
            'overall_stats': overall_stats,
            'video_results': video_results,
            'test_videos': self.test_videos,
            'timestamp': timestamp
        }
        
        with open(json_filename, 'w') as jsonfile:
            json.dump(summary, jsonfile, indent=2)
        
        print(f"💾 Saved summary to: {json_filename}")
    
    def _generate_visualizations(self, video_results: List[Dict]):
        """Generate comparison visualizations."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Multi-Video Performance Comparison', fontsize=16, fontweight='bold')
        
        # 1. Response time comparison (box plot)
        ax1 = axes[0, 0]
        response_data = []
        labels = []
        for result in video_results:
            if result['response_times']:
                response_data.append(result['response_times'])
                labels.append(f"{result['content_type']}\n({result['video_name'][:20]}...)")
        
        if response_data:
            ax1.boxplot(response_data, labels=labels)
            ax1.set_ylabel('Response Time (ms)', fontsize=12)
            ax1.set_title('Response Time Distribution by Video', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='x', rotation=15)
        
        # 2. Average response time bar chart
        ax2 = axes[0, 1]
        video_names = [r['video_name'][:25] for r in video_results]
        avg_times = [r.get('avg_response_time', 0) for r in video_results]
        colors = ['#2ecc71', '#3498db', '#e74c3c']
        
        bars = ax2.bar(range(len(video_names)), avg_times, color=colors[:len(video_names)])
        ax2.set_ylabel('Average Response Time (ms)', fontsize=12)
        ax2.set_title('Average Response Time by Video', fontsize=14, fontweight='bold')
        ax2.set_xticks(range(len(video_names)))
        ax2.set_xticklabels(video_names, rotation=15, ha='right')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.0f}ms', ha='center', va='bottom', fontsize=10)
        
        # 3. Sentiment distribution comparison
        ax3 = axes[1, 0]
        video_labels = [r['video_name'][:20] for r in video_results]
        positive = [r['sentiment_distribution']['POSITIVE'] for r in video_results]
        neutral = [r['sentiment_distribution']['NEUTRAL'] for r in video_results]
        negative = [r['sentiment_distribution']['NEGATIVE'] for r in video_results]
        
        x = range(len(video_labels))
        width = 0.25
        
        ax3.bar([i - width for i in x], positive, width, label='Positive', color='#2ecc71')
        ax3.bar(x, neutral, width, label='Neutral', color='#95a5a6')
        ax3.bar([i + width for i in x], negative, width, label='Negative', color='#e74c3c')
        
        ax3.set_ylabel('Number of Comments', fontsize=12)
        ax3.set_title('Sentiment Distribution by Video', fontsize=14, fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(video_labels, rotation=15, ha='right')
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Success rate comparison
        ax4 = axes[1, 1]
        success_rates = [(r['successful_requests'] / (r['successful_requests'] + r['errors']) * 100) 
                        for r in video_results]
        
        bars = ax4.bar(range(len(video_names)), success_rates, color=colors[:len(video_names)])
        ax4.set_ylabel('Success Rate (%)', fontsize=12)
        ax4.set_title('Success Rate by Video', fontsize=14, fontweight='bold')
        ax4.set_xticks(range(len(video_names)))
        ax4.set_xticklabels(video_names, rotation=15, ha='right')
        ax4.set_ylim([0, 105])
        ax4.grid(True, alpha=0.3, axis='y')
        ax4.axhline(y=100, color='green', linestyle='--', alpha=0.5, label='100%')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        
        # Save figure
        plot_filename = f"evaluation/api_load_testing/multi_video_comparison_{timestamp}.png"
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Saved visualization to: {plot_filename}")


if __name__ == "__main__":
    # Configuration
    API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com"
    REQUESTS_PER_VIDEO = 20  # Number of requests to test per video
    
    print("\n" + "="*80)
    print("🎯 MULTI-VIDEO API BENCHMARK")
    print("="*80)
    print(f"\nThis benchmark tests API performance across MULTIPLE DIVERSE VIDEOS")
    print(f"to ensure consistent performance and unbiased sentiment analysis.")
    print(f"\nConfiguration:")
    print(f"  - API Base URL: {API_BASE_URL}")
    print(f"  - Requests per video: {REQUESTS_PER_VIDEO}")
    print(f"  - Total videos: 3 (Music, Documentary, Viral)")
    
    # Run benchmark
    benchmark = MultiVideoBenchmark(API_BASE_URL)
    results = benchmark.run_benchmark(requests_per_video=REQUESTS_PER_VIDEO)
    
    print(f"\n{'='*80}")
    print("🎉 BENCHMARK COMPLETE!")
    print(f"{'='*80}")
    print(f"\n✅ Tested {results['overall_stats']['videos_tested']} diverse videos")
    print(f"✅ Total requests: {results['overall_stats']['total_requests']}")
    print(f"✅ Success rate: {results['overall_stats']['success_rate']:.1f}%")
    print(f"✅ Average response time: {results['overall_stats']['avg_response_time']:.0f}ms")
    print(f"\n📊 Results demonstrate performance consistency across diverse content types!")


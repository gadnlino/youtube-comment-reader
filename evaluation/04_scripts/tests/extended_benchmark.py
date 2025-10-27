"""
Extended Performance Benchmarking Script - More Comprehensive Testing

This script runs longer tests with more requests to evaluate:
- Long-term performance stability
- Performance degradation over time
- More accurate statistics with larger sample sizes

Usage:
    python extended_benchmark.py
"""

import requests
import time
import json
import statistics
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from datetime import datetime


class ExtendedAPIBenchmark:
    """Extended performance benchmark with more requests."""
    
    def __init__(self, api_base_url: str, video_id: str):
        self.api_base_url = api_base_url.rstrip('/')
        self.video_id = video_id
        self.results: List[Dict[str, Any]] = []
        
    def measure_request(
        self, 
        endpoint: str, 
        params: Dict[str, Any],
        test_name: str
    ) -> Dict[str, Any]:
        """Measure a single API request performance."""
        url = f"{self.api_base_url}{endpoint}"
        
        start_time = time.time()
        try:
            response = requests.get(url, params=params, timeout=120)
            elapsed_time = time.time() - start_time
            
            data = response.json() if response.status_code == 200 else {}
            comment_count = len(data.get('items', []))
            has_sentiment = any('sentiment' in item for item in data.get('items', []))
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'test_name': test_name,
                'status_code': response.status_code,
                'response_time_ms': elapsed_time * 1000,
                'comment_count': comment_count,
                'has_sentiment': has_sentiment,
                'success': response.status_code == 200
            }
            
            if test_name.startswith('Request'):
                req_num = int(test_name.split()[1])
                if req_num % 10 == 0:
                    print(f"  Progress: {req_num} requests completed ({elapsed_time*1000:.0f}ms)")
            
            return result
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            return {
                'timestamp': datetime.now().isoformat(),
                'test_name': test_name,
                'status_code': 0,
                'response_time_ms': elapsed_time * 1000,
                'comment_count': 0,
                'has_sentiment': False,
                'success': False,
                'error': str(e)
            }
    
    def test_extended_warm_performance(self, num_requests: int = 100) -> List[Dict[str, Any]]:
        """
        Test warm Lambda performance with many consecutive requests.
        
        Args:
            num_requests: Number of requests to make (default: 100)
            
        Returns:
            List of performance metrics
        """
        print(f"\n🔥 Testing Extended Warm Performance ({num_requests} requests)")
        print("   This will take several minutes...")
        
        results = []
        params = {
            'videoId': self.video_id,
            'part': 'snippet',
            'maxResults': 50,
            'showPositives': 'true',
            'showNegatives': 'true',
            'showNeutral': 'true'
        }
        
        start_time = time.time()
        
        for i in range(num_requests):
            result = self.measure_request(
                '/prod/video/comments', 
                params, 
                f'Request {i+1}'
            )
            results.append(result)
            
            # Small delay to avoid overwhelming the API
            if i < num_requests - 1:
                time.sleep(0.2)
        
        total_time = time.time() - start_time
        
        print(f"\n  ✅ Completed {num_requests} requests in {total_time:.1f}s")
        print(f"  📊 Average throughput: {num_requests/total_time:.2f} req/s")
        
        return results
    
    def test_sustained_load(self, duration_minutes: int = 5) -> List[Dict[str, Any]]:
        """
        Test sustained load over a longer period.
        
        Args:
            duration_minutes: How long to run the test in minutes
            
        Returns:
            List of performance metrics
        """
        print(f"\n⚡ Testing Sustained Load ({duration_minutes} minutes)")
        
        results = []
        params = {
            'videoId': self.video_id,
            'part': 'snippet',
            'maxResults': 50,
            'showPositives': 'true',
            'showNegatives': 'true',
            'showNeutral': 'true'
        }
        
        start_time = time.time()
        duration_seconds = duration_minutes * 60
        request_count = 0
        
        while time.time() - start_time < duration_seconds:
            request_count += 1
            
            result = self.measure_request(
                '/prod/video/comments',
                params,
                f'Sustained {request_count}'
            )
            results.append(result)
            
            if request_count % 20 == 0:
                elapsed = time.time() - start_time
                print(f"  Progress: {request_count} requests in {elapsed:.1f}s")
            
            # Small delay between requests
            time.sleep(0.5)
        
        total_time = time.time() - start_time
        throughput = request_count / total_time
        
        print(f"\n  ✅ Completed sustained load test")
        print(f"  📊 Total requests: {request_count}")
        print(f"  📊 Total time: {total_time:.1f}s")
        print(f"  📊 Throughput: {throughput:.2f} req/s")
        
        return results
    
    def test_different_batch_sizes_extended(self) -> List[Dict[str, Any]]:
        """Test performance with different batch sizes (10 requests each)."""
        print("\n📦 Testing Different Batch Sizes (10 requests per size)")
        
        results = []
        batch_sizes = [10, 25, 50, 100]
        
        for batch_size in batch_sizes:
            print(f"\n  Testing batch size: {batch_size}")
            
            for i in range(10):
                params = {
                    'videoId': self.video_id,
                    'part': 'snippet',
                    'maxResults': batch_size,
                    'showPositives': 'true',
                    'showNegatives': 'true',
                    'showNeutral': 'true'
                }
                
                result = self.measure_request(
                    '/prod/video/comments',
                    params,
                    f'Batch-{batch_size}-Request-{i+1}'
                )
                results.append(result)
                time.sleep(0.3)
            
            # Calculate average for this batch size
            batch_times = [r['response_time_ms'] for r in results[-10:] if r['success']]
            if batch_times:
                avg_time = statistics.mean(batch_times)
                print(f"    Avg: {avg_time:.0f}ms")
        
        return results
    
    def test_sentiment_overhead_extended(self, num_requests: int = 20) -> Dict[str, Any]:
        """
        Measure sentiment analysis overhead with more samples.
        
        Args:
            num_requests: Number of requests per scenario
            
        Returns:
            Dictionary with overhead statistics
        """
        print(f"\n🎭 Testing Sentiment Analysis Overhead ({num_requests} requests per scenario)")
        
        params_no_sentiment = {
            'videoId': self.video_id,
            'part': 'snippet',
            'maxResults': 50
        }
        
        params_with_sentiment = {
            'videoId': self.video_id,
            'part': 'snippet',
            'maxResults': 50,
            'showPositives': 'true',
            'showNegatives': 'true',
            'showNeutral': 'true'
        }
        
        # Test without sentiment
        print("  Testing WITHOUT sentiment...")
        no_sentiment_times = []
        for i in range(num_requests):
            result = self.measure_request(
                '/prod/video/comments',
                params_no_sentiment,
                f'NoSentiment-{i+1}'
            )
            if result['success']:
                no_sentiment_times.append(result['response_time_ms'])
            time.sleep(0.3)
        
        # Test with sentiment
        print("  Testing WITH sentiment...")
        with_sentiment_times = []
        for i in range(num_requests):
            result = self.measure_request(
                '/prod/video/comments',
                params_with_sentiment,
                f'WithSentiment-{i+1}'
            )
            if result['success']:
                with_sentiment_times.append(result['response_time_ms'])
            time.sleep(0.3)
        
        # Calculate statistics
        avg_no_sentiment = statistics.mean(no_sentiment_times) if no_sentiment_times else 0
        avg_with_sentiment = statistics.mean(with_sentiment_times) if with_sentiment_times else 0
        overhead = avg_with_sentiment - avg_no_sentiment
        overhead_percent = (overhead / avg_no_sentiment * 100) if avg_no_sentiment > 0 else 0
        
        print(f"\n  📊 Sentiment Analysis Overhead:")
        print(f"     Without sentiment: {avg_no_sentiment:.0f}ms (±{statistics.stdev(no_sentiment_times):.0f}ms)")
        print(f"     With sentiment:    {avg_with_sentiment:.0f}ms (±{statistics.stdev(with_sentiment_times):.0f}ms)")
        print(f"     Overhead:          {overhead:.0f}ms ({overhead_percent:.1f}%)")
        
        return {
            'avg_without_sentiment_ms': avg_no_sentiment,
            'stdev_without_sentiment_ms': statistics.stdev(no_sentiment_times) if len(no_sentiment_times) > 1 else 0,
            'avg_with_sentiment_ms': avg_with_sentiment,
            'stdev_with_sentiment_ms': statistics.stdev(with_sentiment_times) if len(with_sentiment_times) > 1 else 0,
            'overhead_ms': overhead,
            'overhead_percent': overhead_percent,
            'samples_without': len(no_sentiment_times),
            'samples_with': len(with_sentiment_times)
        }
    
    def run_extended_tests(self, num_requests: int = 100) -> pd.DataFrame:
        """
        Run extended performance tests.
        
        Args:
            num_requests: Number of requests for warm performance test
            
        Returns:
            DataFrame with all test results
        """
        print("=" * 80)
        print("🚀 YouTube Comment Reader API - EXTENDED Performance Benchmark")
        print("=" * 80)
        print(f"API: {self.api_base_url}")
        print(f"Video ID: {self.video_id}")
        print(f"Warm Performance Requests: {num_requests}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n⚠️  This will take 10-15 minutes to complete...")
        
        # Run tests
        warm_results = self.test_extended_warm_performance(num_requests)
        batch_results = self.test_different_batch_sizes_extended()
        sentiment_overhead = self.test_sentiment_overhead_extended(20)
        sustained_results = self.test_sustained_load(2)  # 2 minutes sustained
        
        # Combine results
        all_results = warm_results + batch_results + sustained_results
        self.results = all_results
        
        # Save detailed results
        df = pd.DataFrame(all_results)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f'extended_performance_results_{timestamp}.csv'
        df.to_csv(csv_filename, index=False)
        print(f"\n💾 Results saved to: {csv_filename}")
        
        # Generate comprehensive report
        self.generate_extended_report(df, sentiment_overhead)
        
        # Generate graphs
        self.generate_extended_graphs(df, timestamp)
        
        return df
    
    def generate_extended_report(
        self, 
        df: pd.DataFrame, 
        sentiment_overhead: Dict[str, Any]
    ):
        """Generate extended performance report."""
        print("\n" + "=" * 80)
        print("📊 EXTENDED PERFORMANCE SUMMARY")
        print("=" * 80)
        
        successful_requests = df[df['success'] == True]
        
        if len(successful_requests) > 0:
            response_times = successful_requests['response_time_ms']
            
            print(f"\n📈 Response Time Statistics ({len(successful_requests)} successful requests):")
            print(f"   Average:      {response_times.mean():.0f}ms")
            print(f"   Median:       {response_times.median():.0f}ms")
            print(f"   Std Dev:      {response_times.std():.0f}ms")
            print(f"   Minimum:      {response_times.min():.0f}ms")
            print(f"   Maximum:      {response_times.max():.0f}ms")
            print(f"   P50:          {response_times.quantile(0.50):.0f}ms")
            print(f"   P75:          {response_times.quantile(0.75):.0f}ms")
            print(f"   P90:          {response_times.quantile(0.90):.0f}ms")
            print(f"   P95:          {response_times.quantile(0.95):.0f}ms")
            print(f"   P99:          {response_times.quantile(0.99):.0f}ms")
        
        print(f"\n🎭 Sentiment Analysis:")
        print(f"   Overhead: {sentiment_overhead['overhead_ms']:.0f}ms "
              f"({sentiment_overhead['overhead_percent']:.1f}%)")
        print(f"   Samples: {sentiment_overhead['samples_without']} without, "
              f"{sentiment_overhead['samples_with']} with sentiment")
        
        print(f"\n✅ Success Rate:")
        success_rate = (len(successful_requests) / len(df)) * 100
        print(f"   {success_rate:.1f}% ({len(successful_requests)}/{len(df)})")
        
        print("\n" + "=" * 80)
    
    def generate_extended_graphs(self, df: pd.DataFrame, timestamp: str):
        """Generate comprehensive visualization graphs."""
        successful = df[df['success'] == True].copy()
        
        # Graph 1: Response time over all requests
        plt.figure(figsize=(16, 8))
        plt.subplot(2, 2, 1)
        plt.plot(range(len(successful)), successful['response_time_ms'], 
                marker='.', linestyle='-', linewidth=0.5, markersize=3, alpha=0.7)
        plt.xlabel('Request Number')
        plt.ylabel('Response Time (ms)')
        plt.title(f'Response Time Across {len(successful)} Requests')
        plt.grid(True, alpha=0.3)
        
        # Graph 2: Response time distribution (histogram)
        plt.subplot(2, 2, 2)
        plt.hist(successful['response_time_ms'], bins=50, edgecolor='black', alpha=0.7)
        plt.xlabel('Response Time (ms)')
        plt.ylabel('Frequency')
        plt.title('Response Time Distribution')
        plt.grid(True, alpha=0.3, axis='y')
        
        # Graph 3: Rolling average (window=10)
        plt.subplot(2, 2, 3)
        rolling_avg = successful['response_time_ms'].rolling(window=10).mean()
        plt.plot(range(len(rolling_avg)), rolling_avg, linewidth=2, color='red')
        plt.xlabel('Request Number')
        plt.ylabel('Response Time (ms)')
        plt.title('Rolling Average (window=10)')
        plt.grid(True, alpha=0.3)
        
        # Graph 4: Box plot by request groups
        plt.subplot(2, 2, 4)
        # Group every 20 requests
        successful['group'] = successful.index // 20
        successful.boxplot(column='response_time_ms', by='group', ax=plt.gca())
        plt.xlabel('Request Group (20 requests each)')
        plt.ylabel('Response Time (ms)')
        plt.title('Response Time Distribution by Groups')
        plt.suptitle('')  # Remove default title
        
        plt.tight_layout()
        filename = f'extended_performance_graphs_{timestamp}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n📊 Extended graphs saved: {filename}")
        plt.close()


def main():
    """Main function to run the extended benchmark."""
    
    # Configuration
    API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com"
    VIDEO_ID = "dQw4w9WgXcQ"
    NUM_REQUESTS = 100  # Change this to run more or fewer requests
    
    print("🎯 Extended Performance Benchmark Configuration:")
    print(f"   - Warm performance test: {NUM_REQUESTS} requests")
    print(f"   - Batch size test: 40 requests (10 per size)")
    print(f"   - Sentiment overhead: 40 requests (20 per scenario)")
    print(f"   - Sustained load: 2 minutes")
    print(f"   - Total estimated time: 10-15 minutes\n")
    
    # Create benchmark instance and run tests
    benchmark = ExtendedAPIBenchmark(API_BASE_URL, VIDEO_ID)
    results_df = benchmark.run_extended_tests(NUM_REQUESTS)
    
    print("\n✅ Extended benchmark completed!")
    print("   Check the generated CSV and PNG files for detailed results.")


if __name__ == "__main__":
    main()



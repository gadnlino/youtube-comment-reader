"""
Performance benchmarking script for YouTube Comment Reader API.

This script measures:
- Response times for different batch sizes
- Cold start vs warm Lambda performance
- Throughput (requests per second)
- Sentiment analysis overhead

Usage:
    python performance_benchmark.py

The script generates:
- Console output with metrics
- CSV file with detailed results
- Performance graphs (PNG files)
"""

import requests
import time
import json
import statistics
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from datetime import datetime


class APIPerformanceBenchmark:
    """
    Performance benchmark tool for YouTube Comment Reader API.
    
    Measures response times, throughput, and cold start performance
    for the complete YouTube comment fetching and sentiment analysis flow.
    """
    
    def __init__(self, api_base_url: str, youtube_api_key: str, video_id: str):
        """
        Initialize the benchmark tool.
        
        Args:
            api_base_url: Base URL of the API Gateway
            youtube_api_key: YouTube Data API key
            video_id: Test video ID to fetch comments from
        """
        self.api_base_url = api_base_url.rstrip('/')
        self.youtube_api_key = youtube_api_key
        self.video_id = video_id
        self.results: List[Dict[str, Any]] = []
        
    def measure_request(
        self, 
        endpoint: str, 
        params: Dict[str, Any],
        test_name: str
    ) -> Dict[str, Any]:
        """
        Measure a single API request performance.
        
        Args:
            endpoint: API endpoint path (e.g., '/prod/comments')
            params: Query parameters
            test_name: Name for this test
            
        Returns:
            Dictionary with performance metrics
        """
        url = f"{self.api_base_url}{endpoint}"
        
        # Measure request time
        start_time = time.time()
        try:
            response = requests.get(url, params=params, timeout=120)
            elapsed_time = time.time() - start_time
            
            # Parse response
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
            
            print(f"  ✓ {test_name}: {elapsed_time*1000:.0f}ms "
                  f"({comment_count} comments, sentiment={has_sentiment})")
            
            return result
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"  ✗ {test_name}: Error - {str(e)}")
            
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
    
    def test_cold_start(self) -> Dict[str, Any]:
        """
        Test Lambda cold start performance.
        
        Waits 15 minutes to ensure Lambda is cold, then makes first request.
        
        Returns:
            Performance metrics for cold start
        """
        print("\n🧊 Testing Cold Start Performance")
        print("   Waiting 15 minutes for Lambda to go cold...")
        print("   (You can skip this for testing by modifying the wait time)")
        
        # Wait for Lambda to go cold (comment out for quick testing)
        # time.sleep(900)  # 15 minutes
        
        params = {
            'videoId': self.video_id,
            'part': 'snippet',
            'maxResults': 50,
            'key': self.youtube_api_key,
            'showPositives': 'true',
            'showNegatives': 'true',
            'showNeutral': 'true'
        }
        
        return self.measure_request('/prod/video/comments', params, 'Cold Start')
    
    def test_warm_performance(self, num_requests: int = 10) -> List[Dict[str, Any]]:
        """
        Test warm Lambda performance with multiple consecutive requests.
        
        Args:
            num_requests: Number of requests to make
            
        Returns:
            List of performance metrics
        """
        print(f"\n🔥 Testing Warm Performance ({num_requests} requests)")
        
        results = []
        params = {
            'videoId': self.video_id,
            'part': 'snippet',
            'maxResults': 50,
            'key': self.youtube_api_key,
            'showPositives': 'true',
            'showNegatives': 'true',
            'showNeutral': 'true'
        }
        
        for i in range(num_requests):
            result = self.measure_request(
                '/prod/video/comments', 
                params, 
                f'Warm Request {i+1}'
            )
            results.append(result)
            time.sleep(0.5)  # Small delay between requests
            
        return results
    
    def test_batch_sizes(self) -> List[Dict[str, Any]]:
        """
        Test performance with different comment batch sizes.
        
        Returns:
            List of performance metrics for each batch size
        """
        print("\n📦 Testing Different Batch Sizes")
        
        results = []
        batch_sizes = [10, 25, 50, 100]
        
        for batch_size in batch_sizes:
            params = {
                'videoId': self.video_id,
                'part': 'snippet',
                'maxResults': batch_size,
                'key': self.youtube_api_key,
                'showPositives': 'true',
                'showNegatives': 'true',
                'showNeutral': 'true'
            }
            
            result = self.measure_request(
                '/prod/video/comments',
                params,
                f'Batch Size {batch_size}'
            )
            results.append(result)
            time.sleep(1)  # Wait between tests
            
        return results
    
    def test_sentiment_overhead(self) -> Dict[str, Any]:
        """
        Measure the overhead of sentiment analysis.
        
        Compares fetching comments with and without sentiment analysis.
        
        Returns:
            Dictionary comparing performance with/without sentiment
        """
        print("\n🎭 Testing Sentiment Analysis Overhead")
        
        params_no_sentiment = {
            'videoId': self.video_id,
            'part': 'snippet',
            'maxResults': 50,
            'key': self.youtube_api_key
        }
        
        params_with_sentiment = {
            'videoId': self.video_id,
            'part': 'snippet',
            'maxResults': 50,
            'key': self.youtube_api_key,
            'showPositives': 'true',
            'showNegatives': 'true',
            'showNeutral': 'true'
        }
        
        # Test without sentiment (3 requests for average)
        no_sentiment_times = []
        for i in range(3):
            result = self.measure_request(
                '/prod/video/comments',
                params_no_sentiment,
                f'Without Sentiment {i+1}'
            )
            no_sentiment_times.append(result['response_time_ms'])
            time.sleep(0.5)
        
        # Test with sentiment (3 requests for average)
        with_sentiment_times = []
        for i in range(3):
            result = self.measure_request(
                '/prod/video/comments',
                params_with_sentiment,
                f'With Sentiment {i+1}'
            )
            with_sentiment_times.append(result['response_time_ms'])
            time.sleep(0.5)
        
        avg_no_sentiment = statistics.mean(no_sentiment_times)
        avg_with_sentiment = statistics.mean(with_sentiment_times)
        overhead = avg_with_sentiment - avg_no_sentiment
        overhead_percent = (overhead / avg_no_sentiment) * 100
        
        print(f"\n  📊 Sentiment Analysis Overhead:")
        print(f"     Without sentiment: {avg_no_sentiment:.0f}ms")
        print(f"     With sentiment:    {avg_with_sentiment:.0f}ms")
        print(f"     Overhead:          {overhead:.0f}ms ({overhead_percent:.1f}%)")
        
        return {
            'avg_without_sentiment_ms': avg_no_sentiment,
            'avg_with_sentiment_ms': avg_with_sentiment,
            'overhead_ms': overhead,
            'overhead_percent': overhead_percent
        }
    
    def test_throughput(self, duration_seconds: int = 30) -> Dict[str, Any]:
        """
        Test maximum throughput (requests per second).
        
        Args:
            duration_seconds: How long to run the test
            
        Returns:
            Throughput metrics
        """
        print(f"\n⚡ Testing Throughput ({duration_seconds} seconds)")
        
        params = {
            'videoId': self.video_id,
            'part': 'snippet',
            'maxResults': 10,  # Small batch for throughput test
            'key': self.youtube_api_key
        }
        
        start_time = time.time()
        request_count = 0
        response_times = []
        
        while time.time() - start_time < duration_seconds:
            req_start = time.time()
            try:
                response = requests.get(
                    f"{self.api_base_url}/prod/video/comments",
                    params=params,
                    timeout=30
                )
                req_time = time.time() - req_start
                response_times.append(req_time * 1000)
                request_count += 1
                
                if request_count % 10 == 0:
                    print(f"  Progress: {request_count} requests...")
                    
            except Exception as e:
                print(f"  Error: {e}")
        
        total_time = time.time() - start_time
        avg_response_time = statistics.mean(response_times) if response_times else 0
        throughput = request_count / total_time
        
        print(f"\n  📈 Throughput Results:")
        print(f"     Total requests:     {request_count}")
        print(f"     Total time:         {total_time:.1f}s")
        print(f"     Throughput:         {throughput:.2f} requests/second")
        print(f"     Avg response time:  {avg_response_time:.0f}ms")
        
        return {
            'total_requests': request_count,
            'total_time_seconds': total_time,
            'throughput_rps': throughput,
            'avg_response_time_ms': avg_response_time
        }
    
    def run_all_tests(self) -> pd.DataFrame:
        """
        Run all performance tests.
        
        Returns:
            DataFrame with all test results
        """
        print("=" * 80)
        print("🚀 YouTube Comment Reader API - Performance Benchmark")
        print("=" * 80)
        print(f"API: {self.api_base_url}")
        print(f"Video ID: {self.video_id}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run tests
        # cold_start = self.test_cold_start()  # Skip for quick testing
        warm_results = self.test_warm_performance(10)
        batch_results = self.test_batch_sizes()
        sentiment_overhead = self.test_sentiment_overhead()
        throughput = self.test_throughput(30)
        
        # Combine results
        all_results = warm_results + batch_results
        self.results = all_results
        
        # Save detailed results
        df = pd.DataFrame(all_results)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f'performance_results_{timestamp}.csv'
        df.to_csv(csv_filename, index=False)
        print(f"\n💾 Results saved to: {csv_filename}")
        
        # Generate summary report
        self.generate_report(df, sentiment_overhead, throughput)
        
        return df
    
    def generate_report(
        self, 
        df: pd.DataFrame, 
        sentiment_overhead: Dict[str, Any],
        throughput: Dict[str, Any]
    ):
        """
        Generate performance report with graphs.
        
        Args:
            df: DataFrame with test results
            sentiment_overhead: Sentiment overhead metrics
            throughput: Throughput metrics
        """
        print("\n" + "=" * 80)
        print("📊 PERFORMANCE SUMMARY")
        print("=" * 80)
        
        # Calculate statistics
        successful_requests = df[df['success'] == True]
        if len(successful_requests) > 0:
            avg_response = successful_requests['response_time_ms'].mean()
            min_response = successful_requests['response_time_ms'].min()
            max_response = successful_requests['response_time_ms'].max()
            p95_response = successful_requests['response_time_ms'].quantile(0.95)
            p99_response = successful_requests['response_time_ms'].quantile(0.99)
            
            print(f"\n📈 Response Time Statistics:")
            print(f"   Average:  {avg_response:.0f}ms")
            print(f"   Minimum:  {min_response:.0f}ms")
            print(f"   Maximum:  {max_response:.0f}ms")
            print(f"   P95:      {p95_response:.0f}ms")
            print(f"   P99:      {p99_response:.0f}ms")
        
        print(f"\n🎭 Sentiment Analysis:")
        print(f"   Overhead: {sentiment_overhead['overhead_ms']:.0f}ms "
              f"({sentiment_overhead['overhead_percent']:.1f}%)")
        
        print(f"\n⚡ Throughput:")
        print(f"   {throughput['throughput_rps']:.2f} requests/second")
        
        print(f"\n✅ Success Rate:")
        success_rate = (len(successful_requests) / len(df)) * 100
        print(f"   {success_rate:.1f}% ({len(successful_requests)}/{len(df)})")
        
        print("\n" + "=" * 80)
        
        # Generate graphs
        self.generate_graphs(df, sentiment_overhead)
    
    def generate_graphs(self, df: pd.DataFrame, sentiment_overhead: Dict[str, Any]):
        """
        Generate performance visualization graphs.
        
        Args:
            df: DataFrame with test results
            sentiment_overhead: Sentiment overhead metrics
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Graph 1: Response time over requests
        plt.figure(figsize=(12, 6))
        successful = df[df['success'] == True]
        plt.plot(range(len(successful)), successful['response_time_ms'], 
                marker='o', linestyle='-', linewidth=1, markersize=4)
        plt.xlabel('Request Number')
        plt.ylabel('Response Time (ms)')
        plt.title('Response Time Across Requests')
        plt.grid(True, alpha=0.3)
        filename = f'response_time_graph_{timestamp}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n📊 Graph saved: {filename}")
        plt.close()
        
        # Graph 2: Batch size comparison
        batch_tests = df[df['test_name'].str.contains('Batch Size', na=False)]
        if len(batch_tests) > 0:
            plt.figure(figsize=(10, 6))
            batch_sizes = batch_tests['comment_count']
            response_times = batch_tests['response_time_ms']
            plt.bar(range(len(batch_sizes)), response_times)
            plt.xlabel('Batch Size')
            plt.ylabel('Response Time (ms)')
            plt.title('Performance vs Batch Size')
            plt.xticks(range(len(batch_sizes)), batch_sizes)
            plt.grid(True, alpha=0.3, axis='y')
            filename = f'batch_size_comparison_{timestamp}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"📊 Graph saved: {filename}")
            plt.close()


def main():
    """Main function to run the benchmark."""
    
    # Configuration - UPDATE THESE VALUES
    API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com"
    YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"  # Replace with your key
    VIDEO_ID = "dQw4w9WgXcQ"  # Replace with a real video ID
    
    print("⚠️  Make sure to update API_BASE_URL, YOUTUBE_API_KEY, and VIDEO_ID")
    print("    in the script before running!\n")
    
    # Create benchmark instance and run tests
    benchmark = APIPerformanceBenchmark(API_BASE_URL, YOUTUBE_API_KEY, VIDEO_ID)
    results_df = benchmark.run_all_tests()
    
    print("\n✅ Benchmark completed!")
    print("   Check the generated CSV and PNG files for detailed results.")


if __name__ == "__main__":
    main()


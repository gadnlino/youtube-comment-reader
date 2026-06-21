"""
Heavy Load Testing - 10,000+ Comments

This script tests the system with LARGE comment volumes to evaluate:
- Performance under heavy load
- System stability with high data volume
- Scalability limits
- Memory handling
- Processing time for large batches

Usage:
    python heavy_load_test.py
"""

import requests
import time
import json
import statistics
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from datetime import datetime


class HeavyLoadTester:
    """Heavy load testing with 10,000+ comments."""
    
    def __init__(self, api_base_url: str, video_id: str):
        self.api_base_url = api_base_url.rstrip('/')
        self.video_id = video_id
        self.results: List[Dict[str, Any]] = []
        
    def fetch_large_comment_batch(
        self, 
        batch_size: int, 
        with_sentiment: bool = True
    ) -> Dict[str, Any]:
        """
        Fetch a large batch of comments.
        
        Args:
            batch_size: Number of comments to request (max per request)
            with_sentiment: Whether to include sentiment analysis
        """
        params = {
            'videoId': self.video_id,
            'part': 'snippet',
            'maxResults': batch_size
        }
        
        if with_sentiment:
            params['showPositives'] = 'true'
            params['showNegatives'] = 'true'
            params['showNeutral'] = 'true'
        
        print(f"  Requesting {batch_size} comments (with_sentiment={with_sentiment})...")
        
        start_time = time.time()
        try:
            response = requests.get(
                f"{self.api_base_url}/prod/video/comments",
                params=params,
                timeout=300  # 5 minute timeout for large batches
            )
            elapsed_time = time.time() - start_time
            
            if response.status_code != 200:
                print(f"  ❌ Error: Status {response.status_code}")
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'response_time_ms': elapsed_time * 1000
                }
            
            data = response.json()
            items = data.get('items', [])
            
            # Count sentiments if present
            sentiments = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
            for item in items:
                sent = item.get('sentiment')
                if sent in sentiments:
                    sentiments[sent] += 1
            
            result = {
                'success': True,
                'status_code': response.status_code,
                'response_time_ms': elapsed_time * 1000,
                'requested_count': batch_size,
                'actual_count': len(items),
                'has_sentiment': with_sentiment,
                'sentiments': sentiments if with_sentiment else None,
                'time_per_comment_ms': (elapsed_time * 1000) / len(items) if items else 0
            }
            
            print(f"  ✅ Received {len(items)} comments in {elapsed_time:.2f}s")
            print(f"     Time per comment: {result['time_per_comment_ms']:.2f}ms")
            if with_sentiment:
                print(f"     Sentiments: {sentiments}")
            
            return result
            
        except requests.Timeout:
            elapsed_time = time.time() - start_time
            print(f"  ❌ Timeout after {elapsed_time:.2f}s")
            return {
                'success': False,
                'status_code': 0,
                'response_time_ms': elapsed_time * 1000,
                'error': 'Timeout'
            }
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"  ❌ Exception: {str(e)}")
            return {
                'success': False,
                'status_code': 0,
                'response_time_ms': elapsed_time * 1000,
                'error': str(e)
            }
    
    def test_incremental_batch_sizes(self) -> List[Dict[str, Any]]:
        """
        Test with incrementally larger batch sizes to find limits.
        
        Batch sizes: 100, 500, 1000, 2000, 5000, 10000
        """
        print("\n" + "=" * 80)
        print("📦 TESTING INCREMENTAL BATCH SIZES")
        print("=" * 80)
        print("Testing with increasing comment counts to find performance limits...\n")
        
        # Note: YouTube API typically limits to ~100 comments per request
        # But we're testing what our system can handle
        batch_sizes = [100, 500, 1000, 2000, 5000, 10000]
        results = []
        
        for batch_size in batch_sizes:
            print(f"\n🔵 Test {len(results)+1}: Batch size = {batch_size} comments")
            print("-" * 60)
            
            # Test with sentiment
            result = self.fetch_large_comment_batch(batch_size, with_sentiment=True)
            result['test_name'] = f'BatchSize_{batch_size}_WithSentiment'
            result['batch_size'] = batch_size
            results.append(result)
            
            # Wait between tests
            time.sleep(2)
            
            # If we got an error or timeout, stop increasing
            if not result['success']:
                print(f"\n⚠️  Stopping at {batch_size} comments due to error/timeout")
                break
            
            # If response time > 60 seconds, warn
            if result['response_time_ms'] > 60000:
                print(f"\n⚠️  Response time exceeds 60 seconds. This may be the practical limit.")
        
        return results
    
    def test_multiple_requests_to_reach_10k(self) -> List[Dict[str, Any]]:
        """
        Make multiple requests to process 10,000 comments total.
        
        Strategy: Make 100 requests of 100 comments each = 10,000 total
        """
        print("\n" + "=" * 80)
        print("🚀 TESTING 10,000 COMMENTS VIA MULTIPLE REQUESTS")
        print("=" * 80)
        print("Making 100 requests of 100 comments each = 10,000 total comments\n")
        
        target_total = 10000
        comments_per_request = 100
        num_requests = target_total // comments_per_request
        
        results = []
        total_comments = 0
        total_time = 0
        
        start_overall = time.time()
        
        for i in range(num_requests):
            if i % 10 == 0:
                print(f"\n🔄 Progress: {i}/{num_requests} requests ({total_comments:,} comments processed)")
            
            result = self.fetch_large_comment_batch(
                comments_per_request, 
                with_sentiment=True
            )
            result['test_name'] = f'Request_{i+1}_of_{num_requests}'
            result['cumulative_comments'] = total_comments + result.get('actual_count', 0)
            results.append(result)
            
            if result['success']:
                total_comments += result.get('actual_count', 0)
                total_time += result['response_time_ms']
            
            # Small delay to avoid overwhelming the system
            time.sleep(0.5)
            
            # Stop if we hit errors
            if not result['success']:
                print(f"\n⚠️  Stopping due to error at request {i+1}")
                break
        
        overall_time = time.time() - start_overall
        
        print(f"\n" + "=" * 80)
        print("📊 OVERALL STATISTICS")
        print("=" * 80)
        print(f"Total Requests: {len(results)}")
        print(f"Successful: {sum(1 for r in results if r['success'])}")
        print(f"Failed: {sum(1 for r in results if not r['success'])}")
        print(f"Total Comments Processed: {total_comments:,}")
        print(f"Total Time: {overall_time:.2f}s ({overall_time/60:.2f} minutes)")
        print(f"Average per Request: {total_time/len(results):.0f}ms")
        print(f"Comments per Second: {total_comments/overall_time:.2f}")
        print(f"Time per Comment: {(overall_time*1000)/total_comments:.2f}ms")
        
        return results
    
    def test_sustained_heavy_load(self, duration_minutes: int = 10) -> List[Dict[str, Any]]:
        """
        Test sustained heavy load over extended period.
        
        Args:
            duration_minutes: How long to run (default: 10 minutes)
        """
        print("\n" + "=" * 80)
        print(f"⚡ SUSTAINED HEAVY LOAD TEST ({duration_minutes} minutes)")
        print("=" * 80)
        print(f"Continuously processing comments for {duration_minutes} minutes...\n")
        
        results = []
        total_comments = 0
        start_time = time.time()
        duration_seconds = duration_minutes * 60
        request_num = 0
        
        while time.time() - start_time < duration_seconds:
            request_num += 1
            
            result = self.fetch_large_comment_batch(100, with_sentiment=True)
            result['test_name'] = f'SustainedLoad_Request_{request_num}'
            result['elapsed_time_s'] = time.time() - start_time
            results.append(result)
            
            if result['success']:
                total_comments += result.get('actual_count', 0)
            
            # Progress update every 10 requests
            if request_num % 10 == 0:
                elapsed = time.time() - start_time
                rate = total_comments / elapsed if elapsed > 0 else 0
                print(f"  Progress: {request_num} requests, {total_comments:,} comments, "
                      f"{elapsed:.1f}s, {rate:.1f} comments/s")
            
            time.sleep(0.5)
        
        total_time = time.time() - start_time
        
        print(f"\n📊 Sustained Load Results:")
        print(f"   Duration: {total_time:.1f}s ({total_time/60:.1f} minutes)")
        print(f"   Total Requests: {len(results)}")
        print(f"   Total Comments: {total_comments:,}")
        print(f"   Average Rate: {total_comments/total_time:.2f} comments/second")
        
        return results
    
    def analyze_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze and summarize test results."""
        successful = [r for r in results if r.get('success', False)]
        failed = [r for r in results if not r.get('success', True)]
        
        if not successful:
            print("\n❌ No successful requests to analyze")
            return {}
        
        response_times = [r['response_time_ms'] for r in successful]
        comments_processed = [r.get('actual_count', 0) for r in successful]
        time_per_comment = [r.get('time_per_comment_ms', 0) for r in successful if r.get('time_per_comment_ms', 0) > 0]
        
        analysis = {
            'total_requests': len(results),
            'successful_requests': len(successful),
            'failed_requests': len(failed),
            'success_rate_pct': (len(successful) / len(results) * 100) if results else 0,
            'total_comments': sum(comments_processed),
            'avg_response_time_ms': statistics.mean(response_times),
            'median_response_time_ms': statistics.median(response_times),
            'min_response_time_ms': min(response_times),
            'max_response_time_ms': max(response_times),
            'p95_response_time_ms': statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else max(response_times),
            'avg_time_per_comment_ms': statistics.mean(time_per_comment) if time_per_comment else 0,
            'total_processing_time_s': sum(response_times) / 1000
        }
        
        return analysis
    
    def generate_report(self, all_results: Dict[str, List], analyses: Dict[str, Dict]):
        """Generate comprehensive test report."""
        print("\n" + "=" * 80)
        print("📊 HEAVY LOAD TEST - COMPREHENSIVE REPORT")
        print("=" * 80)
        
        # Summary for each test type
        for test_name, results in all_results.items():
            if not results:
                continue
                
            print(f"\n{'='*80}")
            print(f"🔷 {test_name}")
            print(f"{'='*80}")
            
            analysis = analyses.get(test_name, {})
            
            if analysis:
                print(f"\n📈 Statistics:")
                print(f"   Total Requests:        {analysis['total_requests']}")
                print(f"   Successful:            {analysis['successful_requests']}")
                print(f"   Failed:                {analysis['failed_requests']}")
                print(f"   Success Rate:          {analysis['success_rate_pct']:.1f}%")
                print(f"   Total Comments:        {analysis['total_comments']:,}")
                print(f"   Avg Response Time:     {analysis['avg_response_time_ms']:.0f}ms")
                print(f"   Median Response Time:  {analysis['median_response_time_ms']:.0f}ms")
                print(f"   Min Response Time:     {analysis['min_response_time_ms']:.0f}ms")
                print(f"   Max Response Time:     {analysis['max_response_time_ms']:.0f}ms")
                print(f"   P95 Response Time:     {analysis['p95_response_time_ms']:.0f}ms")
                print(f"   Time per Comment:      {analysis['avg_time_per_comment_ms']:.2f}ms")
                print(f"   Total Processing Time: {analysis['total_processing_time_s']:.1f}s")
        
        print("\n" + "=" * 80)
    
    def save_results(self, all_results: Dict[str, List], analyses: Dict[str, Dict]):
        """Save results to files."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Combine all results
        combined_results = []
        for test_name, results in all_results.items():
            for r in results:
                r['test_type'] = test_name
                combined_results.append(r)
        
        # Save to CSV
        if combined_results:
            df = pd.DataFrame(combined_results)
            csv_filename = f'heavy_load_test_results_{timestamp}.csv'
            df.to_csv(csv_filename, index=False)
            print(f"\n💾 Results saved to: {csv_filename}")
        
        # Save analysis to JSON
        json_filename = f'heavy_load_test_analysis_{timestamp}.json'
        with open(json_filename, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'analyses': analyses,
                'summary': {
                    'total_tests': sum(len(r) for r in all_results.values()),
                    'total_comments': sum(a.get('total_comments', 0) for a in analyses.values())
                }
            }, f, indent=2)
        print(f"💾 Analysis saved to: {json_filename}")
    
    def run_heavy_load_tests(self):
        """Run all heavy load tests."""
        print("=" * 80)
        print("🔥 HEAVY LOAD TESTING - 10,000+ COMMENTS")
        print("=" * 80)
        print(f"API: {self.api_base_url}")
        print(f"Video ID: {self.video_id}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n⚠️  This will take 15-30 minutes to complete...")
        print("=" * 80)
        
        all_results = {}
        analyses = {}
        
        # Test 1: Incremental batch sizes
        print("\n\n")
        incremental_results = self.test_incremental_batch_sizes()
        all_results['Incremental_Batch_Sizes'] = incremental_results
        analyses['Incremental_Batch_Sizes'] = self.analyze_results(incremental_results)
        
        # Test 2: Multiple requests to reach 10K
        print("\n\n")
        multiple_results = self.test_multiple_requests_to_reach_10k()
        all_results['Multiple_Requests_10K'] = multiple_results
        analyses['Multiple_Requests_10K'] = self.analyze_results(multiple_results)
        
        # Test 3: Sustained heavy load (optional - takes 10 minutes)
        # Uncomment to run:
        # print("\n\n")
        # sustained_results = self.test_sustained_heavy_load(10)
        # all_results['Sustained_Heavy_Load'] = sustained_results
        # analyses['Sustained_Heavy_Load'] = self.analyze_results(sustained_results)
        
        # Generate comprehensive report
        self.generate_report(all_results, analyses)
        
        # Save results
        self.save_results(all_results, analyses)
        
        print("\n" + "=" * 80)
        print("✅ HEAVY LOAD TESTING COMPLETE!")
        print("=" * 80)


def main():
    """Main function to run heavy load tests."""
    
    # Configuration
    API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com"
    VIDEO_ID = "dQw4w9WgXcQ"
    
    print("\n⚠️  WARNING: This test will make many API requests!")
    print("   - YouTube API has quota limits")
    print("   - Test will take 15-30 minutes")
    print("   - System will be under heavy load\n")
    
    input("Press Enter to continue or Ctrl+C to cancel...")
    
    # Run tests
    tester = HeavyLoadTester(API_BASE_URL, VIDEO_ID)
    tester.run_heavy_load_tests()


if __name__ == "__main__":
    main()



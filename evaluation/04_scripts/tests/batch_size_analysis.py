"""
Batch Size Analysis - Testing API Performance with Different Comment Counts

This script tests how response time varies with different batch sizes
to understand scalability characteristics of the API.
"""

import requests
import time
import json
import csv
from datetime import datetime
from typing import Dict, List, Any
from statistics import mean, median, stdev
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class BatchSizeAnalyzer:
    """
    Tests API performance across different batch sizes.
    """
    
    def __init__(self, api_base_url: str, video_id: str):
        """
        Initialize the batch size analyzer.
        
        Args:
            api_base_url: Base URL for the API
            video_id: Video ID to test with
        """
        self.api_base_url = api_base_url
        self.video_id = video_id
        self.results = []
        
        # Test different batch sizes from small to large
        self.batch_sizes = [10, 25, 50, 75, 100, 150, 200, 300, 500]
        self.requests_per_size = 10  # Number of requests for each batch size
    
    def test_batch_size(self, batch_size: int) -> Dict[str, Any]:
        """
        Test API performance with a specific batch size.
        
        Args:
            batch_size: Number of comments to request
            
        Returns:
            Performance metrics for this batch size
        """
        print(f"\n📊 Testing batch size: {batch_size} comments")
        print(f"   Running {self.requests_per_size} requests...")
        
        batch_results = {
            'batch_size': batch_size,
            'response_times': [],
            'actual_comments': [],
            'time_per_comment': [],
            'errors': 0,
            'successful_requests': 0
        }
        
        for i in range(self.requests_per_size):
            try:
                params = {
                    'videoId': self.video_id,
                    'maxResults': batch_size,
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
                response_time = (time.time() - start_time) * 1000  # to ms
                
                if response.status_code == 200:
                    data = response.json()
                    comments = data.get('items', [])
                    actual_count = len(comments)
                    
                    batch_results['response_times'].append(response_time)
                    batch_results['actual_comments'].append(actual_count)
                    batch_results['time_per_comment'].append(response_time / actual_count if actual_count > 0 else 0)
                    batch_results['successful_requests'] += 1
                    
                    # Store detailed result
                    self.results.append({
                        'timestamp': datetime.now().isoformat(),
                        'batch_size': batch_size,
                        'request_number': i + 1,
                        'response_time_ms': response_time,
                        'actual_comments': actual_count,
                        'time_per_comment_ms': response_time / actual_count if actual_count > 0 else 0,
                        'status_code': response.status_code
                    })
                    
                    print(f"   Request {i+1}/{self.requests_per_size}: {response_time:.0f}ms "
                          f"({actual_count} comments, {response_time/actual_count:.1f}ms/comment) ✅")
                else:
                    batch_results['errors'] += 1
                    print(f"   Request {i+1}/{self.requests_per_size}: ERROR {response.status_code} ❌")
                    
            except Exception as e:
                batch_results['errors'] += 1
                print(f"   Request {i+1}/{self.requests_per_size}: EXCEPTION {str(e)} ❌")
            
            # Small delay between requests
            time.sleep(0.3)
        
        # Calculate statistics
        if batch_results['response_times']:
            batch_results['avg_response_time'] = mean(batch_results['response_times'])
            batch_results['median_response_time'] = median(batch_results['response_times'])
            batch_results['min_response_time'] = min(batch_results['response_times'])
            batch_results['max_response_time'] = max(batch_results['response_times'])
            if len(batch_results['response_times']) > 1:
                batch_results['std_dev'] = stdev(batch_results['response_times'])
            else:
                batch_results['std_dev'] = 0
            
            batch_results['avg_time_per_comment'] = mean(batch_results['time_per_comment'])
            batch_results['avg_actual_comments'] = mean(batch_results['actual_comments'])
        
        # Print summary
        print(f"\n   📊 Summary for batch size {batch_size}:")
        print(f"   ✅ Successful: {batch_results['successful_requests']}/{self.requests_per_size}")
        if batch_results.get('avg_response_time'):
            print(f"   ⏱️  Avg Response: {batch_results['avg_response_time']:.0f}ms")
            print(f"   📝 Avg Comments: {batch_results['avg_actual_comments']:.0f}")
            print(f"   ⚡ Avg Time/Comment: {batch_results['avg_time_per_comment']:.2f}ms")
        
        return batch_results
    
    def run_analysis(self) -> List[Dict[str, Any]]:
        """
        Run complete batch size analysis.
        
        Returns:
            List of results for each batch size
        """
        print("\n" + "="*80)
        print("📊 BATCH SIZE ANALYSIS - API PERFORMANCE")
        print("="*80)
        print(f"\nTesting {len(self.batch_sizes)} different batch sizes")
        print(f"Batch sizes: {self.batch_sizes}")
        print(f"Requests per size: {self.requests_per_size}")
        print(f"Total requests: {len(self.batch_sizes) * self.requests_per_size}")
        print(f"API: {self.api_base_url}")
        print(f"Video ID: {self.video_id}")
        
        start_time = time.time()
        
        batch_summaries = []
        for batch_size in self.batch_sizes:
            summary = self.test_batch_size(batch_size)
            batch_summaries.append(summary)
        
        total_time = time.time() - start_time
        
        # Print overall summary
        self._print_overall_summary(batch_summaries, total_time)
        
        # Save results
        self._save_results(batch_summaries)
        
        # Generate visualizations
        self._generate_visualizations(batch_summaries)
        
        return batch_summaries
    
    def _print_overall_summary(self, summaries: List[Dict], total_time: float):
        """Print comprehensive summary of all batch size tests."""
        print("\n" + "="*80)
        print("📊 OVERALL BATCH SIZE ANALYSIS RESULTS")
        print("="*80)
        
        print(f"\n⏱️  Total Test Duration: {total_time:.1f} seconds")
        print(f"📊 Batch Sizes Tested: {len(summaries)}")
        print(f"🔢 Total Requests: {len(self.results)}")
        
        successful = sum(s['successful_requests'] for s in summaries)
        total_requests = len(self.batch_sizes) * self.requests_per_size
        print(f"✅ Success Rate: {successful}/{total_requests} ({successful/total_requests*100:.1f}%)")
        
        print(f"\n📈 PERFORMANCE BY BATCH SIZE:")
        print("-" * 80)
        print(f"{'Batch Size':<12} {'Avg Time':<12} {'Time/Comment':<15} {'Throughput':<15} {'Success':<10}")
        print("-" * 80)
        
        for summary in summaries:
            if summary.get('avg_response_time'):
                batch_size = summary['batch_size']
                avg_time = summary['avg_response_time']
                time_per = summary['avg_time_per_comment']
                throughput = summary['avg_actual_comments'] / (avg_time / 1000)  # comments per second
                success = f"{summary['successful_requests']}/{self.requests_per_size}"
                
                print(f"{batch_size:<12} {avg_time:<12.0f} {time_per:<15.2f} {throughput:<15.1f} {success:<10}")
        
        print("-" * 80)
        
        # Key findings
        print(f"\n🔍 KEY FINDINGS:")
        
        # Find optimal batch size (best time per comment)
        valid_summaries = [s for s in summaries if s.get('avg_time_per_comment')]
        if valid_summaries:
            best_efficiency = min(valid_summaries, key=lambda x: x['avg_time_per_comment'])
            print(f"   ⚡ Most Efficient Batch Size: {best_efficiency['batch_size']} comments")
            print(f"      ({best_efficiency['avg_time_per_comment']:.2f}ms per comment)")
            
            fastest_batch = min(valid_summaries, key=lambda x: x['avg_response_time'])
            print(f"   🚀 Fastest Overall: {fastest_batch['batch_size']} comments")
            print(f"      ({fastest_batch['avg_response_time']:.0f}ms total)")
            
            # Calculate if there's a linear relationship
            batch_sizes = [s['batch_size'] for s in valid_summaries]
            response_times = [s['avg_response_time'] for s in valid_summaries]
            
            correlation = np.corrcoef(batch_sizes, response_times)[0, 1]
            print(f"   📊 Correlation (batch size vs time): {correlation:.3f}")
            
            if correlation > 0.8:
                print(f"      → Strong positive correlation (near-linear scaling)")
            elif correlation > 0.5:
                print(f"      → Moderate positive correlation")
            else:
                print(f"      → Weak correlation (sub-linear scaling ✅)")
        
        print("\n" + "="*80)
    
    def _save_results(self, summaries: List[Dict]):
        """Save results to CSV and JSON files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results to CSV
        csv_filename = f"evaluation/api_load_testing/batch_size_analysis_{timestamp}.csv"
        with open(csv_filename, 'w', newline='') as csvfile:
            if self.results:
                fieldnames = self.results[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.results)
        
        print(f"\n💾 Saved detailed results to: {csv_filename}")
        
        # Save summary to JSON
        json_filename = f"evaluation/api_load_testing/batch_size_summary_{timestamp}.json"
        summary_data = {
            'test_config': {
                'batch_sizes': self.batch_sizes,
                'requests_per_size': self.requests_per_size,
                'video_id': self.video_id,
                'api_url': self.api_base_url
            },
            'summaries': summaries,
            'timestamp': timestamp
        }
        
        with open(json_filename, 'w') as jsonfile:
            json.dump(summary_data, jsonfile, indent=2)
        
        print(f"💾 Saved summary to: {json_filename}")
    
    def _generate_visualizations(self, summaries: List[Dict]):
        """Generate comprehensive visualizations."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        valid_summaries = [s for s in summaries if s.get('avg_response_time')]
        if not valid_summaries:
            print("⚠️  No valid data for visualization")
            return
        
        # Create figure with multiple subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Análise de Tamanho de Lote - Performance da API', 
                    fontsize=14, fontweight='bold')
        
        batch_sizes = [s['batch_size'] for s in valid_summaries]
        avg_times = [s['avg_response_time'] for s in valid_summaries]
        time_per_comment = [s['avg_time_per_comment'] for s in valid_summaries]
        
        # 1. Response Time vs Batch Size
        ax1 = axes[0, 0]
        ax1.plot(batch_sizes, avg_times, 'o-', color='#3498db', linewidth=2, markersize=8)
        
        # Add trend line
        z = np.polyfit(batch_sizes, avg_times, 1)
        p = np.poly1d(z)
        ax1.plot(batch_sizes, p(batch_sizes), "r--", alpha=0.6, linewidth=1.5,
                label=f'Tendência Linear: y={z[0]:.2f}x+{z[1]:.0f}')
        
        ax1.set_xlabel('Tamanho do Lote (número de comentários)', fontweight='bold')
        ax1.set_ylabel('Tempo de Resposta Médio (ms)', fontweight='bold')
        ax1.set_title('(A) Tempo de Resposta vs Tamanho do Lote', fontweight='bold', loc='left')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # 2. Time per Comment vs Batch Size
        ax2 = axes[0, 1]
        ax2.plot(batch_sizes, time_per_comment, 's-', color='#2ecc71', linewidth=2, markersize=8)
        ax2.axhline(y=np.mean(time_per_comment), color='red', linestyle='--', 
                   label=f'Média: {np.mean(time_per_comment):.2f}ms', alpha=0.6)
        
        ax2.set_xlabel('Tamanho do Lote (número de comentários)', fontweight='bold')
        ax2.set_ylabel('Tempo por Comentário (ms)', fontweight='bold')
        ax2.set_title('(B) Eficiência de Processamento vs Tamanho do Lote', fontweight='bold', loc='left')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # 3. Throughput (comments per second)
        ax3 = axes[1, 0]
        throughput = [s['avg_actual_comments'] / (s['avg_response_time'] / 1000) 
                     for s in valid_summaries]
        
        bars = ax3.bar(range(len(batch_sizes)), throughput, color='#e74c3c', alpha=0.7, edgecolor='black')
        ax3.set_xticks(range(len(batch_sizes)))
        ax3.set_xticklabels(batch_sizes, rotation=45)
        ax3.set_xlabel('Tamanho do Lote', fontweight='bold')
        ax3.set_ylabel('Taxa de Processamento (coments/seg)', fontweight='bold')
        ax3.set_title('(C) Taxa de Processamento por Tamanho de Lote', fontweight='bold', loc='left')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for i, (bar, val) in enumerate(zip(bars, throughput)):
            ax3.text(bar.get_x() + bar.get_width()/2, val + 1, 
                    f'{val:.0f}', ha='center', va='bottom', fontsize=8)
        
        # 4. Scaling Efficiency (ideal vs actual)
        ax4 = axes[1, 1]
        
        # Ideal linear scaling (from smallest batch)
        if batch_sizes and avg_times:
            base_time = avg_times[0]
            base_size = batch_sizes[0]
            ideal_times = [(size / base_size) * base_time for size in batch_sizes]
            
            ax4.plot(batch_sizes, avg_times, 'o-', color='#3498db', linewidth=2, 
                    markersize=8, label='Tempo Real')
            ax4.plot(batch_sizes, ideal_times, 's--', color='gray', linewidth=1.5, 
                    markersize=6, label='Escalamento Linear Ideal', alpha=0.6)
            
            ax4.set_xlabel('Tamanho do Lote', fontweight='bold')
            ax4.set_ylabel('Tempo de Resposta (ms)', fontweight='bold')
            ax4.set_title('(D) Escalamento Real vs Ideal', fontweight='bold', loc='left')
            ax4.grid(True, alpha=0.3)
            ax4.legend()
        
        plt.tight_layout()
        
        # Save figure
        filename = f"evaluation/api_load_testing/batch_size_analysis_{timestamp}.png"
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.close()
        
        print(f"📊 Saved visualization to: {filename}")


if __name__ == "__main__":
    # Configuration
    API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com"
    VIDEO_ID = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
    
    print("\n" + "="*80)
    print("🎯 BATCH SIZE PERFORMANCE ANALYSIS")
    print("="*80)
    print(f"\nThis test analyzes how API performance varies with different batch sizes")
    print(f"to understand optimal request sizing and scalability characteristics.")
    
    # Run analysis
    analyzer = BatchSizeAnalyzer(API_BASE_URL, VIDEO_ID)
    results = analyzer.run_analysis()
    
    print(f"\n{'='*80}")
    print("🎉 BATCH SIZE ANALYSIS COMPLETE!")
    print(f"{'='*80}")
    print(f"\n✅ Tested {len(analyzer.batch_sizes)} different batch sizes")
    print(f"✅ Total requests: {len(analyzer.results)}")
    print(f"✅ Results saved and visualized")
    print(f"\n📊 Check the generated graphs to see performance scaling!")


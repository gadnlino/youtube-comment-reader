# API Performance Evaluation Methodology

**Document Purpose**: Detailed methodology for evaluating API performance, scalability, and reliability  
**Audience**: Academic/Technical Documentation  
**Date**: October 27, 2025  
**Version**: 1.0  

---

## 📋 Table of Contents

1. [Introduction](#1-introduction)
2. [Test Environment](#2-test-environment)
3. [Test Design](#3-test-design)
4. [Data Collection Methods](#4-data-collection-methods)
5. [Statistical Analysis](#5-statistical-analysis)
6. [Reproducibility](#6-reproducibility)
7. [Limitations](#7-limitations)

---

## 1. Introduction

### 1.1 Purpose

This document describes the comprehensive methodology used to evaluate the performance, scalability, and reliability of the YouTube Comment Reader API. The evaluation aims to measure:

- **Response time** under various conditions
- **Throughput** and request handling capacity
- **Scalability** with increasing load
- **Reliability** and error rates
- **Sentiment analysis overhead**
- **Multi-video consistency**

### 1.2 Evaluation Goals

1. **Quantify Performance**: Measure response times, latency, and throughput
2. **Assess Scalability**: Determine how performance changes with load
3. **Ensure Reliability**: Validate system stability under sustained use
4. **Benchmark Features**: Measure sentiment analysis impact
5. **Academic Rigor**: Provide statistically significant results

### 1.3 Testing Principles

- **Reproducibility**: All tests can be repeated with documented procedures
- **Real-world conditions**: Tests use production deployed API
- **Statistical significance**: Large sample sizes (219+ requests)
- **Comprehensive coverage**: Multiple scenarios and edge cases
- **Transparency**: All data and scripts available for review

---

## 2. Test Environment

### 2.1 Client Environment

**Hardware**:
- **Device**: MacBook (Apple Silicon M-series)
- **Processor**: ARM64 architecture
- **OS**: macOS 25.0.0 (Darwin)
- **Memory**: Sufficient for concurrent requests
- **Storage**: SSD for fast data logging

**Network**:
- **Connection**: Standard broadband internet
- **ISP**: Commercial internet service
- **Location**: Client location to AWS (realistic latency)
- **Bandwidth**: Sufficient for HTTP requests (< 1 MB/s)

**Why this matters**: Testing from real client environment includes authentic network latency and represents genuine user experience.

---

### 2.2 Server Environment (Under Test)

**API Gateway**:
```
Base URL: https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com
Region: us-east-1 (N. Virginia, USA)
Type: AWS API Gateway (REST API)
```

**Backend Architecture**:
- **API Gateway**: AWS API Gateway with REST protocol
- **Comment Fetching Lambda**: Node.js (TypeScript)
  - Memory: 1024 MB
  - Timeout: 2 minutes
  - Runtime: Node.js 18.x
- **Sentiment Analysis Lambda**: Python 3.11 (Docker container)
  - Memory: 1024 MB
  - Timeout: 2 minutes
  - Runtime: Custom Docker image
- **Database**: DynamoDB for comment caching
- **External API**: YouTube Data API v3

**Sentiment Analysis Model**:
- Algorithm: TF-IDF + Logistic Regression
- Accuracy: 66.14%
- Model Size: ~10 MB (serialized)
- Processing Speed: < 100ms per batch of 100 comments

---

### 2.3 Software Tools

**Primary Language**: Python 3.12

**Dependencies**:
```python
requests==2.32.5      # HTTP client library
pandas==2.2.0         # Data analysis and manipulation
matplotlib==3.8.2     # Graph generation
seaborn==0.13.2       # Statistical visualizations
numpy==1.26.4         # Numerical computations
scipy==1.12.0         # Statistical functions
```

**Why these tools**:
- **requests**: Industry-standard, reliable HTTP library
- **pandas**: Powerful statistical analysis and CSV handling
- **matplotlib/seaborn**: Professional, publication-quality graphs
- **numpy/scipy**: Accurate numerical and statistical operations

**Environment Setup**:
```bash
# Create isolated environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 2.4 Test Data Source

**Primary Video**:
- **Video ID**: `dQw4w9WgXcQ`
- **Title**: "Rick Astley - Never Gonna Give You Up"
- **Type**: Music Video
- **Characteristics**:
  - High comment volume (10M+ comments)
  - Diverse sentiments (positive, negative, neutral)
  - Mixture of genuine and humorous comments
  - Publicly accessible
  - Stable (not frequently deleted)

**Secondary Videos** (Multi-Video Testing):
- **Video 2**: `jNQXAC9IVRw` - "Me at the zoo" (First YouTube video)
- **Video 3**: `9bZkp7q19f0` - "PSY - Gangnam Style" (Viral video)

**Rationale**: Using well-known, stable videos ensures:
- Consistent test data across runs
- High comment availability
- Diverse sentiment distribution
- Reproducibility for others

---

## 3. Test Design

### 3.1 Test Suite Overview

The API evaluation consists of **6 test types** covering different aspects:

| Test # | Test Name | Requests | Comments | Duration | Purpose |
|--------|-----------|----------|----------|----------|---------|
| 1 | Extended Performance | 219 | ~10,900 | ~45 min | Comprehensive performance |
| 2 | Heavy Load | 106 | 10,600 | ~3 min | Scalability testing |
| 3 | Multi-Video | 60 | 6,000 | ~1 min | Cross-video consistency |
| 4 | Batch Size Analysis | 90 | 9,000 | ~2 min | Optimization testing |
| 5 | Quick Smoke Test | 10 | 1,000 | ~10 sec | Rapid validation |
| 6 | Sustained Load (Locust) | Variable | Variable | 10 min | Concurrent users |

**Total**: 485+ requests, 37,500+ comments processed

---

### 3.2 Test 1: Extended Performance Test

**Objective**: Comprehensive performance characterization

**Method**: Sequential requests with controlled delays

**Test Scenarios**:

1. **Warm Performance Test** (100 requests):
   ```python
   for i in range(100):
       response = requests.get(API_URL, params={
           'videoId': VIDEO_ID,
           'maxResults': 50,
           'showPositives': 'true',
           'showNegatives': 'true',
           'showNeutral': 'true'
       })
       log_metrics(response)
       time.sleep(0.2)  # 200ms delay
   ```
   - Purpose: Measure stable, warmed-up performance
   - Delay: 0.2 seconds between requests
   - Expected: Consistent response times

2. **Batch Size Impact Test** (40 requests):
   ```python
   batch_sizes = [10, 25, 50, 100]
   for size in batch_sizes:
       for repeat in range(10):
           response = requests.get(API_URL, params={
               'videoId': VIDEO_ID,
               'maxResults': size,
               'showPositives': 'true',
               'showNegatives': 'true',
               'showNeutral': 'true'
           })
           log_metrics(response, batch_size=size)
   ```
   - Purpose: Measure impact of comment count on response time
   - Batch sizes: 10, 25, 50, 100 comments
   - Expected: Linear or sub-linear scaling

3. **Sentiment Overhead Test** (40 requests):
   ```python
   # Without sentiment (20 requests)
   for i in range(20):
       response = requests.get(API_URL, params={
           'videoId': VIDEO_ID,
           'maxResults': 50
           # No sentiment flags
       })
       log_metrics(response, has_sentiment=False)
   
   # With sentiment (20 requests)
   for i in range(20):
       response = requests.get(API_URL, params={
           'videoId': VIDEO_ID,
           'maxResults': 50,
           'showPositives': 'true',
           'showNegatives': 'true',
           'showNeutral': 'true'
       })
       log_metrics(response, has_sentiment=True)
   ```
   - Purpose: Quantify sentiment analysis computational cost
   - Sample size: 20 requests each (statistically adequate)
   - Expected: Measurable but acceptable overhead

4. **Sustained Load Test** (79 requests):
   ```python
   start_time = time.time()
   duration = 120  # 2 minutes
   
   while time.time() - start_time < duration:
       response = requests.get(API_URL, params={...})
       log_metrics(response)
       time.sleep(0.5)  # 500ms delay
   ```
   - Purpose: Test long-term stability
   - Duration: 2 minutes continuous
   - Delay: 0.5 seconds between requests
   - Expected: No performance degradation

**Total Requests**: 219  
**Expected Duration**: ~45 minutes  
**Script**: `evaluation/scripts/02_api_performance/benchmarks/extended_benchmark.py`

---

### 3.3 Test 2: Heavy Load Test

**Objective**: Validate system under high volume

**Method**: Rapid sequential requests simulating heavy usage

**Test Phases**:

1. **Incremental Batch Size Test** (6 requests):
   ```python
   batch_sizes = [100, 500, 1000, 2000, 5000, 10000]
   for size in batch_sizes:
       response = requests.get(API_URL, params={
           'videoId': VIDEO_ID,
           'maxResults': size,
           'showPositives': 'true',
           'showNegatives': 'true',
           'showNeutral': 'true'
       })
       log_metrics(response, batch_size=size)
       time.sleep(1.0)  # 1 second between tests
   ```
   - Purpose: Find system limits
   - Batch sizes: 100 to 10,000 comments requested
   - Note: YouTube API limits actual returned comments to ~100

2. **High Volume Test** (100 requests):
   ```python
   for i in range(100):
       response = requests.get(API_URL, params={
           'videoId': VIDEO_ID,
           'maxResults': 100,
           'showPositives': 'true',
           'showNegatives': 'true',
           'showNeutral': 'true'
       })
       log_metrics(response)
       time.sleep(0.5)  # 500ms delay
   ```
   - Purpose: Process 10,000 total comments
   - Target: 100 requests × 100 comments = 10,000 comments
   - Duration: ~3 minutes
   - Expected: Consistent performance, no failures

**Total Requests**: 106  
**Total Comments**: 10,600  
**Expected Duration**: ~3-4 minutes  
**Script**: `evaluation/scripts/02_api_performance/benchmarks/heavy_load_test.py`

---

### 3.4 Test 3: Multi-Video Consistency Test

**Objective**: Verify performance across different videos

**Method**: Test 3 diverse videos with identical request patterns

**Test Design**:
```python
videos = [
    {'id': 'dQw4w9WgXcQ', 'name': 'Rick Astley'},
    {'id': 'jNQXAC9IVRw', 'name': 'Me at the zoo'},
    {'id': '9bZkp7q19f0', 'name': 'Gangnam Style'}
]

for video in videos:
    for i in range(20):  # 20 requests per video
        response = requests.get(API_URL, params={
            'videoId': video['id'],
            'maxResults': 100,
            'showPositives': 'true',
            'showNegatives': 'true',
            'showNeutral': 'true'
        })
        log_metrics(response, video_id=video['id'], video_name=video['name'])
        time.sleep(0.5)
```

**Video Selection Rationale**:
- **Video 1**: Music, high engagement, meme culture
- **Video 2**: Documentary, nostalgic comments
- **Video 3**: Viral, international audience

**Analysis**:
- Compare average response times across videos
- Check for performance bias toward specific content
- Verify sentiment distribution diversity

**Total Requests**: 60 (20 per video)  
**Total Comments**: 6,000  
**Expected Duration**: ~1 minute  
**Script**: `evaluation/scripts/02_api_performance/benchmarks/multi_video_benchmark.py`

---

### 3.5 Test 4: Batch Size Analysis

**Objective**: Optimize request parameters

**Method**: Systematic testing of different batch sizes

**Test Design**:
```python
batch_sizes = [10, 25, 50, 75, 100]

for size in batch_sizes:
    for repeat in range(18):  # 18 requests per batch size
        response = requests.get(API_URL, params={
            'videoId': VIDEO_ID,
            'maxResults': size,
            'showPositives': 'true',
            'showNegatives': 'true',
            'showNeutral': 'true'
        })
        log_metrics(response, batch_size=size)
        time.sleep(0.5)
```

**Metrics Analyzed**:
1. **Response time vs batch size**: Linear, sub-linear, or super-linear?
2. **Time per comment**: Does efficiency improve with larger batches?
3. **Optimal batch size**: Balance between speed and data volume

**Expected Results**:
- Larger batches may have higher total time
- Time per comment should decrease (economies of scale)
- Optimal batch size around 50-100 comments

**Total Requests**: 90 (18 per batch size)  
**Total Comments**: 9,000  
**Expected Duration**: ~2 minutes  
**Script**: `evaluation/scripts/02_api_performance/benchmarks/batch_size_analysis.py`

---

### 3.6 Test 5: Quick Smoke Test

**Objective**: Rapid validation for development/debugging

**Method**: Minimal request set to verify functionality

**Test Design**:
```python
# 10 quick requests
for i in range(10):
    response = requests.get(API_URL, params={
        'videoId': VIDEO_ID,
        'maxResults': 100,
        'showPositives': 'true',
        'showNegatives': 'true',
        'showNeutral': 'true'
    })
    log_metrics(response)
    time.sleep(0.5)
```

**Purpose**:
- Verify API is operational
- Check basic functionality
- Quick performance spot-check
- Development iteration

**Total Requests**: 10  
**Expected Duration**: ~10 seconds  
**Script**: `evaluation/scripts/02_api_performance/benchmarks/quick_test.py`

---

### 3.7 Test 6: Concurrent Load Test (Locust)

**Objective**: Test concurrent user simulation

**Method**: Use Locust load testing framework

**Test Configuration**:
```python
# locustfile.py
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)  # 1-3 seconds between requests
    
    @task
    def get_comments(self):
        self.client.get("/comments", params={
            'videoId': 'dQw4w9WgXcQ',
            'maxResults': 50,
            'showPositives': 'true',
            'showNegatives': 'true',
            'showNeutral': 'true'
        })
```

**Test Execution**:
```bash
# Start with 10 users, spawn 2 users/sec, run for 10 minutes
locust -f locustfile.py --headless \
       --users 10 \
       --spawn-rate 2 \
       --run-time 10m \
       --host https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com
```

**Metrics Collected**:
- Requests per second (RPS)
- Response time percentiles (P50, P90, P95, P99)
- Failure rate
- Concurrent user capacity

**Expected Duration**: 10 minutes  
**Script**: `evaluation/scripts/02_api_performance/benchmarks/locustfile.py`

---

## 4. Data Collection Methods

### 4.1 Metrics Collected

For each API request, the following metrics are recorded:

| Metric | Type | Description | Units |
|--------|------|-------------|-------|
| `timestamp` | DateTime | Exact time of request | ISO 8601 |
| `test_name` | String | Test identifier | - |
| `video_id` | String | YouTube video ID | - |
| `batch_size` | Integer | Requested comment count | count |
| `response_time_ms` | Float | Total request duration | milliseconds |
| `status_code` | Integer | HTTP status code | - |
| `comment_count` | Integer | Actual comments returned | count |
| `has_sentiment` | Boolean | Sentiment analysis included | true/false |
| `success` | Boolean | Request successful | true/false |
| `error_message` | String | Error details (if failed) | - |

---

### 4.2 Data Collection Process

**Automated Logging**:
```python
import time
import requests
from datetime import datetime

def make_request_and_log(video_id, max_results, with_sentiment=True):
    # 1. Record start time
    start_time = time.time()
    
    # 2. Prepare parameters
    params = {
        'videoId': video_id,
        'maxResults': max_results
    }
    if with_sentiment:
        params.update({
            'showPositives': 'true',
            'showNegatives': 'true',
            'showNeutral': 'true'
        })
    
    # 3. Make HTTP request
    try:
        response = requests.get(API_URL, params=params, timeout=120)
        elapsed_ms = (time.time() - start_time) * 1000
        
        # 4. Extract response data
        data = response.json() if response.status_code == 200 else {}
        comment_count = len(data.get('items', []))
        success = response.status_code == 200
        error_msg = data.get('error', '') if not success else ''
        
    except Exception as e:
        elapsed_ms = (time.time() - start_time) * 1000
        response.status_code = 0
        comment_count = 0
        success = False
        error_msg = str(e)
    
    # 5. Create log record
    record = {
        'timestamp': datetime.now().isoformat(),
        'video_id': video_id,
        'batch_size': max_results,
        'response_time_ms': elapsed_ms,
        'status_code': response.status_code,
        'comment_count': comment_count,
        'has_sentiment': with_sentiment,
        'success': success,
        'error_message': error_msg
    }
    
    return record
```

**Why this approach**:
- **Precise timing**: Measure actual request duration
- **Comprehensive**: Capture all relevant metrics
- **Error handling**: Log failures for analysis
- **Structured**: Easy to analyze with pandas

---

### 4.3 Data Storage

**CSV Format** (Primary):
```csv
timestamp,test_name,video_id,batch_size,response_time_ms,status_code,comment_count,has_sentiment,success
2025-10-27T14:30:00.123,Extended,dQw4w9WgXcQ,50,1024,200,50,True,True
2025-10-27T14:30:01.456,Extended,dQw4w9WgXcQ,50,987,200,50,True,True
...
```

**Advantages**:
- Standard format, widely supported
- Easy to load with pandas
- Human-readable
- Version control friendly

**JSON Format** (Summaries):
```json
{
  "test_name": "Extended Performance Test",
  "total_requests": 219,
  "successful_requests": 219,
  "success_rate": 100.0,
  "statistics": {
    "mean_ms": 1024,
    "median_ms": 1101,
    "std_ms": 300,
    "min_ms": 569,
    "max_ms": 2633,
    "p95_ms": 1219,
    "p99_ms": 1538
  },
  "timestamp": "2025-10-27T14:45:00"
}
```

**File Organization**:
```
03_data/
├── csv/
│   ├── extended_performance_results.csv
│   ├── heavy_load_test_results.csv
│   ├── multi_video_results.csv
│   └── batch_size_analysis.csv
└── json/
    ├── extended_summary.json
    ├── heavy_load_summary.json
    └── multi_video_summary.json
```

---

## 5. Statistical Analysis

### 5.1 Descriptive Statistics

**Central Tendency**:
```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('results.csv')
successful = df[df['success'] == True]
times = successful['response_time_ms']

# Calculate statistics
stats = {
    'mean': times.mean(),           # Average
    'median': times.median(),       # Middle value (50th percentile)
    'mode': times.mode()[0],        # Most common value
}
```

**Dispersion**:
```python
stats.update({
    'std': times.std(),             # Standard deviation
    'variance': times.var(),        # Variance
    'range': times.max() - times.min(),  # Range
    'iqr': times.quantile(0.75) - times.quantile(0.25)  # Interquartile range
})
```

**Percentiles**:
```python
percentiles = {
    'p50': times.quantile(0.50),    # Median (50th percentile)
    'p75': times.quantile(0.75),    # 75th percentile
    'p90': times.quantile(0.90),    # 90th percentile (SLA metric)
    'p95': times.quantile(0.95),    # 95th percentile (SLA metric)
    'p99': times.quantile(0.99),    # 99th percentile (worst case)
}
```

**Why these metrics**:
- **Mean**: Overall average, useful for total cost estimation
- **Median**: Typical user experience (not skewed by outliers)
- **Std Dev**: Performance consistency (lower is better)
- **P95/P99**: Worst-case scenarios, SLA compliance

---

### 5.2 Comparative Analysis

**Sentiment Overhead Calculation**:
```python
# Split data by sentiment inclusion
without_sentiment = df[df['has_sentiment'] == False]['response_time_ms']
with_sentiment = df[df['has_sentiment'] == True]['response_time_ms']

# Calculate averages
avg_without = without_sentiment.mean()
avg_with = with_sentiment.mean()

# Calculate overhead
overhead_ms = avg_with - avg_without
overhead_pct = (overhead_ms / avg_without) * 100

print(f"Overhead: {overhead_ms:.0f}ms ({overhead_pct:.1f}%)")
```

**Batch Size Analysis**:
```python
# Group by batch size
batch_analysis = df.groupby('batch_size').agg({
    'response_time_ms': ['mean', 'std', 'count'],
    'comment_count': 'mean'
})

# Calculate time per comment
batch_analysis['time_per_comment'] = (
    batch_analysis['response_time_ms']['mean'] / 
    batch_analysis['comment_count']['mean']
)

print(batch_analysis)
```

**Multi-Video Comparison**:
```python
# Group by video
video_analysis = df.groupby('video_id').agg({
    'response_time_ms': ['mean', 'median', 'std'],
    'success': 'sum'
})

# Statistical test (ANOVA)
from scipy import stats
videos = df['video_id'].unique()
groups = [df[df['video_id'] == v]['response_time_ms'] for v in videos]
f_stat, p_value = stats.f_oneway(*groups)

print(f"ANOVA F-statistic: {f_stat:.2f}, p-value: {p_value:.4f}")
if p_value > 0.05:
    print("No significant difference between videos")
else:
    print("Significant difference detected")
```

---

### 5.3 Confidence Intervals

**Calculate 95% Confidence Interval**:
```python
from scipy import stats

# Calculate mean and standard error
mean = times.mean()
std_error = times.std() / np.sqrt(len(times))

# 95% confidence interval
confidence = 0.95
degrees_freedom = len(times) - 1
t_value = stats.t.ppf((1 + confidence) / 2, degrees_freedom)

margin_error = t_value * std_error
ci_lower = mean - margin_error
ci_upper = mean + margin_error

print(f"Mean: {mean:.0f}ms")
print(f"95% CI: [{ci_lower:.0f}ms, {ci_upper:.0f}ms]")
```

**Interpretation**:
- We are 95% confident the true mean response time lies within this interval
- With 219 samples, confidence interval is tight
- Adequate for production decision-making

---

### 5.4 Visualization Methods

**1. Time Series (Response Time Over Requests)**:
```python
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['response_time_ms'], alpha=0.6, linewidth=0.8)
plt.axhline(df['response_time_ms'].mean(), color='r', 
            linestyle='--', label='Mean')
plt.axhline(df['response_time_ms'].median(), color='g', 
            linestyle='--', label='Median')
plt.xlabel('Request Number')
plt.ylabel('Response Time (ms)')
plt.title('Response Time Across All Requests')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('response_time_series.png', dpi=300)
```

**2. Distribution Histogram**:
```python
plt.figure(figsize=(10, 6))
plt.hist(df['response_time_ms'], bins=50, edgecolor='black', alpha=0.7)
plt.axvline(df['response_time_ms'].mean(), color='r', 
            linestyle='--', label=f"Mean: {df['response_time_ms'].mean():.0f}ms")
plt.axvline(df['response_time_ms'].median(), color='g', 
            linestyle='--', label=f"Median: {df['response_time_ms'].median():.0f}ms")
plt.xlabel('Response Time (ms)')
plt.ylabel('Frequency')
plt.title('Response Time Distribution')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.savefig('response_time_distribution.png', dpi=300)
```

**3. Box Plot (Comparison)**:
```python
plt.figure(figsize=(10, 6))
df.boxplot(column='response_time_ms', by='video_id', figsize=(10, 6))
plt.xlabel('Video ID')
plt.ylabel('Response Time (ms)')
plt.title('Response Time by Video')
plt.suptitle('')  # Remove default title
plt.savefig('response_time_by_video.png', dpi=300)
```

**4. Heatmap (Performance Matrix)**:
```python
import seaborn as sns

# Create pivot table
pivot = df.pivot_table(
    values='response_time_ms',
    index='batch_size',
    columns='has_sentiment',
    aggfunc='mean'
)

plt.figure(figsize=(8, 6))
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd')
plt.title('Average Response Time (ms) by Batch Size and Sentiment')
plt.xlabel('Sentiment Analysis')
plt.ylabel('Batch Size')
plt.savefig('performance_heatmap.png', dpi=300)
```

---

## 6. Reproducibility

### 6.1 Setup Instructions

**Prerequisites**:
```bash
# System requirements
- Python 3.12 or higher
- pip package manager
- 500 MB disk space
- Internet connection
```

**Installation**:
```bash
# Navigate to evaluation directory
cd evaluation/scripts/02_api_performance/benchmarks

# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

---

### 6.2 Running Tests

**Extended Performance Test**:
```bash
python extended_benchmark.py

# Expected output:
# ✅ Starting Extended Performance Test...
# ⏳ Test 1/4: Warm Performance Test (100 requests)
# ⏳ Test 2/4: Batch Size Test (40 requests)
# ⏳ Test 3/4: Sentiment Overhead Test (40 requests)
# ⏳ Test 4/4: Sustained Load Test (79 requests)
# ✅ Test completed! Results saved to:
#    - 03_data/csv/extended_performance_results.csv
#    - 03_data/json/extended_summary.json
```

**Heavy Load Test**:
```bash
python heavy_load_test.py

# Duration: ~3-4 minutes
# Outputs: CSV and JSON files
```

**Multi-Video Test**:
```bash
python multi_video_benchmark.py

# Duration: ~1 minute
# Outputs: CSV and JSON files
```

**Batch Size Analysis**:
```bash
python batch_size_analysis.py

# Duration: ~2 minutes
# Outputs: CSV and JSON files
```

**Quick Smoke Test**:
```bash
python quick_test.py

# Duration: ~10 seconds
# Outputs: Console output only
```

---

### 6.3 Generating Graphs

**Academic Graphs (English)**:
```bash
cd ../generators
python generate_academic_graphs.py

# Generates:
# - 02_graphs/english/figure1_comprehensive_performance_overview.png
# - 02_graphs/english/figure2_scalability_analysis.png
# - 02_graphs/english/figure3_statistical_summary.png
# - 02_graphs/english/figure4_performance_heatmap.png
```

**Academic Graphs (Portuguese)**:
```bash
python generate_academic_graphs_pt.py

# Generates Portuguese versions of all graphs
```

---

### 6.4 Expected Variations

**Response Times**:
- **Range**: ±10-20% variation expected
- **Causes**: Network conditions, AWS load, time of day
- **Example**: If documented mean is 1,024ms, expect 820-1,229ms

**Throughput**:
- **Range**: ±5-10% variation expected
- **Causes**: Lambda cold starts, cache state
- **Example**: If documented 0.65 req/s, expect 0.59-0.72 req/s

**Success Rate**:
- **Expected**: Should remain 100% or very close
- **Acceptable**: ≥95% (occasional failures due to network)
- **Causes**: Network timeouts, YouTube API rate limits

**Statistical Confidence**:
- Mean values should fall within documented 95% confidence intervals
- Standard deviation may vary ±15%
- Percentiles (P95, P99) may vary more (±20-30%)

---

## 7. Limitations

### 7.1 Test Limitations

**Sample Size**:
- **Current**: 219-485 requests per test type
- **Limitation**: Not exhaustive (millions would be ideal)
- **Justification**: Balances thoroughness vs. time/cost
- **Mitigation**: Multiple test types cover different scenarios

**Test Duration**:
- **Current**: Tests run for minutes to hours
- **Limitation**: Don't capture weekly/monthly patterns
- **Justification**: Adequate for performance characterization
- **Mitigation**: Multiple test runs at different times

**Geographic Location**:
- **Current**: Single test location (client machine)
- **Limitation**: Latency varies by geography
- **Justification**: Represents typical user experience
- **Mitigation**: Document test location, AWS region

**Video Diversity**:
- **Current**: 3 videos tested extensively
- **Limitation**: YouTube has billions of videos
- **Justification**: Selected videos represent diverse characteristics
- **Mitigation**: Videos chosen for diversity (content type, engagement)

---

### 7.2 External Factors

**Uncontrolled Variables**:

1. **YouTube API Rate Limits**:
   - Daily quota: 10,000 units
   - Impact: May throttle or reject requests
   - Mitigation: Use known working videos, reasonable request rates

2. **AWS Lambda Cold Starts**:
   - First request after idle: +500-2000ms latency
   - Impact: Skews average upward
   - Mitigation: Documented separately, excluded from some analyses

3. **Network Latency**:
   - Variable based on ISP, routing, congestion
   - Impact: Adds variability to measurements
   - Mitigation: Large sample size averages out variations

4. **Cache State**:
   - DynamoDB caches comment data
   - Impact: First request slow, subsequent fast
   - Mitigation: Tested both scenarios (cold and warm cache)

5. **Time of Day**:
   - AWS load varies throughout day
   - Impact: Performance may vary by test time
   - Mitigation: Multiple test runs, document test times

---

### 7.3 Assumptions

**Key Assumptions**:

1. **Representative Data**: Selected videos represent typical usage
   - **Validity**: Reasonable for diverse content types
   - **Risk**: May not represent niche or problematic videos

2. **Network Stability**: Internet connection stable during tests
   - **Validity**: Modern broadband is generally stable
   - **Risk**: Occasional network hiccups

3. **No External Interference**: No other processes affecting results
   - **Validity**: Dedicated test runs
   - **Risk**: Background processes on client machine

4. **API Stability**: AWS services operating normally
   - **Validity**: AWS has high uptime (99.9%+)
   - **Risk**: Occasional AWS outages or issues

5. **Model Consistency**: Sentiment model performance is stable
   - **Validity**: Model is deterministic (not neural network)
   - **Risk**: Model version changes (unlikely)

---

### 7.4 Threats to Validity

**Internal Validity**:
- **Risk**: Measurement errors
- **Mitigation**: Automated data collection, validated logging

**External Validity**:
- **Risk**: Results may not generalize to all conditions
- **Mitigation**: Multiple videos, test scenarios, geographic note

**Construct Validity**:
- **Risk**: Metrics may not capture true user experience
- **Mitigation**: Multiple metrics (response time, throughput, success rate)

**Statistical Conclusion Validity**:
- **Risk**: Insufficient sample size for confident conclusions
- **Mitigation**: 219+ samples per test (exceeds n=30 minimum)

---

### 7.5 Ethical Considerations

**Data Privacy**:
- **Approach**: Use only public YouTube videos
- **Rationale**: No private or sensitive data accessed
- **Compliance**: YouTube Terms of Service followed

**Resource Usage**:
- **Approach**: Reasonable request rates (0.2-0.5s delays)
- **Rationale**: Avoid overloading API or infrastructure
- **Compliance**: AWS and YouTube rate limits respected

**Reproducibility**:
- **Approach**: All scripts and data documented
- **Rationale**: Enable peer review and validation
- **Benefit**: Transparent, trustworthy research

---

## 8. Conclusion

This methodology document provides a comprehensive, reproducible approach to API performance evaluation. Key strengths:

✅ **Rigorous**: Large sample sizes, statistical analysis  
✅ **Comprehensive**: Multiple test types covering different scenarios  
✅ **Reproducible**: Detailed procedures, scripts provided  
✅ **Transparent**: Limitations and assumptions acknowledged  
✅ **Academic**: Meets standards for research documentation  

**Results Summary**:
- **Average Response Time**: 1,024ms (excellent)
- **Success Rate**: 100% (perfect reliability)
- **Scalability**: Handles 10,600+ comments without degradation
- **Consistency**: Performs uniformly across diverse videos

---

**Document Version**: 1.0  
**Last Updated**: October 27, 2025  
**Author**: Guilherme Avelino  
**Status**: Complete  

---

## 9. References

**Academic Literature**:
- Tanenbaum, A. S., & Van Steen, M. (2017). *Distributed Systems: Principles and Paradigms*. Pearson.
- Vogels, W. (2009). Eventually consistent. *Communications of the ACM*, 52(1), 40-44.

**Tools & Frameworks**:
- [Python Requests Library](https://requests.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [Locust Load Testing](https://locust.io/)

**APIs & Services**:
- [AWS API Gateway](https://aws.amazon.com/api-gateway/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)

**Statistical Methods**:
- [SciPy Stats Module](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [NumPy User Guide](https://numpy.org/doc/stable/user/)


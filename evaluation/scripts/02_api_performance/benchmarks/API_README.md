# API Load Testing & Performance Evaluation

This directory contains comprehensive load testing and performance benchmarking tools for the YouTube Comment Reader API.

## 📋 What We Test

### 1. **Complete End-to-End Flow**
- Search videos → Fetch comments → Sentiment analysis → Filter by sentiment
- Tests the real integration that the mobile app uses

### 2. **Performance Metrics**
- ⏱️ Response times (average, min, max, p95, p99)
- 🚀 Throughput (requests per second / TPS)
- ❄️ Cold start vs warm Lambda performance
- 📦 Different batch sizes (10, 25, 50, 100 comments)
- 🎭 Sentiment analysis overhead

### 3. **Load Testing**
- Concurrent users (simulate 1-100 simultaneous users)
- Sustained load over time
- Error rates under stress
- API behavior under load

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd evaluation/api_load_testing

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r evaluation/requirements.txt
```

### 2. Configure Test Parameters

Edit the configuration in the scripts:

**For `performance_benchmark.py`:**
```python
API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com"
YOUTUBE_API_KEY = "YOUR_KEY_HERE"
VIDEO_ID = "dQw4w9WgXcQ"  # Video with many comments
```

**For `locustfile.py`:**
```python
VIDEO_ID = "dQw4w9WgXcQ"  # Video with many comments
API_KEY = "YOUR_KEY_HERE"
```

---

## 📊 Option 1: Performance Benchmark (Automated)

**Best for**: Detailed metrics, graphs, and reports

Run the automated benchmark:

```bash
python performance_benchmark.py
```

### What it does:
1. ✅ Tests warm Lambda performance (10 consecutive requests)
2. ✅ Tests different batch sizes (10, 25, 50, 100 comments)
3. ✅ Measures sentiment analysis overhead
4. ✅ Measures throughput (30 seconds sustained load)

### Output:
- 📄 `performance_results_TIMESTAMP.csv` - Detailed results
- 📊 `response_time_graph_TIMESTAMP.png` - Response time visualization
- 📊 `batch_size_comparison_TIMESTAMP.png` - Batch size comparison
- 🖥️ Console output with summary statistics

### Example Output:
```
📈 Response Time Statistics:
   Average:  2450ms
   Minimum:  1850ms
   Maximum:  4200ms
   P95:      3800ms
   P99:      4100ms

🎭 Sentiment Analysis:
   Overhead: 1200ms (80.5%)

⚡ Throughput:
   5.23 requests/second

✅ Success Rate:
   100.0% (25/25)
```

---

## 🔥 Option 2: Load Testing with Locust (Interactive)

**Best for**: Simulating real users, stress testing, interactive monitoring

### 1. Start Locust

```bash
locust -f locustfile.py --host=https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com
```

### 2. Open Web Interface

Open your browser to: **http://localhost:8089**

### 3. Configure Test

In the web interface:
- **Number of users**: Start with 10, increase to 50-100
- **Spawn rate**: 5 users per second
- **Host**: Already configured
- Click **Start Swarming**

### 4. Monitor Results

The web interface shows:
- 📈 Requests per second (RPS/TPS)
- ⏱️ Response time charts (real-time)
- ✅ Success/failure rates
- 📊 Response time percentiles (p50, p95, p99)
- 📉 Number of users over time

### 5. Test Scenarios

Locust automatically tests these scenarios with different weights:
- Search videos (weight: 2)
- Fetch comments without sentiment (weight: 3 - most common)
- Fetch comments with all sentiments (weight: 2)
- Fetch only positive comments (weight: 1)
- Fetch only negative comments (weight: 1)

### 6. Export Results

Click **Download Data** to export:
- CSV with detailed statistics
- Response time distribution
- Failures report

---

## 📝 Test Scenarios

### Scenario 1: Baseline Performance
**What**: Fetch comments WITHOUT sentiment analysis  
**Purpose**: Measure YouTube API + caching performance  
**Command**:
```python
params = {
    'videoId': VIDEO_ID,
    'maxResults': 50,
}
```

### Scenario 2: With Sentiment Analysis
**What**: Fetch comments WITH sentiment (all types)  
**Purpose**: Measure complete flow including ML Lambda  
**Command**:
```python
params = {
    'videoId': VIDEO_ID,
    'maxResults': 50,
    'showPositives': 'true',
    'showNegatives': 'true',
    'showNeutral': 'true'
}
```

### Scenario 3: Filtered by Sentiment
**What**: Fetch only positive/negative comments  
**Purpose**: Test sentiment filtering accuracy and performance  
**Command**:
```python
params = {
    'videoId': VIDEO_ID,
    'maxResults': 50,
    'showPositives': 'true'  # or showNegatives
}
```

### Scenario 4: Different Batch Sizes
**What**: Test with 10, 25, 50, 100 comments  
**Purpose**: Find optimal batch size for performance  
**Expected**: Linear or sub-linear scaling

---

## 📊 Understanding the Results

### Response Time
- **< 1000ms**: Excellent (likely cached)
- **1000-3000ms**: Good (YouTube API + sentiment)
- **3000-5000ms**: Acceptable (large batches)
- **> 5000ms**: Investigate (possible cold start or throttling)

### Throughput (TPS)
- **> 10 req/s**: Excellent
- **5-10 req/s**: Good
- **1-5 req/s**: Acceptable for ML workload
- **< 1 req/s**: Investigate bottlenecks

### Sentiment Overhead
- Expected: 50-150% overhead compared to no sentiment
- Depends on: Batch size, Lambda warmth, network

### Success Rate
- Target: > 95%
- Errors might be:
  - YouTube API quota exceeded (403)
  - Lambda timeout (504)
  - Cold start timeout (502)

---

## 🎯 Evaluation Checklist

Use these results for your assignment:

### ✅ Performance Metrics
- [ ] Average response time documented
- [ ] P95 and P99 percentiles measured
- [ ] Throughput (TPS) measured
- [ ] Cold start time measured (optional)
- [ ] Warm performance measured

### ✅ Sentiment Analysis
- [ ] Overhead percentage calculated
- [ ] Impact on response time documented
- [ ] Filtering accuracy verified

### ✅ Scalability
- [ ] Batch size impact analyzed
- [ ] Concurrent user performance tested
- [ ] Success rate under load measured

### ✅ Graphs & Visualizations
- [ ] Response time graphs generated
- [ ] Batch size comparison chart
- [ ] Throughput chart from Locust

---

## 🐛 Troubleshooting

### Error: YouTube API Quota Exceeded (403)
**Solution**: Use a different API key or wait for quota reset

### Error: Lambda Timeout
**Solution**: Increase Lambda timeout in CDK stack or reduce batch size

### Error: High Response Times
**Check**:
1. Is Lambda cold? (First request after 15 min idle)
2. Is caching enabled? (should be faster on repeat)
3. Is YouTube API slow? (test without sentiment)

### Locust not starting
**Fix**:
```bash
pip install -r evaluation/requirements.txt
```

---

## 📈 Expected Results

Based on typical performance:

| Metric | Without Sentiment | With Sentiment |
|--------|------------------|----------------|
| Avg Response Time | 500-1500ms | 1500-3000ms |
| P95 Response Time | 1000-2000ms | 2500-4000ms |
| Throughput | 10-20 req/s | 3-8 req/s |
| Success Rate | 99%+ | 95%+ |

---

## 📁 Output Files

After running tests, you'll have:

```
evaluation/api_load_testing/
├── performance_results_20250125_143022.csv
├── response_time_graph_20250125_143022.png
├── batch_size_comparison_20250125_143022.png
├── locust_stats_20250125_143530.csv          # From Locust
└── locust_failures_20250125_143530.csv       # From Locust
```

---

## 💡 Tips for Assignment

1. **Run multiple times**: Results can vary, average 3-5 runs
2. **Document environment**: Note AWS region, Lambda memory, etc.
3. **Compare scenarios**: With/without sentiment, different batch sizes
4. **Include graphs**: Visual results are more impactful
5. **Analyze trade-offs**: Accuracy vs speed, cost vs performance

---

## 🔗 Related Documentation

- [Sentiment Analysis Model Evaluation](../../packages/containers/sentiment_analysis/evaluation/model_evaluation/MODEL_COMPARISON_SUMMARY.md)
- [API Documentation](../../SENTIMENT_ANALYSIS_API_DOCUMENTATION.md)
- [Deployment Guide](../../DEPLOY.md)

---

## ✨ Questions?

Common metrics for your report:
- **Average Response Time**: Most important user-facing metric
- **P95/P99**: Shows worst-case scenarios
- **Throughput**: System capacity
- **Sentiment Overhead**: Cost of ML feature
- **Success Rate**: Reliability

Good luck with your final assignment! 🚀



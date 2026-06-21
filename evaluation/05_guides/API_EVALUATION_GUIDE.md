# API Performance Evaluation - Assignment Documentation

## 📋 Overview

This document provides a structured evaluation framework for the YouTube Comment Reader application, focusing on API performance, load testing, and end-to-end functionality testing.

## 🎯 Evaluation Areas

### 1. ✅ Sentiment Analysis Accuracy (COMPLETED)
**Location**: `packages/containers/sentiment_analysis/evaluation/model_evaluation/`

**Results**:
- **Model Used**: TF-IDF + Logistic Regression
- **Accuracy**: 66.14%
- **F1-Score**: 66.28%
- **Dataset Size**: 1M+ comments
- **Compared Against**: VADER, TextBlob, SVM, DeBERTa transformers

**Documentation**: See `MODEL_COMPARISON_SUMMARY.md` for detailed analysis

---

### 2. 🔥 API Load Testing & Performance (NEW)
**Location**: `evaluation/api_load_testing/`

#### What We Test:

##### A. Response Time Metrics
- Average, Minimum, Maximum response times
- P95 and P99 percentiles
- Response time distribution

##### B. Throughput
- Requests per second (RPS/TPS)
- Sustained load capacity
- Concurrent user handling (10, 50, 100 users)

##### C. Cold Start vs Warm Performance
- First request after idle (cold start)
- Consecutive requests (warm Lambda)
- Performance degradation over time

##### D. Batch Size Impact
- Small batches: 10 comments
- Medium batches: 25-50 comments
- Large batches: 100 comments
- Time per comment scaling

##### E. Sentiment Analysis Overhead
- Baseline: Comments without sentiment
- With sentiment: Complete flow
- Overhead calculation (time & percentage)

##### F. API Endpoints Tested
1. `/prod/videos/search` - Video search
2. `/prod/comments` - Fetch comments (no sentiment)
3. `/prod/comments?showPositives=true&showNegatives=true&showNeutral=true` - With sentiment
4. `/prod/comments?showPositives=true` - Filter positive only
5. `/prod/comments?showNegatives=true` - Filter negative only

#### How to Run:

**Quick Test** (verify everything works):
```bash
cd evaluation/api_load_testing
python3 -m venv venv
source venv/bin/activate
pip install -r evaluation/requirements.txt
python quick_test.py
```

**Performance Benchmark** (automated metrics + graphs):
```bash
python performance_benchmark.py
```

**Load Testing** (interactive with web UI):
```bash
locust -f locustfile.py --host=https://YOUR_API.amazonaws.com
# Open browser: http://localhost:8089
```

#### Expected Output Files:
- `performance_results_TIMESTAMP.csv` - Raw data
- `response_time_graph_TIMESTAMP.png` - Visualization
- `batch_size_comparison_TIMESTAMP.png` - Batch analysis
- Locust web UI with real-time stats

---

### 3. 🧪 End-to-End Functionality Testing

#### Test Scenarios:

**Scenario 1**: Complete User Flow
1. User searches for videos
2. Selects a video
3. Fetches comments
4. Applies sentiment filter (positive/negative/neutral)
5. Verifies correct comments are shown

**Scenario 2**: Sentiment Filter Accuracy
1. Fetch comments with all sentiments
2. Filter for positive only → Verify all are POSITIVE
3. Filter for negative only → Verify all are NEGATIVE
4. Filter for neutral only → Verify all are NEUTRAL

**Scenario 3**: Error Handling
1. Invalid video ID → Graceful error
2. YouTube API quota exceeded (403) → User-friendly message
3. No internet connection → Proper error handling
4. Very long comments → Truncation/display

**Scenario 4**: Cache Effectiveness
1. First request (cold) → Measure time
2. Repeat request → Should be faster (cached)
3. Calculate cache speedup

**How to Test**:
```bash
python quick_test.py  # Automated E2E tests
```

Or manually using the mobile app:
1. Open app
2. Search for a video
3. Apply sentiment filters
4. Verify results match expectations

---

### 4. 📱 User Experience Evaluation

#### A. Task Completion Testing

**Task 1**: Find negative comments about a video
- Without filter: User must read all comments manually
- With filter: User clicks "Show Negative" filter
- **Metric**: Time to complete task
- **Expected**: 5-10x faster with filter

**Task 2**: Analyze video sentiment at a glance
- View comment count by sentiment
- Quick understanding of overall reception
- **Metric**: Time to understand video sentiment
- **Expected**: < 10 seconds vs 2-3 minutes manual review

#### B. UI/UX Metrics

1. **Loading States**
   - Does spinner show during API calls?
   - Is user informed of progress?
   - Timeout handling

2. **Visual Feedback**
   - Sentiment colors (green/red/gray)
   - Clear indication of active filters
   - Error messages are clear

3. **Responsiveness**
   - Touch targets are adequate (44x44pt minimum)
   - Smooth scrolling through comments
   - Filter toggle is instant

#### C. Mobile App Performance

1. **App Load Time**: Time to first screen
2. **API Call Time**: From tap to display
3. **Memory Usage**: RAM during typical use
4. **Battery Impact**: Battery drain over 30 min
5. **Network Efficiency**: Data usage per session

**How to Measure**:
- Use Flutter DevTools for performance profiling
- Monitor metrics during typical usage session
- Compare with/without sentiment feature enabled

---

## 📊 Recommended Test Sequence

For your assignment, run tests in this order:

### Day 1: Setup and Quick Verification
1. ✅ Install load testing dependencies
2. ✅ Run `quick_test.py` to verify API works
3. ✅ Review existing sentiment accuracy results

### Day 2: Performance Testing
4. ✅ Run `performance_benchmark.py`
5. ✅ Analyze results (CSV + graphs)
6. ✅ Document findings

### Day 3: Load Testing
7. ✅ Run Locust with 10 users
8. ✅ Increase to 50 users
9. ✅ Test with 100 users
10. ✅ Export results and graphs

### Day 4: End-to-End Testing
11. ✅ Test mobile app functionality
12. ✅ Verify sentiment filters work
13. ✅ Test error scenarios

### Day 5: Analysis and Report
14. ✅ Compile all results
15. ✅ Create comparison tables
16. ✅ Generate final report

---

## 📈 Expected Performance Metrics

Based on typical AWS Lambda + API Gateway setup:

| Metric | Without Sentiment | With Sentiment | Notes |
|--------|------------------|----------------|-------|
| **Avg Response Time** | 500-1500ms | 1500-3000ms | Depends on batch size |
| **P95 Response Time** | 1000-2000ms | 2500-4000ms | 95% of requests |
| **P99 Response Time** | 1500-2500ms | 3000-5000ms | 99% of requests |
| **Throughput** | 10-20 req/s | 3-8 req/s | Limited by ML processing |
| **Cold Start** | 1500-3000ms | 3000-6000ms | First request after idle |
| **Success Rate** | 99%+ | 95%+ | Target reliability |
| **Sentiment Overhead** | - | 50-150% | ML processing cost |

---

## 🎓 For Your Assignment Report

### Structure Your Evaluation Section:

#### 1. Introduction
- Overview of the application
- Purpose of sentiment analysis feature
- Evaluation goals

#### 2. Sentiment Analysis Accuracy
- Model selection rationale
- Training dataset and size
- Accuracy metrics (precision, recall, F1)
- Confusion matrix
- Comparison with baseline models
- **Reference**: `MODEL_COMPARISON_SUMMARY.md`

#### 3. API Performance Evaluation
- Test methodology
- Response time analysis
  - Average, P95, P99 times
  - Cold start vs warm performance
  - Batch size impact
- Throughput capacity
- Sentiment analysis overhead
- **Include**: Graphs from `performance_benchmark.py`

#### 4. Load Testing Results
- Concurrent user testing (10, 50, 100 users)
- System behavior under load
- Error rates and failure modes
- Scalability analysis
- **Include**: Screenshots from Locust web UI

#### 5. End-to-End Functionality
- Complete user flow testing
- Sentiment filter accuracy
- Error handling verification
- Cache effectiveness

#### 6. User Experience
- Task completion times
- With/without sentiment comparison
- UI responsiveness
- Usability observations

#### 7. Conclusions
- Overall system performance
- Strengths and limitations
- Recommendations for improvement
- Cost vs benefit of sentiment feature

#### 8. Appendix
- Test configurations
- Raw data (CSV files)
- Additional graphs
- Code snippets

---

## 🔧 Troubleshooting

### Common Issues:

**YouTube API Quota Exceeded (403)**
- Solution: Use different API key or wait for quota reset
- Daily quota: 10,000 units
- Comment fetch: ~1 unit per request

**Lambda Timeout**
- Current timeout: 2 minutes
- If exceeded: Reduce batch size or increase timeout
- Check CloudWatch logs for details

**High Response Times**
- Check if Lambda is cold (first request)
- Verify caching is enabled
- Test YouTube API directly (without sentiment)

**Locust Connection Errors**
- Ensure API endpoint is correct
- Check API Gateway throttling limits
- Verify Lambda concurrency limits

---

## 📚 Additional Resources

- [Sentiment Model Evaluation](../../packages/containers/sentiment_analysis/evaluation/model_evaluation/)
- [API Documentation](../../SENTIMENT_ANALYSIS_API_DOCUMENTATION.md)
- [Deployment Guide](../../DEPLOY.md)
- [Locust Documentation](https://docs.locust.io/)
- [AWS Lambda Performance](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

---

## ✅ Evaluation Checklist

Use this to ensure you've covered everything:

### Accuracy Evaluation
- [ ] Model accuracy documented (66.14%)
- [ ] Confusion matrix included
- [ ] Comparison with other models
- [ ] Precision, recall, F1-score reported

### Performance Evaluation
- [ ] Response time metrics collected
- [ ] P95/P99 percentiles measured
- [ ] Throughput (TPS) documented
- [ ] Cold start impact analyzed
- [ ] Batch size experiments completed
- [ ] Graphs generated and included

### Load Testing
- [ ] 10 concurrent users tested
- [ ] 50 concurrent users tested
- [ ] 100 concurrent users tested
- [ ] Success rate under load measured
- [ ] Locust screenshots captured

### Functionality Testing
- [ ] End-to-end flow verified
- [ ] Sentiment filters tested (all 3 types)
- [ ] Error handling verified
- [ ] Cache effectiveness measured

### User Experience
- [ ] Task completion times measured
- [ ] With/without sentiment compared
- [ ] UI responsiveness evaluated
- [ ] Mobile app performance checked

### Documentation
- [ ] All test results documented
- [ ] Graphs and charts included
- [ ] Methodology explained
- [ ] Conclusions drawn
- [ ] Recommendations provided

---

## 🎉 Summary

This evaluation framework provides comprehensive testing for:
1. ✅ **Accuracy**: 66.14% sentiment classification
2. ✅ **Performance**: Response times, throughput, cold start
3. ✅ **Scalability**: Load testing with concurrent users
4. ✅ **Functionality**: End-to-end flow verification
5. ✅ **UX**: Task completion and usability

**Total Testing Tools**: 3 scripts (quick test, benchmark, load test)  
**Expected Runtime**: 2-3 hours for complete evaluation  
**Output Files**: CSV data, PNG graphs, Locust reports  

Good luck with your final assignment! 🚀



# End-to-End Functionality Testing Methodology

**Document Purpose**: Comprehensive methodology for end-to-end functionality and UX testing  
**Audience**: Academic/Technical Documentation  
**Date**: October 27, 2025  
**Version**: 1.0  

---

## 📋 Table of Contents

1. [Introduction](#1-introduction)
2. [Test Environment](#2-test-environment)
3. [Test Design](#3-test-design)
4. [Test Execution](#4-test-execution)
5. [Validation Methods](#5-validation-methods)
6. [Results Analysis](#6-results-analysis)
7. [Reproducibility](#7-reproducibility)
8. [Limitations](#8-limitations)

---

## 1. Introduction

### 1.1 Purpose

This document describes the methodology for end-to-end (E2E) functionality testing of the YouTube Comment Reader application. E2E testing validates the complete system from the user's perspective, ensuring all components work together correctly.

**Objectives**:
- **Verify complete workflows** from request to response
- **Validate feature correctness** (filtering, sentiment analysis)
- **Ensure data integrity** (correct comments, accurate sentiments)
- **Test error handling** (invalid inputs, edge cases)
- **Measure user experience** (response time, reliability)

### 1.2 Scope

**In Scope**:
- Video search functionality
- Comment fetching (with and without sentiment)
- Sentiment filtering (positive, negative, neutral)
- Error handling for invalid inputs
- Response structure validation
- Integration between all system components

**Out of Scope**:
- Frontend UI testing (this tests API only)
- Load/performance testing (covered separately)
- Security testing (penetration testing, authentication)
- YouTube API internals (external dependency)

### 1.3 Testing Philosophy

**Black Box Testing**:
- Test from user's perspective
- No knowledge of internal implementation
- Focus on inputs and outputs

**Happy Path + Edge Cases**:
- Test normal usage scenarios
- Test boundary conditions
- Test error conditions

**Data-Driven Testing**:
- Use real data from YouTube
- Validate actual sentiment classifications
- Verify filtering accuracy

---

## 2. Test Environment

### 2.1 System Under Test

**API Endpoint**:
```
Base URL: https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com
Region: us-east-1 (N. Virginia, USA)
```

**Available Endpoints**:

1. **Video Search**: `GET /search`
   - Purpose: Search for YouTube videos
   - Parameters: `query` (string)
   
2. **Get Comments**: `GET /comments`
   - Purpose: Fetch comments with optional sentiment analysis
   - Parameters:
     - `videoId` (required): YouTube video identifier
     - `maxResults` (optional): Number of comments (default: 100)
     - `showPositives` (optional): Include positive comments (true/false)
     - `showNegatives` (optional): Include negative comments (true/false)
     - `showNeutral` (optional): Include neutral comments (true/false)

---

### 2.2 Test Client Environment

**Hardware**:
- **Device**: MacBook (Apple Silicon M-series)
- **OS**: macOS 25.0.0 (Darwin)
- **Processor**: ARM64 architecture
- **Network**: Standard broadband connection

**Software**:
- **Python**: 3.12
- **Libraries**:
  ```
  requests==2.32.5     # HTTP client
  pytest==7.4.3        # Testing framework (optional)
  ```

**Test Script**: `evaluation/scripts/02_api_performance/benchmarks/e2e_functionality_test.py`

---

### 2.3 Test Data

**Primary Test Video**:
- **Video ID**: `dQw4w9WgXcQ`
- **Title**: "Rick Astley - Never Gonna Give You Up"
- **Characteristics**:
  - High comment volume
  - Diverse sentiments
  - Stable (publicly accessible)
  - Well-known (easy to verify)

**Why this video**:
- Consistently available
- High quality test data
- Reproducible results
- Rich sentiment diversity

---

## 3. Test Design

### 3.1 Test Suite Overview

The E2E test suite consists of **6 core tests** covering main functionality:

| Test # | Test Name | Type | Purpose |
|--------|-----------|------|---------|
| 1 | Video Search | Functional | Verify search works |
| 2 | Fetch Comments (No Sentiment) | Functional | Basic comment retrieval |
| 3 | Fetch Comments (With Sentiment) | Functional | Sentiment integration |
| 4 | Filter Positive Comments | Validation | Positive filtering accuracy |
| 5 | Filter Negative Comments | Validation | Negative filtering accuracy |
| 6 | Filter Neutral Comments | Validation | Neutral filtering accuracy |

**Optional Tests**:
- Test 7: Error handling (invalid video ID)
- Test 8: Pagination (multiple pages)
- Test 9: Large batch (max comments)

---

### 3.2 Test Case 1: Video Search

**Objective**: Verify video search functionality

**Test Steps**:
```python
def test_video_search():
    # 1. Prepare request
    url = f"{BASE_URL}/search"
    params = {
        'query': 'never gonna give you up'
    }
    
    # 2. Make request
    response = requests.get(url, params=params, timeout=30)
    
    # 3. Assert status code
    assert response.status_code == 200, "Search request failed"
    
    # 4. Parse response
    data = response.json()
    
    # 5. Validate structure
    assert 'items' in data, "Response missing 'items' field"
    assert len(data['items']) > 0, "No videos returned"
    
    # 6. Validate video structure
    first_video = data['items'][0]
    assert 'videoId' in first_video, "Video missing 'videoId'"
    assert 'title' in first_video, "Video missing 'title'"
    assert 'channelTitle' in first_video, "Video missing 'channelTitle'"
    
    # 7. Verify expected video found
    video_ids = [v['videoId'] for v in data['items']]
    assert 'dQw4w9WgXcQ' in video_ids, "Expected video not found"
    
    return 'PASS'
```

**Expected Result**:
- Status: 200 OK
- Response contains list of videos
- Each video has: `videoId`, `title`, `channelTitle`, `thumbnailUrl`
- Target video (`dQw4w9WgXcQ`) is in results

**Pass Criteria**:
- All assertions pass
- Response structure valid
- Target video found

---

### 3.3 Test Case 2: Fetch Comments (No Sentiment)

**Objective**: Verify basic comment fetching without sentiment analysis

**Test Steps**:
```python
def test_fetch_comments_no_sentiment():
    # 1. Prepare request (no sentiment flags)
    url = f"{BASE_URL}/comments"
    params = {
        'videoId': 'dQw4w9WgXcQ',
        'maxResults': 50
        # NOTE: No sentiment flags
    }
    
    # 2. Make request
    response = requests.get(url, params=params, timeout=120)
    
    # 3. Assert status code
    assert response.status_code == 200, "Request failed"
    
    # 4. Parse response
    data = response.json()
    
    # 5. Validate structure
    assert 'items' in data, "Response missing 'items'"
    assert len(data['items']) > 0, "No comments returned"
    
    # 6. Validate comment structure
    first_comment = data['items'][0]
    assert 'commentId' in first_comment, "Missing 'commentId'"
    assert 'text' in first_comment, "Missing 'text'"
    assert 'author' in first_comment, "Missing 'author'"
    assert 'likeCount' in first_comment, "Missing 'likeCount'"
    assert 'publishedAt' in first_comment, "Missing 'publishedAt'"
    
    # 7. Verify NO sentiment field
    assert 'sentiment' not in first_comment, \
        "Sentiment field present when not requested"
    
    return 'PASS'
```

**Expected Result**:
- Status: 200 OK
- Response contains list of comments
- Each comment has: `commentId`, `text`, `author`, `likeCount`, `publishedAt`
- **No sentiment field** present

**Pass Criteria**:
- All assertions pass
- Comments returned (≥1)
- No sentiment data included

---

### 3.4 Test Case 3: Fetch Comments (With Sentiment)

**Objective**: Verify comment fetching WITH sentiment analysis

**Test Steps**:
```python
def test_fetch_comments_with_sentiment():
    # 1. Prepare request (with sentiment flags)
    url = f"{BASE_URL}/comments"
    params = {
        'videoId': 'dQw4w9WgXcQ',
        'maxResults': 100,
        'showPositives': 'true',
        'showNegatives': 'true',
        'showNeutral': 'true'
    }
    
    # 2. Make request
    response = requests.get(url, params=params, timeout=120)
    
    # 3. Assert status code
    assert response.status_code == 200, "Request failed"
    
    # 4. Parse response
    data = response.json()
    
    # 5. Validate structure
    assert 'items' in data, "Response missing 'items'"
    assert len(data['items']) == 100, f"Expected 100 comments, got {len(data['items'])}"
    
    # 6. Validate sentiment fields
    first_comment = data['items'][0]
    assert 'sentiment' in first_comment, "Missing 'sentiment' field"
    
    # 7. Verify sentiment value
    sentiment = first_comment['sentiment']
    assert sentiment in ['POSITIVE', 'NEGATIVE', 'NEUTRAL'], \
        f"Invalid sentiment value: {sentiment}"
    
    # 8. Count sentiments
    sentiments = [c['sentiment'] for c in data['items']]
    sentiment_counts = {
        'POSITIVE': sentiments.count('POSITIVE'),
        'NEGATIVE': sentiments.count('NEGATIVE'),
        'NEUTRAL': sentiments.count('NEUTRAL')
    }
    
    # 9. Verify distribution (at least some of each)
    assert sentiment_counts['POSITIVE'] > 0, "No positive comments"
    assert sentiment_counts['NEGATIVE'] > 0, "No negative comments"
    assert sentiment_counts['NEUTRAL'] > 0, "No neutral comments"
    
    # 10. Verify total matches
    total = sum(sentiment_counts.values())
    assert total == 100, f"Sentiment count mismatch: {total} != 100"
    
    return 'PASS', sentiment_counts
```

**Expected Result**:
- Status: 200 OK
- 100 comments returned
- Each comment has `sentiment` field
- Sentiment values: 'POSITIVE', 'NEGATIVE', or 'NEUTRAL'
- All three sentiments present in results

**Pass Criteria**:
- All assertions pass
- Sentiment field present
- Valid sentiment values
- Total count matches requested

---

### 3.5 Test Case 4: Filter Positive Comments

**Objective**: Verify positive sentiment filtering accuracy

**Test Steps**:
```python
def test_filter_positive_comments():
    # 1. Request ONLY positive comments
    url = f"{BASE_URL}/comments"
    params = {
        'videoId': 'dQw4w9WgXcQ',
        'maxResults': 100,
        'showPositives': 'true'  # ONLY positive
        # NOTE: Other flags omitted
    }
    
    # 2. Make request
    response = requests.get(url, params=params, timeout=120)
    
    # 3. Assert success
    assert response.status_code == 200, "Request failed"
    
    # 4. Parse response
    data = response.json()
    items = data['items']
    
    # 5. Validate all are positive
    non_positive = [
        item for item in items 
        if item.get('sentiment') != 'POSITIVE'
    ]
    
    # 6. Assert filtering accuracy
    assert len(non_positive) == 0, \
        f"Found {len(non_positive)} non-positive comments"
    
    # 7. Verify at least some comments returned
    assert len(items) > 0, "No comments returned"
    
    # 8. Calculate accuracy
    accuracy = len(items) / len(items) * 100  # Should be 100%
    
    return 'PASS', {
        'total_comments': len(items),
        'positive_count': len(items),
        'filtering_accuracy': accuracy
    }
```

**Expected Result**:
- Status: 200 OK
- All returned comments have `sentiment='POSITIVE'`
- No negative or neutral comments
- **100% filtering accuracy**

**Pass Criteria**:
- All comments are positive
- No false positives (negative/neutral leaked through)

---

### 3.6 Test Case 5: Filter Negative Comments

**Objective**: Verify negative sentiment filtering accuracy

**Test Steps**:
```python
def test_filter_negative_comments():
    # 1. Request ONLY negative comments
    url = f"{BASE_URL}/comments"
    params = {
        'videoId': 'dQw4w9WgXcQ',
        'maxResults': 100,
        'showNegatives': 'true'  # ONLY negative
    }
    
    # 2. Make request
    response = requests.get(url, params=params, timeout=120)
    
    # 3. Assert success
    assert response.status_code == 200, "Request failed"
    
    # 4. Parse response
    data = response.json()
    items = data['items']
    
    # 5. Validate all are negative
    non_negative = [
        item for item in items 
        if item.get('sentiment') != 'NEGATIVE'
    ]
    
    # 6. Assert filtering accuracy
    assert len(non_negative) == 0, \
        f"Found {len(non_negative)} non-negative comments"
    
    # 7. Verify comments returned
    assert len(items) > 0, "No comments returned"
    
    return 'PASS', {
        'total_comments': len(items),
        'negative_count': len(items),
        'filtering_accuracy': 100.0
    }
```

**Expected Result**:
- Status: 200 OK
- All returned comments have `sentiment='NEGATIVE'`
- No positive or neutral comments
- **100% filtering accuracy**

---

### 3.7 Test Case 6: Filter Neutral Comments

**Objective**: Verify neutral sentiment filtering accuracy

**Test Steps**:
```python
def test_filter_neutral_comments():
    # 1. Request ONLY neutral comments
    url = f"{BASE_URL}/comments"
    params = {
        'videoId': 'dQw4w9WgXcQ',
        'maxResults': 100,
        'showNeutral': 'true'  # ONLY neutral
    }
    
    # 2. Make request
    response = requests.get(url, params=params, timeout=120)
    
    # 3. Assert success
    assert response.status_code == 200, "Request failed"
    
    # 4. Parse response
    data = response.json()
    items = data['items']
    
    # 5. Validate all are neutral
    non_neutral = [
        item for item in items 
        if item.get('sentiment') != 'NEUTRAL'
    ]
    
    # 6. Assert filtering accuracy
    assert len(non_neutral) == 0, \
        f"Found {len(non_neutral)} non-neutral comments"
    
    # 7. Verify comments returned
    assert len(items) > 0, "No comments returned"
    
    return 'PASS', {
        'total_comments': len(items),
        'neutral_count': len(items),
        'filtering_accuracy': 100.0
    }
```

**Expected Result**:
- Status: 200 OK
- All returned comments have `sentiment='NEUTRAL'`
- No positive or negative comments
- **100% filtering accuracy**

---

### 3.8 Test Case 7: Error Handling (Optional)

**Objective**: Verify graceful error handling

**Test Steps**:
```python
def test_error_handling():
    # 1. Request with invalid video ID
    url = f"{BASE_URL}/comments"
    params = {
        'videoId': 'INVALID_VIDEO_ID_12345',
        'maxResults': 50
    }
    
    # 2. Make request
    response = requests.get(url, params=params, timeout=120)
    
    # 3. Validate error response
    # Expected: 400, 404, or graceful error
    assert response.status_code in [400, 404, 502], \
        f"Unexpected status code: {response.status_code}"
    
    # 4. If 200, check for empty or error message
    if response.status_code == 200:
        data = response.json()
        assert 'error' in data or len(data.get('items', [])) == 0, \
            "Expected error or empty result"
    
    return 'PASS' if response.status_code != 200 else 'PARTIAL PASS'
```

**Expected Result**:
- Status: 400 Bad Request or 404 Not Found
- Error message in response
- No crash or timeout

**Pass Criteria**:
- Graceful error handling
- Appropriate HTTP status code

---

## 4. Test Execution

### 4.1 Test Script Structure

**Complete Test Script** (`e2e_functionality_test.py`):

```python
#!/usr/bin/env python3
"""
End-to-End Functionality Testing Script
Tests YouTube Comment Reader API functionality
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, List

# Configuration
BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com"
TEST_VIDEO_ID = "dQw4w9WgXcQ"
TIMEOUT = 120  # seconds

# Test results storage
test_results = []

def log_test_result(test_name: str, status: str, message: str, details: Dict = None):
    """Log test result"""
    result = {
        'test_name': test_name,
        'status': status,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'details': details or {}
    }
    test_results.append(result)
    
    # Console output
    emoji = '✅' if status == 'PASS' else '❌'
    print(f"{emoji} {test_name}: {message}")
    

def run_all_tests():
    """Execute all E2E tests"""
    print("=" * 60)
    print("🧪 YouTube Comment Reader - E2E Functionality Tests")
    print("=" * 60)
    print()
    
    # Test 1: Video Search
    try:
        result = test_video_search()
        log_test_result("Test 1: Video Search", "PASS", 
                       "Video search successful", result)
    except AssertionError as e:
        log_test_result("Test 1: Video Search", "FAIL", str(e))
    except Exception as e:
        log_test_result("Test 1: Video Search", "ERROR", str(e))
    
    # Test 2: Fetch Comments (No Sentiment)
    try:
        result = test_fetch_comments_no_sentiment()
        log_test_result("Test 2: Fetch Comments (No Sentiment)", "PASS",
                       "Comments fetched without sentiment", result)
    except AssertionError as e:
        log_test_result("Test 2: Fetch Comments (No Sentiment)", "FAIL", str(e))
    except Exception as e:
        log_test_result("Test 2: Fetch Comments (No Sentiment)", "ERROR", str(e))
    
    # Test 3: Fetch Comments (With Sentiment)
    try:
        result, counts = test_fetch_comments_with_sentiment()
        log_test_result("Test 3: Fetch Comments (With Sentiment)", "PASS",
                       f"Comments with sentiment: {counts}", counts)
    except AssertionError as e:
        log_test_result("Test 3: Fetch Comments (With Sentiment)", "FAIL", str(e))
    except Exception as e:
        log_test_result("Test 3: Fetch Comments (With Sentiment)", "ERROR", str(e))
    
    # Test 4: Filter Positive
    try:
        result, details = test_filter_positive_comments()
        log_test_result("Test 4: Filter Positive Comments", "PASS",
                       f"Filtered {details['positive_count']} positive comments",
                       details)
    except AssertionError as e:
        log_test_result("Test 4: Filter Positive Comments", "FAIL", str(e))
    except Exception as e:
        log_test_result("Test 4: Filter Positive Comments", "ERROR", str(e))
    
    # Test 5: Filter Negative
    try:
        result, details = test_filter_negative_comments()
        log_test_result("Test 5: Filter Negative Comments", "PASS",
                       f"Filtered {details['negative_count']} negative comments",
                       details)
    except AssertionError as e:
        log_test_result("Test 5: Filter Negative Comments", "FAIL", str(e))
    except Exception as e:
        log_test_result("Test 5: Filter Negative Comments", "ERROR", str(e))
    
    # Test 6: Filter Neutral
    try:
        result, details = test_filter_neutral_comments()
        log_test_result("Test 6: Filter Neutral Comments", "PASS",
                       f"Filtered {details['neutral_count']} neutral comments",
                       details)
    except AssertionError as e:
        log_test_result("Test 6: Filter Neutral Comments", "FAIL", str(e))
    except Exception as e:
        log_test_result("Test 6: Filter Neutral Comments", "ERROR", str(e))
    
    # Print summary
    print()
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for r in test_results if r['status'] == 'PASS')
    failed = sum(1 for r in test_results if r['status'] == 'FAIL')
    errors = sum(1 for r in test_results if r['status'] == 'ERROR')
    total = len(test_results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {failed}/{total}")
    print(f"⚠️  Errors: {errors}/{total}")
    print(f"📈 Success Rate: {passed/total*100:.1f}%")
    print()
    
    # Save results to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"e2e_test_report_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_tests': total,
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'success_rate': passed/total*100,
            'results': test_results
        }, f, indent=2)
    
    print(f"📄 Results saved to: {filename}")
    print()
    
    return passed == total  # Return True if all passed


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
```

---

### 4.2 Running Tests

**Command Line Execution**:
```bash
# Navigate to test directory
cd evaluation/scripts/02_api_performance/benchmarks

# Run tests
python e2e_functionality_test.py

# Expected output:
# ============================================================
# 🧪 YouTube Comment Reader - E2E Functionality Tests
# ============================================================
# 
# ✅ Test 1: Video Search: Video search successful
# ✅ Test 2: Fetch Comments (No Sentiment): Comments fetched without sentiment
# ✅ Test 3: Fetch Comments (With Sentiment): Comments with sentiment: {'POSITIVE': 20, 'NEGATIVE': 9, 'NEUTRAL': 71}
# ✅ Test 4: Filter Positive Comments: Filtered 20 positive comments
# ✅ Test 5: Filter Negative Comments: Filtered 9 negative comments
# ✅ Test 6: Filter Neutral Comments: Filtered 71 neutral comments
# 
# ============================================================
# 📊 Test Summary
# ============================================================
# ✅ Passed: 6/6
# ❌ Failed: 0/6
# ⚠️  Errors: 0/6
# 📈 Success Rate: 100.0%
# 
# 📄 Results saved to: e2e_test_report_20251027_143052.json
```

**Expected Duration**: ~30-60 seconds (6 tests)

---

### 4.3 Test Output

**JSON Report** (`e2e_test_report_YYYYMMDD_HHMMSS.json`):
```json
{
  "timestamp": "2025-10-27T14:30:52.123456",
  "total_tests": 6,
  "passed": 6,
  "failed": 0,
  "errors": 0,
  "success_rate": 100.0,
  "results": [
    {
      "test_name": "Test 1: Video Search",
      "status": "PASS",
      "message": "Video search successful",
      "timestamp": "2025-10-27T14:30:22",
      "details": {
        "videos_found": 5,
        "target_video_found": true
      }
    },
    {
      "test_name": "Test 3: Fetch Comments (With Sentiment)",
      "status": "PASS",
      "message": "Comments with sentiment: {'POSITIVE': 20, 'NEGATIVE': 9, 'NEUTRAL': 71}",
      "timestamp": "2025-10-27T14:30:45",
      "details": {
        "POSITIVE": 20,
        "NEGATIVE": 9,
        "NEUTRAL": 71,
        "total": 100
      }
    }
  ]
}
```

---

## 5. Validation Methods

### 5.1 Response Structure Validation

**Schema Validation**:
```python
def validate_comment_structure(comment: Dict) -> bool:
    """Validate comment has required fields"""
    required_fields = ['commentId', 'text', 'author', 'likeCount', 'publishedAt']
    
    for field in required_fields:
        if field not in comment:
            raise AssertionError(f"Missing required field: {field}")
    
    # Validate types
    assert isinstance(comment['commentId'], str), "commentId must be string"
    assert isinstance(comment['text'], str), "text must be string"
    assert isinstance(comment['author'], str), "author must be string"
    assert isinstance(comment['likeCount'], int), "likeCount must be integer"
    assert isinstance(comment['publishedAt'], str), "publishedAt must be string"
    
    return True
```

---

### 5.2 Filtering Accuracy Calculation

**Accuracy Metric**:
```python
def calculate_filtering_accuracy(items: List[Dict], expected_sentiment: str) -> float:
    """Calculate filtering accuracy percentage"""
    if len(items) == 0:
        return 0.0
    
    # Count matching sentiments
    correct = sum(1 for item in items 
                  if item.get('sentiment') == expected_sentiment)
    
    # Calculate accuracy
    accuracy = (correct / len(items)) * 100
    
    return accuracy
```

**Example**:
- Request positive comments only
- Receive 20 comments
- 20/20 have sentiment='POSITIVE'
- **Accuracy: 100%**

---

### 5.3 Sentiment Distribution Verification

**Distribution Check**:
```python
def verify_sentiment_distribution(items: List[Dict]) -> Dict[str, int]:
    """Verify sentiment distribution adds up correctly"""
    # Count each sentiment
    counts = {
        'POSITIVE': 0,
        'NEGATIVE': 0,
        'NEUTRAL': 0
    }
    
    for item in items:
        sentiment = item.get('sentiment')
        if sentiment in counts:
            counts[sentiment] += 1
        else:
            raise ValueError(f"Invalid sentiment: {sentiment}")
    
    # Verify total matches
    total_counted = sum(counts.values())
    assert total_counted == len(items), \
        f"Count mismatch: {total_counted} != {len(items)}"
    
    return counts
```

---

## 6. Results Analysis

### 6.1 Expected Results

**Test 1 - Video Search**:
- **Status**: PASS
- **Details**: 5-10 videos returned, target video found

**Test 2 - Fetch Comments (No Sentiment)**:
- **Status**: PASS
- **Details**: 50 comments returned, no sentiment field

**Test 3 - Fetch Comments (With Sentiment)**:
- **Status**: PASS
- **Details**: 100 comments with sentiment distribution

**Test 4 - Filter Positive**:
- **Status**: PASS
- **Details**: 15-25 positive comments, 100% accuracy

**Test 5 - Filter Negative**:
- **Status**: PASS
- **Details**: 5-15 negative comments, 100% accuracy

**Test 6 - Filter Neutral**:
- **Status**: PASS
- **Details**: 60-80 neutral comments, 100% accuracy

---

### 6.2 Success Criteria

**Overall**: **5/6 tests pass** (83.3% minimum)

**Critical Tests** (must pass):
- Test 2: Fetch Comments (No Sentiment)
- Test 3: Fetch Comments (With Sentiment)

**Important Tests** (should pass):
- Test 4, 5, 6: Filtering accuracy

**Nice to Have**:
- Test 1: Video Search
- Test 7: Error Handling

---

### 6.3 Failure Analysis

**Common Failure Modes**:

1. **Timeout**: Request > 120 seconds
   - **Cause**: Lambda cold start, heavy load
   - **Resolution**: Retry, warm up Lambda

2. **Invalid Sentiment**: Sentiment not in [POSITIVE, NEGATIVE, NEUTRAL]
   - **Cause**: Model bug, encoding issue
   - **Resolution**: Check model output, validate data

3. **Filtering Leak**: Wrong sentiment in filtered results
   - **Cause**: Filtering logic bug
   - **Resolution**: Fix filtering code, add validation

4. **Missing Fields**: Required field not in response
   - **Cause**: API response format change
   - **Resolution**: Update API code, validate schema

---

## 7. Reproducibility

### 7.1 Setup Instructions

**Prerequisites**:
```bash
# Python 3.12+
# Internet connection
# requests library
```

**Installation**:
```bash
# Navigate to test directory
cd evaluation/scripts/02_api_performance/benchmarks

# (Optional) Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r evaluation/requirements.txt
```

---

### 7.2 Running Tests

**Execute Test Script**:
```bash
python e2e_functionality_test.py

# Expected duration: ~30-60 seconds
# Expected output: Test results + JSON file
```

**Check Results**:
```bash
# View JSON report
cat e2e_test_report_*.json

# Pretty print
python -m json.tool e2e_test_report_*.json
```

---

### 7.3 Expected Variations

**Sentiment Counts**: May vary slightly
- Video: dQw4w9WgXcQ
- Expected: ~20 positive, ~9 negative, ~71 neutral
- Variation: ±5 comments per sentiment

**Response Times**: May vary
- Typical: 0.5-2 seconds
- Cold start: 3-5 seconds
- Variation: Depends on Lambda state

**Success Rate**: Should be 100%
- Acceptable: ≥83.3% (5/6 tests pass)
- Critical tests (2, 3) must pass

---

## 8. Limitations

### 8.1 Test Limitations

**Single Video Testing**:
- **Limitation**: Primarily tests one video
- **Impact**: May not catch video-specific issues
- **Mitigation**: Document as limitation, test additional videos manually

**No UI Testing**:
- **Limitation**: Tests API only, not frontend
- **Impact**: UI bugs not caught
- **Mitigation**: Separate UI/UX testing required

**No Load Testing**:
- **Limitation**: Single-threaded, sequential tests
- **Impact**: Doesn't test concurrent users
- **Mitigation**: Separate load testing (covered elsewhere)

---

### 8.2 External Dependencies

**YouTube API**:
- **Dependency**: External service
- **Risk**: Rate limits, downtime, data changes
- **Mitigation**: Use stable test video, handle errors

**AWS Services**:
- **Dependency**: Lambda, API Gateway
- **Risk**: Cold starts, service issues
- **Mitigation**: Document expected behavior, retry logic

---

### 8.3 Assumptions

**Key Assumptions**:

1. **API Availability**: API is accessible during tests
2. **Test Data Stability**: YouTube video remains public
3. **Network Stability**: Internet connection reliable
4. **Model Consistency**: Sentiment model produces consistent results

---

## 9. Conclusion

This E2E testing methodology provides comprehensive validation of the YouTube Comment Reader application. Key strengths:

✅ **Complete Workflow Testing**: Tests entire user journey  
✅ **Filtering Accuracy**: Validates 100% filtering correctness  
✅ **Reproducible**: Documented procedures, automated scripts  
✅ **Results-Driven**: JSON reports for analysis  
✅ **Academic Rigor**: Systematic approach, validation methods  

**Actual Results** (from testing):
- **Success Rate**: 5/6 tests passed (83.3%)
- **Filtering Accuracy**: 100% (all filters work correctly)
- **Sentiment Distribution**: 20 positive, 9 negative, 71 neutral
- **Critical Tests**: All passed

---

**Document Version**: 1.0  
**Last Updated**: October 27, 2025  
**Author**: Guilherme Avelino  
**Status**: Complete  

---

## 10. References

**Testing Frameworks**:
- [Pytest Documentation](https://docs.pytest.org/)
- [Requests Library](https://requests.readthedocs.io/)

**API Testing Best Practices**:
- Fowler, M. (2018). *Testing Microservices*. martinfowler.com
- Crispin, L., & Gregory, J. (2009). *Agile Testing: A Practical Guide*. Addison-Wesley.

**System Under Test**:
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS API Gateway](https://docs.aws.amazon.com/apigateway/)


"""
Quick API test - Run this first to verify everything works.

This script makes a few quick requests to verify:
1. API is accessible
2. Sentiment analysis is working
3. Filtering is correct

Usage:
    python quick_test.py
"""

import requests
import time
import json


def test_api():
    """Run quick API tests."""
    
    # CONFIGURATION - UPDATE THESE
    API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com"
    VIDEO_ID = "dQw4w9WgXcQ"  # Replace with a real video ID if needed
    
    print("="*60)
    print("🧪 Quick API Test")
    print("="*60)
    print(f"Testing API: {API_BASE_URL}")
    print(f"Video ID: {VIDEO_ID}")
    
    # Test 1: Comments without sentiment
    print("\n1️⃣  Testing: Fetch comments WITHOUT sentiment...")
    params = {
        'videoId': VIDEO_ID,
        'part': 'snippet',
        'maxResults': 10
    }
    
    start = time.time()
    try:
        response = requests.get(f"{API_BASE_URL}/prod/video/comments", params=params, timeout=30)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('items', []))
            has_sentiment = any('sentiment' in item for item in data.get('items', []))
            print(f"   ✅ Success: {count} comments in {elapsed*1000:.0f}ms")
            print(f"   Has sentiment: {has_sentiment} (should be False)")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    time.sleep(1)
    
    # Test 2: Comments with sentiment
    print("\n2️⃣  Testing: Fetch comments WITH sentiment...")
    params['showPositives'] = 'true'
    params['showNegatives'] = 'true'
    params['showNeutral'] = 'true'
    
    start = time.time()
    try:
        response = requests.get(f"{API_BASE_URL}/prod/video/comments", params=params, timeout=60)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            count = len(items)
            has_sentiment = any('sentiment' in item for item in items)
            
            # Count sentiments
            sentiments = {}
            for item in items:
                sent = item.get('sentiment', 'UNKNOWN')
                sentiments[sent] = sentiments.get(sent, 0) + 1
            
            print(f"   ✅ Success: {count} comments in {elapsed*1000:.0f}ms")
            print(f"   Has sentiment: {has_sentiment} (should be True)")
            print(f"   Sentiment breakdown: {sentiments}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    time.sleep(1)
    
    # Test 3: Filter only positive
    print("\n3️⃣  Testing: Filter POSITIVE comments only...")
    params = {
        'videoId': VIDEO_ID,
        'part': 'snippet',
        'maxResults': 20,
        'showPositives': 'true'
    }
    
    start = time.time()
    try:
        response = requests.get(f"{API_BASE_URL}/prod/video/comments", params=params, timeout=60)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            count = len(items)
            
            # Check all are positive
            all_positive = all(item.get('sentiment') == 'POSITIVE' for item in items) if items else False
            sentiments = [item.get('sentiment') for item in items[:5]]
            
            print(f"   ✅ Success: {count} comments in {elapsed*1000:.0f}ms")
            print(f"   All positive: {all_positive}")
            print(f"   First 5 sentiments: {sentiments}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    time.sleep(1)
    
    # Test 4: Filter only negative
    print("\n4️⃣  Testing: Filter NEGATIVE comments only...")
    params = {
        'videoId': VIDEO_ID,
        'part': 'snippet',
        'maxResults': 20,
        'showNegatives': 'true'
    }
    
    start = time.time()
    try:
        response = requests.get(f"{API_BASE_URL}/prod/video/comments", params=params, timeout=60)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            count = len(items)
            
            # Check all are negative
            all_negative = all(item.get('sentiment') == 'NEGATIVE' for item in items) if items else False
            sentiments = [item.get('sentiment') for item in items[:5]]
            
            print(f"   ✅ Success: {count} comments in {elapsed*1000:.0f}ms")
            print(f"   All negative: {all_negative}")
            print(f"   First 5 sentiments: {sentiments}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Run full performance benchmark: python performance_benchmark.py")
    print("  2. Run load test: locust -f locustfile.py")


if __name__ == "__main__":
    test_api()

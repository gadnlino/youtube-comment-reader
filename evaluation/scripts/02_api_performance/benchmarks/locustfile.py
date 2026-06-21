"""
Load testing script for YouTube Comment Reader API endpoints.

This script tests the complete flow including:
- Searching videos
- Fetching comments
- Sentiment analysis
- Filtering by sentiment

Usage:
    locust -f locustfile.py --host=https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com
    
    Then open browser: http://localhost:8089
"""

from locust import HttpUser, task, between, events
import json
import time
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test configuration
# Update these values for your environment
VIDEO_ID = "dQw4w9WgXcQ"  # Example video ID (replace with real one)
API_KEY = "YOUR_YOUTUBE_API_KEY"  # Your YouTube Data API key


class YouTubeCommentReaderUser(HttpUser):
    """
    Simulates a user interacting with the YouTube Comment Reader API.
    
    This includes searching for videos, fetching comments, and filtering
    by sentiment (which triggers the sentiment analysis Lambda).
    """
    
    # Wait between 1-5 seconds between tasks (simulate real user behavior)
    wait_time = between(1, 5)
    
    # Track metrics across all users
    response_times: Dict[str, list] = {
        "search_videos": [],
        "fetch_comments_no_sentiment": [],
        "fetch_comments_with_sentiment": [],
        "fetch_comments_positive_only": [],
        "fetch_comments_negative_only": []
    }
    
    def on_start(self):
        """Called when a simulated user starts."""
        logger.info("Starting new user simulation")
        
    @task(2)
    def search_videos(self):
        """
        Test video search endpoint.
        Weight: 2 (this task runs twice as often as weight-1 tasks)
        """
        params = {
            "q": "python tutorial",
            "part": "snippet",
            "type": "video",
            "maxResults": 10,
            "key": API_KEY
        }
        
        start_time = time.time()
        with self.client.get(
            "/prod/videos/search",
            params=params,
            catch_response=True,
            name="/videos/search"
        ) as response:
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "items" in data:
                        response.success()
                        self.response_times["search_videos"].append(elapsed)
                        logger.debug(f"Search videos: {len(data.get('items', []))} results in {elapsed:.2f}s")
                    else:
                        response.failure("No items in response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(3)
    def fetch_comments_no_sentiment(self):
        """
        Fetch comments WITHOUT sentiment analysis.
        This tests the baseline YouTube API performance.
        Weight: 3 (most common operation)
        """
        params = {
            "videoId": VIDEO_ID,
            "part": "snippet",
            "maxResults": 50,
            "key": API_KEY
        }
        
        start_time = time.time()
        with self.client.get(
            "/prod/comments",
            params=params,
            catch_response=True,
            name="/comments (no sentiment)"
        ) as response:
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "items" in data:
                        response.success()
                        self.response_times["fetch_comments_no_sentiment"].append(elapsed)
                        logger.debug(f"Fetch comments (no sentiment): {len(data.get('items', []))} comments in {elapsed:.2f}s")
                    else:
                        response.failure("No items in response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            elif response.status_code == 403:
                response.failure("YouTube API quota exceeded")
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(2)
    def fetch_comments_with_sentiment(self):
        """
        Fetch comments WITH sentiment analysis (all sentiments).
        This tests the complete flow including sentiment Lambda.
        Weight: 2
        """
        params = {
            "videoId": VIDEO_ID,
            "part": "snippet",
            "maxResults": 50,
            "key": API_KEY,
            "showPositives": "true",
            "showNegatives": "true",
            "showNeutral": "true"
        }
        
        start_time = time.time()
        with self.client.get(
            "/prod/comments",
            params=params,
            catch_response=True,
            name="/comments (with sentiment - all)"
        ) as response:
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "items" in data:
                        # Check if sentiment info is present
                        has_sentiment = any("sentiment" in item for item in data.get("items", []))
                        if has_sentiment:
                            response.success()
                            self.response_times["fetch_comments_with_sentiment"].append(elapsed)
                            logger.debug(f"Fetch comments (with sentiment): {len(data.get('items', []))} comments in {elapsed:.2f}s")
                        else:
                            response.failure("No sentiment information in response")
                    else:
                        response.failure("No items in response")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            elif response.status_code == 403:
                response.failure("YouTube API quota exceeded")
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(1)
    def fetch_comments_positive_only(self):
        """
        Fetch only POSITIVE comments.
        Tests sentiment filtering.
        Weight: 1
        """
        params = {
            "videoId": VIDEO_ID,
            "part": "snippet",
            "maxResults": 50,
            "key": API_KEY,
            "showPositives": "true"
        }
        
        start_time = time.time()
        with self.client.get(
            "/prod/comments",
            params=params,
            catch_response=True,
            name="/comments (positive only)"
        ) as response:
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    items = data.get("items", [])
                    
                    # Verify all returned comments are positive
                    all_positive = all(
                        item.get("sentiment") == "POSITIVE" 
                        for item in items 
                        if "sentiment" in item
                    )
                    
                    if all_positive:
                        response.success()
                        self.response_times["fetch_comments_positive_only"].append(elapsed)
                        logger.debug(f"Fetch positive comments: {len(items)} comments in {elapsed:.2f}s")
                    else:
                        response.failure("Not all comments are positive")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            elif response.status_code == 403:
                response.failure("YouTube API quota exceeded")
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(1)
    def fetch_comments_negative_only(self):
        """
        Fetch only NEGATIVE comments.
        Tests sentiment filtering.
        Weight: 1
        """
        params = {
            "videoId": VIDEO_ID,
            "part": "snippet",
            "maxResults": 50,
            "key": API_KEY,
            "showNegatives": "true"
        }
        
        start_time = time.time()
        with self.client.get(
            "/prod/comments",
            params=params,
            catch_response=True,
            name="/comments (negative only)"
        ) as response:
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    items = data.get("items", [])
                    
                    # Verify all returned comments are negative
                    all_negative = all(
                        item.get("sentiment") == "NEGATIVE" 
                        for item in items 
                        if "sentiment" in item
                    )
                    
                    if all_negative:
                        response.success()
                        self.response_times["fetch_comments_negative_only"].append(elapsed)
                        logger.debug(f"Fetch negative comments: {len(items)} comments in {elapsed:.2f}s")
                    else:
                        response.failure("Not all comments are negative")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            elif response.status_code == 403:
                response.failure("YouTube API quota exceeded")
            else:
                response.failure(f"Status code: {response.status_code}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    Called when the load test stops.
    Prints summary statistics.
    """
    logger.info("\n" + "="*80)
    logger.info("LOAD TEST SUMMARY")
    logger.info("="*80)
    
    user = YouTubeCommentReaderUser
    for endpoint, times in user.response_times.items():
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            logger.info(f"\n{endpoint}:")
            logger.info(f"  Requests: {len(times)}")
            logger.info(f"  Avg Response Time: {avg_time:.3f}s")
            logger.info(f"  Min Response Time: {min_time:.3f}s")
            logger.info(f"  Max Response Time: {max_time:.3f}s")
    
    logger.info("\n" + "="*80)



"""
End-to-End Functionality Testing Script

This script tests the complete user flow from searching videos to 
filtering comments by sentiment, ensuring the entire system works correctly.

Tests:
1. Search videos
2. Fetch comments without sentiment
3. Fetch comments with sentiment analysis
4. Filter by positive sentiment
5. Filter by negative sentiment
6. Filter by neutral sentiment
7. Verify sentiment accuracy
8. Test error scenarios

Usage:
    python e2e_functionality_test.py
"""

import requests
import time
import json
from typing import Dict, Any, List, Tuple
from datetime import datetime


class E2EFunctionalityTester:
    """End-to-end functionality testing for YouTube Comment Reader API."""
    
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url.rstrip('/')
        self.test_results: List[Dict[str, Any]] = []
        self.passed = 0
        self.failed = 0
        
    def log_test(self, test_name: str, passed: bool, message: str, details: Dict = None):
        """Log test result."""
        result = {
            'test': test_name,
            'passed': passed,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        self.test_results.append(result)
        
        if passed:
            self.passed += 1
            print(f"  ✅ PASS: {test_name}")
            print(f"     {message}")
        else:
            self.failed += 1
            print(f"  ❌ FAIL: {test_name}")
            print(f"     {message}")
        
        if details:
            for key, value in details.items():
                print(f"     • {key}: {value}")
        print()
    
    def test_search_videos(self) -> Tuple[bool, str]:
        """Test 1: Search for videos."""
        print("\n📝 Test 1: Search Videos")
        print("   Testing video search functionality...")
        
        try:
            response = requests.get(
                f"{self.api_base_url}/prod/search",
                params={
                    'q': 'python tutorial',
                    'part': 'snippet',
                    'type': 'video',
                    'maxResults': 5
                },
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_test(
                    "Search Videos",
                    False,
                    f"API returned status {response.status_code}",
                    {'response': response.text[:200]}
                )
                return False, None
            
            data = response.json()
            items = data.get('items', [])
            
            if len(items) == 0:
                self.log_test(
                    "Search Videos",
                    False,
                    "No videos found in search results",
                    {'response_keys': list(data.keys())}
                )
                return False, None
            
            # Get first video ID for subsequent tests
            video_id = items[0]['id'].get('videoId') if isinstance(items[0]['id'], dict) else items[0]['id']
            video_title = items[0]['snippet']['title']
            
            self.log_test(
                "Search Videos",
                True,
                f"Successfully found {len(items)} videos",
                {
                    'video_count': len(items),
                    'first_video_id': video_id,
                    'first_video_title': video_title
                }
            )
            
            return True, video_id
            
        except Exception as e:
            self.log_test(
                "Search Videos",
                False,
                f"Exception occurred: {str(e)}"
            )
            return False, None
    
    def test_fetch_comments_no_sentiment(self, video_id: str) -> Tuple[bool, int]:
        """Test 2: Fetch comments without sentiment analysis."""
        print("\n📝 Test 2: Fetch Comments (No Sentiment)")
        print("   Testing basic comment fetching...")
        
        try:
            response = requests.get(
                f"{self.api_base_url}/prod/video/comments",
                params={
                    'videoId': video_id,
                    'part': 'snippet',
                    'maxResults': 50
                },
                timeout=30
            )
            
            if response.status_code == 403:
                self.log_test(
                    "Fetch Comments (No Sentiment)",
                    False,
                    "Comments are disabled for this video or quota exceeded",
                    {'status': 403}
                )
                return False, 0
            
            if response.status_code != 200:
                self.log_test(
                    "Fetch Comments (No Sentiment)",
                    False,
                    f"API returned status {response.status_code}",
                    {'response': response.text[:200]}
                )
                return False, 0
            
            data = response.json()
            items = data.get('items', [])
            
            # Verify NO sentiment information
            has_sentiment = any('sentiment' in item for item in items)
            
            if has_sentiment:
                self.log_test(
                    "Fetch Comments (No Sentiment)",
                    False,
                    "Sentiment information found when it shouldn't be present"
                )
                return False, len(items)
            
            self.log_test(
                "Fetch Comments (No Sentiment)",
                True,
                f"Successfully fetched {len(items)} comments without sentiment",
                {
                    'comment_count': len(items),
                    'has_sentiment': False,
                    'sample_comment': items[0]['snippet']['topLevelComment']['snippet']['textDisplay'][:50] if items else 'N/A'
                }
            )
            
            return True, len(items)
            
        except Exception as e:
            self.log_test(
                "Fetch Comments (No Sentiment)",
                False,
                f"Exception occurred: {str(e)}"
            )
            return False, 0
    
    def test_fetch_comments_with_sentiment(self, video_id: str) -> Tuple[bool, List]:
        """Test 3: Fetch comments WITH sentiment analysis."""
        print("\n📝 Test 3: Fetch Comments (With Sentiment)")
        print("   Testing sentiment analysis integration...")
        
        try:
            response = requests.get(
                f"{self.api_base_url}/prod/video/comments",
                params={
                    'videoId': video_id,
                    'part': 'snippet',
                    'maxResults': 50,
                    'showPositives': 'true',
                    'showNegatives': 'true',
                    'showNeutral': 'true'
                },
                timeout=60
            )
            
            if response.status_code != 200:
                self.log_test(
                    "Fetch Comments (With Sentiment)",
                    False,
                    f"API returned status {response.status_code}",
                    {'response': response.text[:200]}
                )
                return False, []
            
            data = response.json()
            items = data.get('items', [])
            
            # Verify sentiment information is present
            items_with_sentiment = [item for item in items if 'sentiment' in item]
            
            if len(items_with_sentiment) == 0:
                self.log_test(
                    "Fetch Comments (With Sentiment)",
                    False,
                    "No sentiment information found in response"
                )
                return False, []
            
            # Count sentiments
            sentiments = {}
            for item in items_with_sentiment:
                sent = item.get('sentiment', 'UNKNOWN')
                sentiments[sent] = sentiments.get(sent, 0) + 1
            
            # Verify all valid sentiments
            valid_sentiments = {'POSITIVE', 'NEGATIVE', 'NEUTRAL'}
            invalid_sentiments = set(sentiments.keys()) - valid_sentiments
            
            if invalid_sentiments:
                self.log_test(
                    "Fetch Comments (With Sentiment)",
                    False,
                    f"Invalid sentiment values found: {invalid_sentiments}"
                )
                return False, items_with_sentiment
            
            self.log_test(
                "Fetch Comments (With Sentiment)",
                True,
                f"Successfully analyzed {len(items_with_sentiment)} comments",
                {
                    'total_comments': len(items),
                    'with_sentiment': len(items_with_sentiment),
                    'positive': sentiments.get('POSITIVE', 0),
                    'negative': sentiments.get('NEGATIVE', 0),
                    'neutral': sentiments.get('NEUTRAL', 0)
                }
            )
            
            return True, items_with_sentiment
            
        except Exception as e:
            self.log_test(
                "Fetch Comments (With Sentiment)",
                False,
                f"Exception occurred: {str(e)}"
            )
            return False, []
    
    def test_filter_positive(self, video_id: str) -> bool:
        """Test 4: Filter positive comments only."""
        print("\n📝 Test 4: Filter Positive Comments")
        print("   Testing positive sentiment filtering...")
        
        try:
            response = requests.get(
                f"{self.api_base_url}/prod/video/comments",
                params={
                    'videoId': video_id,
                    'part': 'snippet',
                    'maxResults': 50,
                    'showPositives': 'true'
                },
                timeout=60
            )
            
            if response.status_code != 200:
                self.log_test(
                    "Filter Positive Comments",
                    False,
                    f"API returned status {response.status_code}"
                )
                return False
            
            data = response.json()
            items = data.get('items', [])
            
            if len(items) == 0:
                self.log_test(
                    "Filter Positive Comments",
                    True,
                    "No positive comments found (valid result)",
                    {'comment_count': 0}
                )
                return True
            
            # Verify ALL are positive
            non_positive = [item for item in items if item.get('sentiment') != 'POSITIVE']
            
            if non_positive:
                self.log_test(
                    "Filter Positive Comments",
                    False,
                    f"Found {len(non_positive)} non-positive comments in filtered results",
                    {
                        'total': len(items),
                        'non_positive': len(non_positive),
                        'sentiments': [item.get('sentiment') for item in non_positive[:3]]
                    }
                )
                return False
            
            self.log_test(
                "Filter Positive Comments",
                True,
                f"All {len(items)} filtered comments are POSITIVE",
                {
                    'comment_count': len(items),
                    'all_positive': True
                }
            )
            
            return True
            
        except Exception as e:
            self.log_test(
                "Filter Positive Comments",
                False,
                f"Exception occurred: {str(e)}"
            )
            return False
    
    def test_filter_negative(self, video_id: str) -> bool:
        """Test 5: Filter negative comments only."""
        print("\n📝 Test 5: Filter Negative Comments")
        print("   Testing negative sentiment filtering...")
        
        try:
            response = requests.get(
                f"{self.api_base_url}/prod/video/comments",
                params={
                    'videoId': video_id,
                    'part': 'snippet',
                    'maxResults': 50,
                    'showNegatives': 'true'
                },
                timeout=60
            )
            
            if response.status_code != 200:
                self.log_test(
                    "Filter Negative Comments",
                    False,
                    f"API returned status {response.status_code}"
                )
                return False
            
            data = response.json()
            items = data.get('items', [])
            
            if len(items) == 0:
                self.log_test(
                    "Filter Negative Comments",
                    True,
                    "No negative comments found (valid result)",
                    {'comment_count': 0}
                )
                return True
            
            # Verify ALL are negative
            non_negative = [item for item in items if item.get('sentiment') != 'NEGATIVE']
            
            if non_negative:
                self.log_test(
                    "Filter Negative Comments",
                    False,
                    f"Found {len(non_negative)} non-negative comments in filtered results"
                )
                return False
            
            self.log_test(
                "Filter Negative Comments",
                True,
                f"All {len(items)} filtered comments are NEGATIVE",
                {
                    'comment_count': len(items),
                    'all_negative': True
                }
            )
            
            return True
            
        except Exception as e:
            self.log_test(
                "Filter Negative Comments",
                False,
                f"Exception occurred: {str(e)}"
            )
            return False
    
    def test_filter_neutral(self, video_id: str) -> bool:
        """Test 6: Filter neutral comments only."""
        print("\n📝 Test 6: Filter Neutral Comments")
        print("   Testing neutral sentiment filtering...")
        
        try:
            response = requests.get(
                f"{self.api_base_url}/prod/video/comments",
                params={
                    'videoId': video_id,
                    'part': 'snippet',
                    'maxResults': 50,
                    'showNeutral': 'true'
                },
                timeout=60
            )
            
            if response.status_code != 200:
                self.log_test(
                    "Filter Neutral Comments",
                    False,
                    f"API returned status {response.status_code}"
                )
                return False
            
            data = response.json()
            items = data.get('items', [])
            
            if len(items) == 0:
                self.log_test(
                    "Filter Neutral Comments",
                    True,
                    "No neutral comments found (valid result)",
                    {'comment_count': 0}
                )
                return True
            
            # Verify ALL are neutral
            non_neutral = [item for item in items if item.get('sentiment') != 'NEUTRAL']
            
            if non_neutral:
                self.log_test(
                    "Filter Neutral Comments",
                    False,
                    f"Found {len(non_neutral)} non-neutral comments in filtered results"
                )
                return False
            
            self.log_test(
                "Filter Neutral Comments",
                True,
                f"All {len(items)} filtered comments are NEUTRAL",
                {
                    'comment_count': len(items),
                    'all_neutral': True
                }
            )
            
            return True
            
        except Exception as e:
            self.log_test(
                "Filter Neutral Comments",
                False,
                f"Exception occurred: {str(e)}"
            )
            return False
    
    def test_error_handling(self) -> bool:
        """Test 7: Error handling with invalid inputs."""
        print("\n📝 Test 7: Error Handling")
        print("   Testing error scenarios...")
        
        all_passed = True
        
        # Test with invalid video ID
        try:
            response = requests.get(
                f"{self.api_base_url}/prod/video/comments",
                params={
                    'videoId': 'INVALID_VIDEO_ID_12345',
                    'part': 'snippet',
                    'maxResults': 10
                },
                timeout=30
            )
            
            # Should either return empty or error status (both acceptable)
            if response.status_code in [200, 400, 404]:
                print(f"  ✅ Invalid video ID handled correctly (status: {response.status_code})")
            else:
                print(f"  ⚠️  Unexpected status for invalid video: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"  ⚠️  Exception with invalid video ID: {str(e)}")
            all_passed = False
        
        self.log_test(
            "Error Handling",
            all_passed,
            "Error scenarios handled appropriately" if all_passed else "Some error scenarios not handled"
        )
        
        return all_passed
    
    def run_all_tests(self, test_video_id: str = None) -> Dict[str, Any]:
        """Run all end-to-end functionality tests."""
        print("=" * 80)
        print("🧪 END-TO-END FUNCTIONALITY TESTING")
        print("=" * 80)
        print(f"API: {self.api_base_url}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Test 1: Search videos (or use provided video ID)
        if test_video_id:
            print(f"\n📝 Using provided video ID: {test_video_id}")
            video_id = test_video_id
        else:
            success, video_id = self.test_search_videos()
            if not success or not video_id:
                print("\n❌ Cannot continue without valid video ID")
                return self.generate_report()
        
        # Test 2: Fetch comments without sentiment
        self.test_fetch_comments_no_sentiment(video_id)
        
        # Test 3: Fetch comments with sentiment
        self.test_fetch_comments_with_sentiment(video_id)
        
        # Test 4-6: Filter by each sentiment
        self.test_filter_positive(video_id)
        self.test_filter_negative(video_id)
        self.test_filter_neutral(video_id)
        
        # Test 7: Error handling
        self.test_error_handling()
        
        # Generate report
        return self.generate_report()
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate final test report."""
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n✅ Passed: {self.passed}/{total}")
        print(f"❌ Failed: {self.failed}/{total}")
        print(f"📈 Success Rate: {success_rate:.1f}%\n")
        
        if self.failed == 0:
            print("🎉 ALL TESTS PASSED! System is fully functional.\n")
        else:
            print("⚠️  Some tests failed. Review details above.\n")
        
        print("=" * 80)
        
        return {
            'total_tests': total,
            'passed': self.passed,
            'failed': self.failed,
            'success_rate': success_rate,
            'results': self.test_results,
            'timestamp': datetime.now().isoformat()
        }


def main():
    """Main function to run E2E tests."""
    
    # Configuration
    API_BASE_URL = "https://5jthpuzp9f.execute-api.us-east-1.amazonaws.com"
    TEST_VIDEO_ID = "dQw4w9WgXcQ"  # Use known working video
    
    # Run tests
    tester = E2EFunctionalityTester(API_BASE_URL)
    report = tester.run_all_tests(TEST_VIDEO_ID)
    
    # Save report
    filename = f'e2e_test_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📄 Report saved to: {filename}\n")


if __name__ == "__main__":
    main()


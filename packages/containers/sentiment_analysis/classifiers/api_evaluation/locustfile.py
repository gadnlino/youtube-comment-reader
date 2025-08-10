# locust -f locustfile.py --headless -u 100 -r 10 --run-time 1m 
# --csv=sentiment_results --host 
# http://Youtub-Youtu-Ag5D8wxXtCke-1311583466.us-east-1.elb.amazonaws.com

import uuid
import time
from locust import HttpUser, task, between
import json
import pandas as pd

comments_file_path = './data/sampled_comments.csv'
send_video_title = False
API_KEY = ('65e55fd8-4e1c-4e72-bb4f-67d5bdaececa1e9ec107-a3e1-4584-9b11-'
           '3651763c2cb32a669fa2-beb0-4df7-a3be-777912f6513972514d39-bd88-'
           '469d-810b-f0f188d5dd18c44a960d-922c-4160-ad73-65ae78faa2e8fbb'
           '456b7-8e00-44ce-8844-396bd49e533c417a6cd3-f7b0-4c09-9890-2a1db'
           '6f6e1745237f80e-fef7-4502-a431-20b336fc1ab1')
BATCH_SIZE = 20
MAX_RETRIES = 2

df = pd.read_csv(comments_file_path)


class SentimentUser(HttpUser):
    wait_time = between(2, 5)  # Increased wait time to reduce load

    @task
    def analyze_sentiment(self):
        for attempt in range(MAX_RETRIES + 1):
            try:
                # Sample comments from the dataframe
                sampled_df = df.sample(n=BATCH_SIZE).reset_index(drop=True)
                
                comments_formatted = []
                for index, row in sampled_df.iterrows():
                    if (isinstance(row['CommentText'], str) and
                            not pd.isna(row['CommentText']) and
                            row['CommentText'].strip() != ""):
                        
                        video_title = None
                        if ('VideoTitle' in row and
                                not pd.isna(row['VideoTitle']) and
                                send_video_title):
                            video_title = row['VideoTitle']
                        
                        comments_formatted.append({
                            "text": row['CommentText'],
                            "videoTitle": video_title,
                            "id": str(uuid.uuid4()),
                        })
                
                if not comments_formatted:
                    print("No valid comments to analyze.")
                    return
                
                payload = {
                    "comments": comments_formatted,
                    "model_name": "cardiffnlp/twitter-xlm-roberta-base-sentiment"
                }
                
                headers = {
                    'Content-Type': 'application/json',
                    'x-api-key': API_KEY
                }
                
                # Make POST request to the API endpoint with increased timeout
                response = self.client.post(
                    "/analyze",
                    data=json.dumps(payload),
                    headers=headers,
                    timeout=120,  # Increased timeout to 2 minutes
                    name="Analyze Sentiment"
                )
                
                # Check if the request was successful
                if response.status_code == 200:
                    print(f"Request successful on attempt {attempt + 1}")
                    break
                elif (response.status_code == 408 or 
                      response.status_code == 504):
                    # Timeout or gateway timeout - retry
                    if attempt < MAX_RETRIES:
                        print(f"Timeout on attempt {attempt + 1}, retrying...")
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    else:
                        print(f"Request failed after {MAX_RETRIES + 1} attempts")
                        break
                else:
                    print(f"Request failed with status code: "
                          f"{response.status_code}")
                    print(f"Response: {response.text}")
                    break
                    
            except Exception as e:
                if "timeout" in str(e).lower() and attempt < MAX_RETRIES:
                    print(f"Timeout exception on attempt {attempt + 1}, "
                          f"retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    print(f"Error in analyze_sentiment task: {str(e)}")
                    # Re-raise to ensure Locust records the failure
                    raise

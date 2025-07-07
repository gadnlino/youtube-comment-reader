#locust -f locustfile.py --headless -u 100 -r 10 --run-time 1m --csv=sentiment_results --host http://Youtub-Youtu-Ag5D8wxXtCke-1311583466.us-east-1.elb.amazonaws.com

import uuid
from locust import HttpUser, task, between
import json
import pandas as pd

comments_file_path = './data/sampled_comments.csv'
send_video_title = False
API_KEY = '299daa21-b1a2-41a5-b3c2-cbc2bc1f7773497f9a35-3ef5-4be8-9fb7-214427d62c86aded2757-2edf-406b-9008-bc8a0e948efa96ab682b-72a1-4eac-9531-536e075d9f3098559383-82bc-4181-b6c3-6c2c81d75d4c78f26092-b064-423b-9279-6d2815478eee'
BATCH_SIZE = 100

df = pd.read_csv(comments_file_path)


class SentimentUser(HttpUser):
    wait_time = between(1, 2)  # Tempo entre requisições por usuário (simula uso real)

    @task
    def analyze_sentiment(self):
        comments_formatted = [
            {
                "text": row['CommentText'],
                "videoTitle": row['VideoTitle'] if 'VideoTitle' in row and not pd.isna(row['VideoTitle']) and send_video_title else None,
                "id": str(uuid.uuid4()),
            }
            for index, row in df.sample(n=BATCH_SIZE).reset_index(drop=True).iterrows()
        ]
        
        payload = dict(
            comments=comments_formatted,
            model_name="cardiffnlp/twitter-xlm-roberta-base-sentiment"
        )
        headers = {'Content-Type': 'application/json', 'x-api-key': API_KEY}
        
        # Faz requisição POST para o endpoint da sua API
        self.client.post(f"{self.host}/analyze", data=json.dumps(payload), headers=headers)

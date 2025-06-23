#locust -f locustfile.py --headless -u 100 -r 10 --run-time 1m --csv=sentiment_results --host http://localhost:8000

import uuid
from locust import HttpUser, task, between
import json
import pandas as pd

comments_file_path = './sampled_comments.csv'
send_video_title = False
API_KEY = ''

df = pd.read_csv(comments_file_path)

df = df.sample(n=100).reset_index(drop=True)



comments_formatted = [
    {
        "text": row['CommentText'],
        "videoTitle": row['VideoTitle'] if 'VideoTitle' in row and not pd.isna(row['VideoTitle']) and send_video_title else None,
        "id": str(uuid.uuid4()),
    }
    for index, row in df.iterrows()
]

class SentimentUser(HttpUser):
    wait_time = between(1, 2)  # Tempo entre requisições por usuário (simula uso real)

    @task
    def analyze_sentiment(self):
        # Escolhe um comentário aleatório
        payload = dict(
            comments=comments_formatted,
            model="cardiffnlp/twitter-xlm-roberta-base-sentiment"
        )
        headers = {'Content-Type': 'application/json', 'x-api-key': API_KEY}
        
        # Faz requisição POST para o endpoint da sua API
        self.client.post("/analyze", data=json.dumps(payload), headers=headers)

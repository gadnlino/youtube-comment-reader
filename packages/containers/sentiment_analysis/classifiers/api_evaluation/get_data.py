
import kagglehub
import pandas as pd

N_SAMPLES=2500

path = kagglehub.dataset_download("amaanpoonawala/youtube-comments-sentiment-dataset")

file_path = f'{path}/youtube_comments_cleaned.csv'
destination_path = './sampled_comments.csv'

df = pd.read_csv(file_path)

# Clean nulls
df = df.dropna(subset=['VideoTitle', 'CommentText', 'Sentiment'])

def build_text_with_context(row):
    return f"Video Title: {row['VideoTitle']}. Comment: {row['CommentText']}"

df['CommentTextWithContext'] = df.apply(build_text_with_context, axis=1)

used_df = df.sample(n=N_SAMPLES).reset_index(drop=True)

used_df.to_csv(destination_path, index=False)


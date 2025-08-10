#!/usr/bin/env python3
"""
Quick Test: SVM + TF-IDF Sentiment Analysis

This script performs a quick test of SVM + TF-IDF
on a smaller sample of the YouTube comments dataset.
"""

import pandas as pd
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    f1_score
)
from sklearn.preprocessing import LabelEncoder
import kagglehub


def load_sample_dataset(sample_size=1000):
    """Load and sample the dataset"""
    print(f"📊 Loading dataset and sampling {sample_size:,} comments...")
    
    # Download dataset using kagglehub
    path = kagglehub.dataset_download(
        "amaanpoonawala/youtube-comments-sentiment-dataset"
    )
    file_path = f'{path}/youtube_comments_cleaned.csv'
    
    # Load and sample the dataset
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['VideoTitle', 'CommentText', 'Sentiment'])
    df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
    
    print(f"✅ Dataset loaded! Shape: {df.shape}")
    print("📈 Sentiment distribution:")
    print(df['Sentiment'].value_counts())
    
    return df


def preprocess_text(texts):
    """Basic text preprocessing"""
    processed_texts = []
    for text in texts:
        if isinstance(text, str):
            cleaned = text.lower().strip()
            cleaned = ' '.join(cleaned.split())
            processed_texts.append(cleaned)
        else:
            processed_texts.append("")
    return processed_texts


def main():
    """Main function"""
    print("🎯 Quick Test: SVM + TF-IDF")
    print("="*50)
    
    # Load dataset
    df = load_sample_dataset(sample_size=1000)
    
    # Preprocess text
    comments = preprocess_text(df['CommentText'].tolist())
    
    # Encode labels
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(df['Sentiment'])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        comments, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    print(f"\n📊 Data split:")
    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Create TF-IDF features
    print(f"\n🔤 Creating TF-IDF features...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words='english',
        min_df=2,
        max_df=0.95
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"✅ TF-IDF features created!")
    print(f"Training features shape: {X_train_tfidf.shape}")
    
    # Train model
    print(f"\n🤖 Training SVM model...")
    start_time = time.time()
    
    model = SVC(
        C=1.0,
        kernel='rbf',
        gamma='scale',
        random_state=42,
        probability=True
    )
    model.fit(X_train_tfidf, y_train)
    
    training_time = time.time() - start_time
    
    # Evaluate model
    print(f"📊 Evaluating model...")
    y_pred = model.predict(X_test_tfidf)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    cm = confusion_matrix(y_test, y_pred)
    
    # Display results
    print(f"\n📊 Quick Test Results:")
    print(f"Processing Time: {training_time:.2f} seconds")
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"F1 Score (Macro): {f1_macro:.4f}")
    
    # Display confusion matrix
    print(f"\n🔢 Confusion Matrix:")
    print("                Predicted")
    print("              Neg  Neu  Pos")
    print("Actual Neg    {:3d} {:3d} {:3d}".format(cm[0, 0], cm[0, 1], cm[0, 2]))
    print("      Neu     {:3d} {:3d} {:3d}".format(cm[1, 0], cm[1, 1], cm[1, 2]))
    print("      Pos     {:3d} {:3d} {:3d}".format(cm[2, 0], cm[2, 1], cm[2, 2]))
    
    print(f"\n🎉 Quick test completed!")
    print(f"📈 Model achieved {accuracy*100:.2f}% accuracy")


if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Quick TextBlob Sentiment Analysis Test

This script runs TextBlob sentiment analysis on a smaller sample of the dataset
for quick testing and comparison with VADER results.
"""

import pandas as pd
from textblob import TextBlob
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    accuracy_score, 
    f1_score
)
import kagglehub
import time


def load_and_sample_dataset(sample_size=1000):
    """Load dataset and sample it"""
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


def predict_with_textblob(comments):
    """Predict sentiment using TextBlob"""
    results = []
    
    print("🔍 Analyzing sentiments with TextBlob...")
    
    for i, comment in enumerate(comments):
        if i % 100 == 0:
            print(f"   Processed {i}/{len(comments)} comments...")
            
        # Create TextBlob object
        blob = TextBlob(comment)
        
        # Get polarity score (-1 to 1)
        polarity = blob.sentiment.polarity
        
        # Determine sentiment label based on polarity score
        if polarity > 0.1:
            label = "positive"
        elif polarity < -0.1:
            label = "negative"
        else:
            label = "neutral"
            
        results.append(label)
    
    print(f"✅ Completed analysis of {len(comments)} comments")
    return results


def calculate_and_display_metrics(y_true, y_pred):
    """Calculate and display classification metrics"""
    print("\n📊 Classification Results:")
    print("="*50)
    
    # Convert to lowercase for consistency
    y_true = [str(label).lower() for label in y_true]
    y_pred = [str(label).lower() for label in y_pred]
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    f1_macro = f1_score(y_true, y_pred, average='macro')
    f1_weighted = f1_score(y_true, y_pred, average='weighted')
    
    # Create confusion matrix
    cm = confusion_matrix(y_true, y_pred, 
                         labels=['negative', 'neutral', 'positive'])
    
    # Display results
    print(f"📈 Overall Metrics:")
    print(f"   Accuracy:  {accuracy:.4f}")
    print(f"   F1 (Macro): {f1_macro:.4f}")
    print(f"   F1 (Weighted): {f1_weighted:.4f}")
    
    print(f"\n🔢 Confusion Matrix:")
    print("                Predicted")
    print("              Neg  Neu  Pos")
    print("Actual Neg    {:3d} {:3d} {:3d}".format(cm[0, 0], cm[0, 1], cm[0, 2]))
    print("      Neu     {:3d} {:3d} {:3d}".format(cm[1, 0], cm[1, 1], cm[1, 2]))
    print("      Pos     {:3d} {:3d} {:3d}".format(cm[2, 0], cm[2, 1], cm[2, 2]))
    
    print(f"\n📋 Detailed Classification Report:")
    print(classification_report(y_true, y_pred, 
                              target_names=['negative', 'neutral', 'positive']))
    
    return {
        'accuracy': accuracy,
        'f1_macro': f1_macro,
        'f1_weighted': f1_weighted,
        'confusion_matrix': cm
    }


def main():
    """Main function"""
    print("🎯 Quick TextBlob Sentiment Analysis Test")
    print("="*50)
    
    # Load and sample dataset
    df = load_and_sample_dataset(sample_size=1000)
    
    # Prepare data
    comments = df['CommentText'].tolist()
    true_labels = df['Sentiment'].tolist()
    
    # Predict with TextBlob
    start_time = time.time()
    predicted_labels = predict_with_textblob(comments)
    end_time = time.time()
    
    # Calculate processing time
    processing_time = end_time - start_time
    avg_time_per_comment = processing_time / len(comments)
    
    print(f"\n⏱️  Processing Time:")
    print(f"   Total time: {processing_time:.2f} seconds")
    print(f"   Average per comment: {avg_time_per_comment:.4f} seconds")
    
    # Calculate and display metrics
    metrics = calculate_and_display_metrics(true_labels, predicted_labels)
    
    print(f"\n🎉 Quick test completed!")
    print(f"📊 Summary: Accuracy={metrics['accuracy']:.3f}, "
          f"F1-Macro={metrics['f1_macro']:.3f}")


if __name__ == "__main__":
    main() 
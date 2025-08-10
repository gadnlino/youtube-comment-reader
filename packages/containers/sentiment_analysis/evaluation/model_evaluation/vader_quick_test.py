#!/usr/bin/env python3
"""
Quick VADER Sentiment Analysis Test

This script runs VADER sentiment analysis on a smaller sample of the dataset
for quick testing and comparison with the Jupyter notebook results.
"""

import ssl
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    accuracy_score, 
    f1_score
)
import kagglehub
import time


def fix_nltk_ssl():
    """Fix SSL certificate issues for NLTK downloads"""
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context


def download_vader_lexicon():
    """Download VADER lexicon with error handling"""
    try:
        nltk.download('vader_lexicon', quiet=True)
        print("✅ VADER lexicon downloaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error downloading VADER lexicon: {e}")
        return False


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


def predict_with_vader(comments):
    """Predict sentiment using VADER"""
    analyzer = SentimentIntensityAnalyzer()
    results = []
    
    print("🔍 Analyzing sentiments with VADER...")
    
    for i, comment in enumerate(comments):
        if i % 100 == 0:
            print(f"   Processed {i}/{len(comments)} comments...")
            
        scores = analyzer.polarity_scores(comment)
        compound_score = scores['compound']
        
        # Determine sentiment label based on compound score
        if compound_score >= 0.05:
            label = "positive"
        elif compound_score <= -0.05:
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
    print("🎯 Quick VADER Sentiment Analysis Test")
    print("="*50)
    
    # Setup NLTK
    fix_nltk_ssl()
    if not download_vader_lexicon():
        print("⚠️  VADER lexicon download failed. Trying to continue...")
    
    # Load and sample dataset
    df = load_and_sample_dataset(sample_size=1000)
    
    # Prepare data
    comments = df['CommentText'].tolist()
    true_labels = df['Sentiment'].tolist()
    
    # Predict with VADER
    start_time = time.time()
    predicted_labels = predict_with_vader(comments)
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
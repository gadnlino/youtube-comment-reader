#!/usr/bin/env python3
"""
Sentiment Analysis Model Comparison Script

This script compares the performance of VADER and TextBlob sentiment analysis
models on the YouTube comments dataset.
"""

import pandas as pd
import time
from textblob import TextBlob
import ssl
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    accuracy_score, 
    f1_score
)
import kagglehub


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
        return True
    except Exception as e:
        print(f"❌ Error downloading VADER lexicon: {e}")
        return False


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
    
    print(f"✅ Completed VADER analysis of {len(comments)} comments")
    return results


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
    
    print(f"✅ Completed TextBlob analysis of {len(comments)} comments")
    return results


def calculate_metrics(y_true, y_pred, model_name):
    """Calculate classification metrics"""
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
    
    return {
        'model': model_name,
        'accuracy': accuracy,
        'f1_macro': f1_macro,
        'f1_weighted': f1_weighted,
        'confusion_matrix': cm
    }


def display_comparison_results(vader_metrics, textblob_metrics):
    """Display comparison results"""
    print("\n" + "="*80)
    print("SENTIMENT ANALYSIS MODEL COMPARISON")
    print("="*80)
    
    # Create comparison table
    comparison_data = [
        {
            'Model': 'VADER',
            'Accuracy': f"{vader_metrics['accuracy']:.4f}",
            'F1 (Macro)': f"{vader_metrics['f1_macro']:.4f}",
            'F1 (Weighted)': f"{vader_metrics['f1_weighted']:.4f}"
        },
        {
            'Model': 'TextBlob',
            'Accuracy': f"{textblob_metrics['accuracy']:.4f}",
            'F1 (Macro)': f"{textblob_metrics['f1_macro']:.4f}",
            'F1 (Weighted)': f"{textblob_metrics['f1_weighted']:.4f}"
        }
    ]
    
    df_comparison = pd.DataFrame(comparison_data)
    print("\n📊 Performance Comparison:")
    print(df_comparison.to_string(index=False))
    
    # Determine winner
    vader_better = vader_metrics['accuracy'] > textblob_metrics['accuracy']
    winner = "VADER" if vader_better else "TextBlob"
    accuracy_diff = abs(vader_metrics['accuracy'] - textblob_metrics['accuracy'])
    
    print(f"\n🏆 Winner: {winner}")
    print(f"📈 Accuracy difference: {accuracy_diff:.4f}")
    
    # Detailed metrics
    print(f"\n📋 Detailed Metrics:")
    print(f"VADER - Accuracy: {vader_metrics['accuracy']:.4f}, F1-Macro: {vader_metrics['f1_macro']:.4f}")
    print(f"TextBlob - Accuracy: {textblob_metrics['accuracy']:.4f}, F1-Macro: {textblob_metrics['f1_macro']:.4f}")
    
    # Confusion matrices
    print(f"\n🔢 VADER Confusion Matrix:")
    cm_vader = vader_metrics['confusion_matrix']
    print("                Predicted")
    print("              Neg  Neu  Pos")
    print("Actual Neg    {:3d} {:3d} {:3d}".format(cm_vader[0, 0], cm_vader[0, 1], cm_vader[0, 2]))
    print("      Neu     {:3d} {:3d} {:3d}".format(cm_vader[1, 0], cm_vader[1, 1], cm_vader[1, 2]))
    print("      Pos     {:3d} {:3d} {:3d}".format(cm_vader[2, 0], cm_vader[2, 1], cm_vader[2, 2]))
    
    print(f"\n🔢 TextBlob Confusion Matrix:")
    cm_textblob = textblob_metrics['confusion_matrix']
    print("                Predicted")
    print("              Neg  Neu  Pos")
    print("Actual Neg    {:3d} {:3d} {:3d}".format(cm_textblob[0, 0], cm_textblob[0, 1], cm_textblob[0, 2]))
    print("      Neu     {:3d} {:3d} {:3d}".format(cm_textblob[1, 0], cm_textblob[1, 1], cm_textblob[1, 2]))
    print("      Pos     {:3d} {:3d} {:3d}".format(cm_textblob[2, 0], cm_textblob[2, 1], cm_textblob[2, 2]))


def main():
    """Main function"""
    print("🎯 Sentiment Analysis Model Comparison")
    print("="*50)
    
    # Setup NLTK
    fix_nltk_ssl()
    if not download_vader_lexicon():
        print("⚠️  VADER lexicon download failed. Trying to continue...")
    
    # Load dataset
    df = load_sample_dataset(sample_size=1000)
    
    # Prepare data
    comments = df['CommentText'].tolist()
    true_labels = df['Sentiment'].tolist()
    
    # Run VADER analysis
    print(f"\n🚀 Running VADER analysis...")
    start_time = time.time()
    vader_predictions = predict_with_vader(comments)
    vader_time = time.time() - start_time
    
    # Run TextBlob analysis
    print(f"\n🚀 Running TextBlob analysis...")
    start_time = time.time()
    textblob_predictions = predict_with_textblob(comments)
    textblob_time = time.time() - start_time
    
    # Calculate metrics
    vader_metrics = calculate_metrics(true_labels, vader_predictions, "VADER")
    textblob_metrics = calculate_metrics(true_labels, textblob_predictions, "TextBlob")
    
    # Add timing to metrics
    vader_metrics['processing_time'] = vader_time
    textblob_metrics['processing_time'] = textblob_time
    
    # Display results
    display_comparison_results(vader_metrics, textblob_metrics)
    
    # Timing comparison
    print(f"\n⏱️  Processing Time Comparison:")
    print(f"VADER: {vader_time:.2f} seconds ({vader_time/len(comments):.4f}s per comment)")
    print(f"TextBlob: {textblob_time:.2f} seconds ({textblob_time/len(comments):.4f}s per comment)")
    
    # Save results
    results = {
        'vader': vader_metrics,
        'textblob': textblob_metrics
    }
    
    with open('model_comparison_results.txt', 'w') as f:
        f.write("Sentiment Analysis Model Comparison Results\n")
        f.write("="*50 + "\n\n")
        f.write(f"VADER - Accuracy: {vader_metrics['accuracy']:.4f}, F1-Macro: {vader_metrics['f1_macro']:.4f}\n")
        f.write(f"TextBlob - Accuracy: {textblob_metrics['accuracy']:.4f}, F1-Macro: {textblob_metrics['f1_macro']:.4f}\n")
        f.write(f"VADER Time: {vader_time:.2f}s\n")
        f.write(f"TextBlob Time: {textblob_time:.2f}s\n")
    
    print(f"\n✅ Results saved to model_comparison_results.txt")
    print(f"\n🎉 Comparison completed!")


if __name__ == "__main__":
    main() 
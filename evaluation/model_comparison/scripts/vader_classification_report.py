#!/usr/bin/env python3
"""
VADER Sentiment Analysis Classification Report Script

This script loads the same YouTube comments dataset used in the Jupyter 
notebook and calculates classification metrics using VADER sentiment analysis.
"""

import ssl
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    accuracy_score, 
    f1_score,
    precision_recall_fscore_support
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
        print("The lexicon may already be downloaded.")
        return False


def load_dataset():
    """Load the YouTube comments dataset"""
    print("📊 Loading YouTube comments dataset...")
    
    # Download dataset using kagglehub
    path = kagglehub.dataset_download(
        "amaanpoonawala/youtube-comments-sentiment-dataset"
    )
    file_path = f'{path}/youtube_comments_cleaned.csv'
    
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Clean nulls
    df = df.dropna(subset=['VideoTitle', 'CommentText', 'Sentiment'])
    
    print(f"✅ Dataset loaded successfully! Shape: {df.shape}")
    print("📈 Sentiment distribution:")
    print(df['Sentiment'].value_counts())
    
    return df


def predict_with_vader_classifier(comments):
    """Predict sentiment using VADER classifier"""
    analyzer = SentimentIntensityAnalyzer()
    results = []
    
    print("🔍 Analyzing sentiments with VADER...")
    
    for i, comment in enumerate(comments):
        if i % 1000 == 0:
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


def calculate_metrics(y_true, y_pred, sample_size=None):
    """Calculate comprehensive classification metrics"""
    print("\n📊 Calculating classification metrics...")
    
    # Convert to lowercase for consistency
    y_true = [str(label).lower() for label in y_true]
    y_pred = [str(label).lower() for label in y_pred]
    
    # Calculate basic metrics
    accuracy = accuracy_score(y_true, y_pred)
    f1_macro = f1_score(y_true, y_pred, average='macro')
    f1_weighted = f1_score(y_true, y_pred, average='weighted')
    
    # Calculate per-class metrics
    precision, recall, f1_per_class, support = precision_recall_fscore_support(
        y_true, y_pred, average=None, labels=['negative', 'neutral', 'positive']
    )
    
    # Create confusion matrix
    cm = confusion_matrix(y_true, y_pred, 
                         labels=['negative', 'neutral', 'positive'])
    
    # Print results
    print(f"\n{'='*60}")
    print("VADER SENTIMENT ANALYSIS RESULTS")
    print(f"{'='*60}")
    
    if sample_size:
        print(f"Sample Size: {sample_size:,} comments")
    
    print(f"\n📈 Overall Metrics:")
    print(f"   Accuracy:  {accuracy:.4f}")
    print(f"   F1 (Macro): {f1_macro:.4f}")
    print(f"   F1 (Weighted): {f1_weighted:.4f}")
    
    print(f"\n📊 Per-Class Metrics:")
    classes = ['negative', 'neutral', 'positive']
    for i, class_name in enumerate(classes):
        print(f"   {class_name.capitalize()}:")
        print(f"     Precision: {precision[i]:.4f}")
        print(f"     Recall:    {recall[i]:.4f}")
        print(f"     F1-Score:  {f1_per_class[i]:.4f}")
        print(f"     Support:   {support[i]:.0f}")
    
    print(f"\n🔢 Confusion Matrix:")
    print("                Predicted")
    print("              Neg  Neu  Pos")
    print("Actual Neg    {:3d} {:3d} {:3d}".format(cm[0, 0], cm[0, 1], cm[0, 2]))
    print("      Neu     {:3d} {:3d} {:3d}".format(cm[1, 0], cm[1, 1], cm[1, 2]))
    print("      Pos     {:3d} {:3d} {:3d}".format(cm[2, 0], cm[2, 1], cm[2, 2]))
    
    print(f"\n📋 Detailed Classification Report:")
    print(classification_report(y_true, y_pred, target_names=classes))
    
    return {
        'accuracy': accuracy,
        'f1_macro': f1_macro,
        'f1_weighted': f1_weighted,
        'precision_per_class': precision,
        'recall_per_class': recall,
        'f1_per_class': f1_per_class,
        'support': support,
        'confusion_matrix': cm
    }


def run_vader_analysis(sample_size=None, random_state=42):
    """Run complete VADER sentiment analysis"""
    print("🚀 Starting VADER Sentiment Analysis")
    print("="*60)
    
    # Setup NLTK
    fix_nltk_ssl()
    if not download_vader_lexicon():
        print("⚠️  VADER lexicon download failed. Trying to continue...")
    
    # Load dataset
    df = load_dataset()
    
    # Sample data if specified
    if sample_size:
        print(f"\n📊 Sampling {sample_size:,} comments...")
        df = df.sample(n=sample_size, random_state=random_state).reset_index(drop=True)
    
    # Prepare data
    comments = df['CommentText'].tolist()
    true_labels = df['Sentiment'].tolist()
    
    # Predict with VADER
    start_time = time.time()
    predicted_labels = predict_with_vader_classifier(comments)
    end_time = time.time()
    
    # Calculate processing time
    processing_time = end_time - start_time
    avg_time_per_comment = processing_time / len(comments)
    
    print(f"\n⏱️  Processing Time:")
    print(f"   Total time: {processing_time:.2f} seconds")
    print(f"   Average per comment: {avg_time_per_comment:.4f} seconds")
    
    # Calculate metrics
    metrics = calculate_metrics(true_labels, predicted_labels, sample_size)
    
    # Add timing to metrics
    metrics['processing_time'] = processing_time
    metrics['avg_time_per_comment'] = avg_time_per_comment
    
    return metrics, df


def main():
    """Main function to run VADER analysis"""
    print("🎯 VADER Sentiment Analysis for YouTube Comments")
    print("="*60)
    
    # Run analysis with different sample sizes
    sample_sizes = [1000, 5000, 10000, None]  # None means full dataset
    
    for sample_size in sample_sizes:
        if sample_size is None:
            print(f"\n🔍 Running analysis on FULL DATASET...")
        else:
            print(f"\n🔍 Running analysis on {sample_size:,} samples...")
        
        try:
            metrics, df = run_vader_analysis(sample_size=sample_size)
            
            # Save results to file
            if sample_size:
                filename = f"vader_results_{sample_size}.txt"
            else:
                filename = "vader_results_full_dataset.txt"
            
            with open(filename, 'w') as f:
                f.write("VADER Sentiment Analysis Results\n")
                f.write(f"Sample Size: {sample_size if sample_size else 'Full Dataset'}\n")
                f.write(f"Processing Time: {metrics['processing_time']:.2f} seconds\n")
                f.write(f"Accuracy: {metrics['accuracy']:.4f}\n")
                f.write(f"F1 (Macro): {metrics['f1_macro']:.4f}\n")
                f.write(f"F1 (Weighted): {metrics['f1_weighted']:.4f}\n")
            
            print(f"✅ Results saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error running analysis: {e}")
            continue
    
    print(f"\n🎉 Analysis completed!")


if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
TextBlob Sentiment Analysis - Full Dataset

This script performs sentiment analysis using TextBlob on the full YouTube comments dataset.
"""

import pandas as pd
import time
from textblob import TextBlob
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
)
import kagglehub


def load_full_dataset():
    """Load the full dataset"""
    print("📊 Loading full YouTube comments dataset...")
    
    # Download dataset using kagglehub
    path = kagglehub.dataset_download(
        "amaanpoonawala/youtube-comments-sentiment-dataset"
    )
    file_path = f'{path}/youtube_comments_cleaned.csv'
    
    # Load the dataset
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['VideoTitle', 'CommentText', 'Sentiment'])
    
    print(f"✅ Dataset loaded! Shape: {df.shape}")
    print("📈 Sentiment distribution:")
    print(df['Sentiment'].value_counts())
    
    return df


def predict_with_textblob(comments):
    """Predict sentiment using TextBlob"""
    results = []
    
    print("🔍 Analyzing sentiments with TextBlob...")
    
    for i, comment in enumerate(comments):
        if i % 10000 == 0:
            print(f"   Processed {i:,}/{len(comments):,} comments...")
            
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
    
    print(f"✅ Completed analysis of {len(comments):,} comments")
    return results


def calculate_metrics(y_true, y_pred):
    """Calculate classification metrics"""
    # Convert to lowercase for consistency
    y_true = [str(label).lower() for label in y_true]
    y_pred = [str(label).lower() for label in y_pred]
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    f1_macro = f1_score(y_true, y_pred, average='macro')
    f1_weighted = f1_score(y_true, y_pred, average='weighted')
    precision_macro = precision_score(y_true, y_pred, average='macro')
    recall_macro = recall_score(y_true, y_pred, average='macro')
    
    # Create confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=['negative', 'neutral', 'positive'])
    
    # Get classification report
    report = classification_report(y_true, y_pred, output_dict=True)
    
    return {
        'accuracy': accuracy,
        'f1_macro': f1_macro,
        'f1_weighted': f1_weighted,
        'precision_macro': precision_macro,
        'recall_macro': recall_macro,
        'confusion_matrix': cm,
        'classification_report': report
    }


def display_results(results, processing_time, sample_size):
    """Display comprehensive results"""
    print("\n" + "="*80)
    print("TEXTBLOB SENTIMENT ANALYSIS RESULTS")
    print("="*80)
    
    print(f"\n📊 Performance Metrics:")
    print(f"Sample Size: {sample_size:,} comments")
    print(f"Processing Time: {processing_time:.2f} seconds")
    print(f"Speed: {processing_time/sample_size:.4f} seconds per comment")
    print(f"Accuracy: {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)")
    print(f"F1 Score (Macro): {results['f1_macro']:.4f}")
    print(f"F1 Score (Weighted): {results['f1_weighted']:.4f}")
    print(f"Precision (Macro): {results['precision_macro']:.4f}")
    print(f"Recall (Macro): {results['recall_macro']:.4f}")
    
    # Display confusion matrix
    cm = results['confusion_matrix']
    print(f"\n🔢 Confusion Matrix:")
    print("                Predicted")
    print("              Neg  Neu  Pos")
    print("Actual Neg    {:3d} {:3d} {:3d}".format(cm[0, 0], cm[0, 1], cm[0, 2]))
    print("      Neu     {:3d} {:3d} {:3d}".format(cm[1, 0], cm[1, 1], cm[1, 2]))
    print("      Pos     {:3d} {:3d} {:3d}".format(cm[2, 0], cm[2, 1], cm[2, 2]))
    
    # Display detailed classification report
    print(f"\n📋 Detailed Classification Report:")
    report = results['classification_report']
    for label in ['negative', 'neutral', 'positive']:
        if label in report:
            print(f"{label.capitalize()}:")
            print(f"  Precision: {report[label]['precision']:.4f}")
            print(f"  Recall: {report[label]['recall']:.4f}")
            print(f"  F1-Score: {report[label]['f1-score']:.4f}")
            print(f"  Support: {report[label]['support']}")


def save_results(results, processing_time, sample_size):
    """Save results to file"""
    print("\n💾 Saving results...")
    
    with open('textblob_results_full_dataset.txt', 'w') as f:
        f.write("TextBlob Sentiment Analysis Results - Full Dataset\n")
        f.write("="*60 + "\n\n")
        f.write(f"Sample Size: {sample_size:,} comments\n")
        f.write(f"Processing Time: {processing_time:.2f} seconds\n")
        f.write(f"Speed: {processing_time/sample_size:.4f} seconds per comment\n")
        f.write(f"Accuracy: {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)\n")
        f.write(f"F1 Score (Macro): {results['f1_macro']:.4f}\n")
        f.write(f"F1 Score (Weighted): {results['f1_weighted']:.4f}\n")
        f.write(f"Precision (Macro): {results['precision_macro']:.4f}\n")
        f.write(f"Recall (Macro): {results['recall_macro']:.4f}\n")
        
        # Save confusion matrix
        f.write(f"\nConfusion Matrix:\n")
        cm = results['confusion_matrix']
        f.write("                Predicted\n")
        f.write("              Neg  Neu  Pos\n")
        f.write("Actual Neg    {:3d} {:3d} {:3d}\n".format(cm[0, 0], cm[0, 1], cm[0, 2]))
        f.write("      Neu     {:3d} {:3d} {:3d}\n".format(cm[1, 0], cm[1, 1], cm[1, 2]))
        f.write("      Pos     {:3d} {:3d} {:3d}\n".format(cm[2, 0], cm[2, 1], cm[2, 2]))
        
        # Save detailed classification report
        f.write(f"\nDetailed Classification Report:\n")
        report = results['classification_report']
        for label in ['negative', 'neutral', 'positive']:
            if label in report:
                f.write(f"{label.capitalize()}:\n")
                f.write(f"  Precision: {report[label]['precision']:.4f}\n")
                f.write(f"  Recall: {report[label]['recall']:.4f}\n")
                f.write(f"  F1-Score: {report[label]['f1-score']:.4f}\n")
                f.write(f"  Support: {report[label]['support']}\n")
    
    print("✅ Results saved to textblob_results_full_dataset.txt")


def main():
    """Main function"""
    print("🎯 TextBlob Sentiment Analysis - Full Dataset")
    print("="*60)
    
    # Load dataset
    df = load_full_dataset()
    
    # Prepare data
    comments = df['CommentText'].tolist()
    true_labels = df['Sentiment'].tolist()
    
    # Run TextBlob analysis
    print(f"\n🚀 Running TextBlob analysis...")
    start_time = time.time()
    textblob_predictions = predict_with_textblob(comments)
    processing_time = time.time() - start_time
    
    # Calculate metrics
    results = calculate_metrics(true_labels, textblob_predictions)
    
    # Display results
    display_results(results, processing_time, len(comments))
    
    # Save results
    save_results(results, processing_time, len(comments))
    
    print(f"\n🎉 TextBlob analysis completed!")
    print(f"📈 Model achieved {results['accuracy']*100:.2f}% accuracy")


if __name__ == "__main__":
    main() 
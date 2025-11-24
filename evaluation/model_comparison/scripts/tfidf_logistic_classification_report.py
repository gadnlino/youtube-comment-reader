#!/usr/bin/env python3
"""
TF-IDF + Logistic Regression Sentiment Analysis

This script performs sentiment analysis using TF-IDF vectorization
combined with Logistic Regression classifier on the YouTube comments dataset.
"""

import pandas as pd
import numpy as np
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
)
from sklearn.preprocessing import LabelEncoder
import kagglehub
import pickle
import os


def load_dataset(sample_size=None):
    """Load and optionally sample the dataset"""
    print("📊 Loading YouTube comments dataset...")
    
    # Download dataset using kagglehub
    path = kagglehub.dataset_download(
        "amaanpoonawala/youtube-comments-sentiment-dataset"
    )
    file_path = f'{path}/youtube_comments_cleaned.csv'
    
    # Load the dataset
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['VideoTitle', 'CommentText', 'Sentiment'])
    
    if sample_size:
        print(f"📊 Sampling {sample_size:,} comments...")
        df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
    else:
        print(f"📊 Using full dataset...")
    
    print(f"✅ Dataset loaded! Shape: {df.shape}")
    print("📈 Sentiment distribution:")
    print(df['Sentiment'].value_counts())
    
    return df


def preprocess_text(texts):
    """Basic text preprocessing"""
    print("🧹 Preprocessing text data...")
    
    # Convert to lowercase and remove extra whitespace
    processed_texts = []
    for text in texts:
        if isinstance(text, str):
            # Basic cleaning
            cleaned = text.lower().strip()
            # Remove extra whitespace
            cleaned = ' '.join(cleaned.split())
            processed_texts.append(cleaned)
        else:
            processed_texts.append("")
    
    print(f"✅ Text preprocessing completed for {len(processed_texts)} comments")
    return processed_texts


def create_tfidf_vectorizer(max_features=10000, ngram_range=(1, 2)):
    """Create TF-IDF vectorizer with specified parameters"""
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        stop_words='english',
        min_df=2,
        max_df=0.95,
        lowercase=True,
        strip_accents='unicode'
    )
    return vectorizer


def train_logistic_regression_model(X_train, y_train, C=1.0, max_iter=1000):
    """Train Logistic Regression model"""
    print("🤖 Training Logistic Regression model...")
    
    model = LogisticRegression(
        C=C,
        max_iter=max_iter,
        random_state=42,
        n_jobs=-1,
        solver='lbfgs'
    )
    
    model.fit(X_train, y_train)
    print("✅ Model training completed!")
    
    return model


def evaluate_model(model, X_test, y_test, vectorizer, label_encoder):
    """Evaluate the trained model"""
    print("📊 Evaluating model performance...")
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    f1_weighted = f1_score(y_test, y_pred, average='weighted')
    precision_macro = precision_score(y_test, y_pred, average='macro')
    recall_macro = recall_score(y_test, y_pred, average='macro')
    
    # Create confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # Get classification report
    report = classification_report(y_test, y_pred, output_dict=True)
    
    results = {
        'accuracy': accuracy,
        'f1_macro': f1_macro,
        'f1_weighted': f1_weighted,
        'precision_macro': precision_macro,
        'recall_macro': recall_macro,
        'confusion_matrix': cm,
        'classification_report': report
    }
    
    return results, y_pred


def display_results(results, processing_time, sample_size):
    """Display comprehensive results"""
    print("\n" + "="*80)
    print("TF-IDF + LOGISTIC REGRESSION SENTIMENT ANALYSIS RESULTS")
    print("="*80)
    
    print(f"\n📊 Performance Metrics:")
    if sample_size is None:
        print(f"Sample Size: Full dataset")
        print(f"Processing Time: {processing_time:.2f} seconds")
        print(f"Speed: {processing_time/1032225:.4f} seconds per comment")
    else:
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


def save_results(results, processing_time, sample_size, model, vectorizer, label_encoder):
    """Save results and model to files"""
    print("\n💾 Saving results and model...")
    
    # Create results directory if it doesn't exist
    import os
    results_dir = '../results'
    os.makedirs(results_dir, exist_ok=True)
    
    # Save results to text file
    results_file = os.path.join(results_dir, 'tfidf_logistic_results.txt')
    with open(results_file, 'w') as f:
        f.write("TF-IDF + Logistic Regression Sentiment Analysis Results\n")
        f.write("="*60 + "\n\n")
        if sample_size is None:
            f.write(f"Sample Size: Full dataset\n")
            f.write(f"Processing Time: {processing_time:.2f} seconds\n")
            f.write(f"Speed: {processing_time/1032225:.4f} seconds per comment\n")
        else:
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
    
    # Save model and vectorizer
    model_data = {
        'model': model,
        'vectorizer': vectorizer,
        'label_encoder': label_encoder
    }
    
    model_file = os.path.join(results_dir, 'tfidf_logistic_model.pkl')
    with open(model_file, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"✅ Results saved to {results_file}")
    print(f"✅ Model saved to {model_file}")


def main():
    """Main function"""
    print("🎯 TF-IDF + Logistic Regression Sentiment Analysis")
    print("="*60)
    
    # Configuration
    sample_size = None  # Use full dataset
    test_size = 0.2
    random_state = 42
    
    # Load dataset
    df = load_dataset(sample_size=sample_size)
    
    # Preprocess text
    comments = preprocess_text(df['CommentText'].tolist())
    
    # Encode labels
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(df['Sentiment'])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        comments, labels, test_size=test_size, random_state=random_state, stratify=labels
    )
    
    print(f"\n📊 Data split:")
    print(f"Training set: {len(X_train):,} samples")
    print(f"Test set: {len(X_test):,} samples")
    
    # Create and fit TF-IDF vectorizer
    print(f"\n🔤 Creating TF-IDF features...")
    vectorizer = create_tfidf_vectorizer(max_features=10000, ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"✅ TF-IDF features created!")
    print(f"Training features shape: {X_train_tfidf.shape}")
    print(f"Test features shape: {X_test_tfidf.shape}")
    
    # Train model
    start_time = time.time()
    model = train_logistic_regression_model(X_train_tfidf, y_train, C=1.0, max_iter=1000)
    training_time = time.time() - start_time
    
    # Evaluate model
    results, y_pred = evaluate_model(model, X_test_tfidf, y_test, vectorizer, label_encoder)
    
    # Calculate total processing time
    total_time = training_time + (time.time() - start_time)
    
    # Display results
    display_results(results, total_time, sample_size)
    
    # Save results
    save_results(results, total_time, sample_size, model, vectorizer, label_encoder)
    
    print(f"\n🎉 TF-IDF + Logistic Regression analysis completed!")
    print(f"📈 Model achieved {results['accuracy']*100:.2f}% accuracy")


if __name__ == "__main__":
    main() 
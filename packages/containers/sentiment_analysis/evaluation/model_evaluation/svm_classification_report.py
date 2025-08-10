#!/usr/bin/env python3
"""
SVM + TF-IDF Sentiment Analysis

This script performs sentiment analysis using Support Vector Machine (SVM) 
with TF-IDF vectorization on YouTube comments dataset.
"""

import pandas as pd
import time
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
)
import kagglehub


def load_dataset(sample_size=None):
    """Load and optionally sample the dataset"""
    print("Loading YouTube comments dataset...")
    
    # Download dataset using kagglehub
    path = kagglehub.dataset_download(
        "amaanpoonawala/youtube-comments-sentiment-dataset"
    )
    file_path = f'{path}/youtube_comments_cleaned.csv'
    
    # Load the dataset
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['VideoTitle', 'CommentText', 'Sentiment'])
    
    if sample_size:
        print(f"Sampling {sample_size:,} comments...")
        df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
    else:
        print(f"Using full dataset...")
    
    print(f"Dataset loaded! Shape: {df.shape}")
    print("Sentiment distribution:")
    print(df['Sentiment'].value_counts())
    
    return df


def preprocess_text(texts):
    """Basic text preprocessing"""
    print("Preprocessing text data...")
    
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
    
    print(f"Text preprocessing completed for {len(processed_texts)} comments")
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


def train_svm_model(X_train, y_train, C=1.0, kernel='rbf', gamma='scale'):
    """Train SVM model"""
    print("Training SVM model...")
    
    model = SVC(
        C=C,
        kernel=kernel,
        gamma=gamma,
        random_state=42,
        probability=True
    )
    
    model.fit(X_train, y_train)
    print("Model training completed!")
    
    return model


def evaluate_model(model, X_test, y_test, vectorizer, label_encoder):
    """Evaluate the trained model"""
    print("Evaluating model performance...")
    
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
    print("SVM + TF-IDF SENTIMENT ANALYSIS RESULTS")
    print("="*80)
    
    print(f"\nPerformance Metrics:")
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
    print(f"\nConfusion Matrix:")
    print("                Predicted")
    print("              Neg  Neu  Pos")
    print("Actual Neg    {:3d} {:3d} {:3d}".format(cm[0, 0], cm[0, 1], cm[0, 2]))
    print("      Neu     {:3d} {:3d} {:3d}".format(cm[1, 0], cm[1, 1], cm[1, 2]))
    print("      Pos     {:3d} {:3d} {:3d}".format(cm[2, 0], cm[2, 1], cm[2, 2]))
    
    # Display detailed classification report
    print(f"\nDetailed Classification Report:")
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
    print("\nSaving results and model...")
    
    # Save results to text file
    with open('svm_results.txt', 'w') as f:
        f.write("SVM + TF-IDF Sentiment Analysis Results\n")
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
    
    with open('svm_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print("Results saved to svm_results.txt")
    print("Model saved to svm_model.pkl")


def main():
    """Main function"""
    print("SVM + TF-IDF Sentiment Analysis")
    print("="*60)
    
    # Configuration
    sample_size = 50000  # Use 50k samples for faster training
    test_size = 0.2
    random_state = 42
    
    # Load dataset
    df = load_dataset(sample_size=sample_size)
    
    # Prepare data
    comments = df['CommentText'].tolist()
    labels = df['Sentiment'].tolist()
    
    # Preprocess text
    processed_comments = preprocess_text(comments)
    
    # Encode labels
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        processed_comments, encoded_labels, 
        test_size=test_size, random_state=random_state, stratify=encoded_labels
    )
    
    print(f"\nData split:")
    print(f"Training set: {len(X_train):,} samples")
    print(f"Test set: {len(X_test):,} samples")
    
    # Create TF-IDF features
    print(f"\nCreating TF-IDF features...")
    vectorizer = create_tfidf_vectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"TF-IDF features created!")
    print(f"Training features shape: {X_train_tfidf.shape}")
    print(f"Test features shape: {X_test_tfidf.shape}")
    
    # Train SVM model
    start_time = time.time()
    svm_model = train_svm_model(X_train_tfidf, y_train)
    training_time = time.time() - start_time
    
    # Evaluate model
    results, predictions = evaluate_model(svm_model, X_test_tfidf, y_test, vectorizer, label_encoder)
    
    # Display results
    display_results(results, training_time, sample_size)
    
    # Save results
    save_results(results, training_time, sample_size, svm_model, vectorizer, label_encoder)
    
    print(f"\nSVM analysis completed!")
    print(f"Model achieved {results['accuracy']*100:.2f}% accuracy")


if __name__ == "__main__":
    main() 
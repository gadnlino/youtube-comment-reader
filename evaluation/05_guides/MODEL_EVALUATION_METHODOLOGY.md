# Sentiment Analysis Model Evaluation Methodology

**Document Purpose**: Comprehensive methodology for evaluating sentiment analysis models  
**Audience**: Academic/Technical Documentation  
**Date**: October 27, 2025  
**Version**: 1.0  

---

## 📋 Table of Contents

1. [Introduction](#1-introduction)
2. [Dataset](#2-dataset)
3. [Model Selection](#3-model-selection)
4. [Training Methodology](#4-training-methodology)
5. [Evaluation Metrics](#5-evaluation-metrics)
6. [Statistical Analysis](#6-statistical-analysis)
7. [Reproducibility](#7-reproducibility)
8. [Limitations](#8-limitations)

---

## 1. Introduction

### 1.1 Purpose

This document describes the methodology used to evaluate and compare sentiment analysis models for YouTube comment classification. The evaluation aims to:

- **Compare model accuracy** across different algorithms
- **Measure computational efficiency** (speed, memory)
- **Select optimal model** for production deployment
- **Provide reproducible results** for academic validation

### 1.2 Research Questions

1. **Performance**: Which model achieves highest classification accuracy?
2. **Efficiency**: What is the speed/accuracy trade-off?
3. **Scalability**: How do models perform on large datasets?
4. **Production Readiness**: Which model is best for real-time API deployment?

### 1.3 Evaluation Criteria

Models are evaluated on four dimensions:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Accuracy** | 40% | Classification correctness (F1-score) |
| **Speed** | 30% | Inference time per comment |
| **Resource Usage** | 20% | Memory, model size, dependencies |
| **Ease of Deployment** | 10% | Integration complexity, maintenance |

---

## 2. Dataset

### 2.1 Data Source

**Dataset**: YouTube Comments Sentiment Dataset  
**Source**: [Kaggle - YouTube Comments Sentiment](https://www.kaggle.com/datasets/amaanpoonawala/youtube-comments-sentiment-dataset)  
**Download Method**: `kagglehub` Python library  

```python
import kagglehub

# Download dataset
path = kagglehub.dataset_download(
    "amaanpoonawala/youtube-comments-sentiment-dataset"
)

# File location
file_path = f'{path}/youtube_comments_cleaned.csv'
```

---

### 2.2 Dataset Characteristics

**Size**:
- **Total Comments**: 1,032,225 comments
- **After Cleaning**: 1,032,225 (100% completeness)
- **File Size**: ~500 MB (CSV)

**Schema**:
| Column | Type | Description |
|--------|------|-------------|
| `CommentID` | String | Unique comment identifier |
| `VideoID` | String | YouTube video identifier |
| `VideoTitle` | String | Title of video |
| `AuthorName` | String | Comment author username |
| `AuthorChannelID` | String | Author's YouTube channel ID |
| `CommentText` | String | **Primary feature**: Comment content |
| `Sentiment` | String | **Target variable**: Positive/Neutral/Negative |
| `Likes` | Integer | Number of likes on comment |
| `Replies` | Integer | Number of replies to comment |
| `PublishedAt` | DateTime | Comment timestamp |
| `CountryCode` | String | Author's country |
| `CategoryID` | Integer | Video category |

**Target Variable** (`Sentiment`):
- **Negative**: 346,075 comments (33.5%)
- **Neutral**: 342,833 comments (33.2%)
- **Positive**: 343,317 comments (33.3%)

**Balance**: Excellent class balance (33.2-33.5% each)

---

### 2.3 Data Preprocessing

**Loading and Cleaning**:
```python
import pandas as pd

# Load dataset
df = pd.read_csv(file_path)

# Remove rows with missing critical fields
df = df.dropna(subset=['VideoTitle', 'CommentText', 'Sentiment'])

# Create context-aware feature
df['CommentTextWithContext'] = df.apply(
    lambda row: f"Video Title: {row['VideoTitle']}. Comment: {row['CommentText']}", 
    axis=1
)

print(f"Total records after cleaning: {len(df):,}")
```

**Text Preprocessing (for ML models)**:
```python
import re
import string

def preprocess_text(text):
    """Preprocess text for sentiment analysis"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Remove user mentions and hashtags
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    
    # Remove special characters and punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

# Apply preprocessing
df['CommentText_Processed'] = df['CommentText'].apply(preprocess_text)
```

**Label Encoding**:
```python
from sklearn.preprocessing import LabelEncoder

# Encode sentiment labels
label_encoder = LabelEncoder()
df['Sentiment_Encoded'] = label_encoder.fit_transform(df['Sentiment'])

# Mapping: Negative=0, Neutral=1, Positive=2
print(dict(enumerate(label_encoder.classes_)))
```

---

### 2.4 Data Splitting

**Train/Test Split** (80/20):
```python
from sklearn.model_selection import train_test_split

# Split data
X = df['CommentText_Processed']  # Features
y = df['Sentiment_Encoded']       # Labels

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.20,        # 20% for testing
    random_state=42,       # Reproducibility
    stratify=y             # Maintain class distribution
)

print(f"Training set: {len(X_train):,} comments")
print(f"Test set: {len(X_test):,} comments")
```

**Split Sizes**:
- **Training**: 825,780 comments (80%)
- **Test**: 206,445 comments (20%)

**Why 80/20 split**:
- Industry standard for large datasets
- Sufficient test data for confident evaluation (206K samples)
- Enough training data for model learning (825K samples)

**Stratification**: Ensures class distribution is preserved in both sets

---

### 2.5 Sampling for Experiments

For computational efficiency, multiple sample sizes were used:

```python
def create_sample(df, n_samples, random_state=42):
    """Create stratified sample of specified size"""
    return df.sample(n=n_samples, random_state=random_state).reset_index(drop=True)

# Sample sizes for different experiments
samples = {
    'quick_test': create_sample(df, 1_000),      # Fast iteration
    'medium_test': create_sample(df, 10_000),    # Model comparison
    'large_test': create_sample(df, 50_000),     # SVM evaluation
    'full_dataset': df                            # Final validation
}
```

**Sample Sizes**:
| Sample Name | Size | Purpose |
|-------------|------|---------|
| Quick Test | 1,000 | Development, debugging |
| Medium Test | 10,000 | Model comparison |
| Large Test | 50,000 | SVM training (computationally expensive) |
| Full Dataset | 1,032,225 | Final model validation |

---

## 3. Model Selection

### 3.1 Model Categories

Five model categories were evaluated:

1. **Rule-based Models**: VADER, TextBlob
2. **Traditional ML**: TF-IDF + Logistic Regression, TF-IDF + SVM
3. **Transformer Models**: DeBERTa-v3-small, Twitter-XLM-RoBERTa (tested but not documented here)

---

### 3.2 Model 1: VADER (Valence Aware Dictionary and sEntiment Reasoner)

**Type**: Rule-based, lexicon-based

**Description**:
- Pre-trained sentiment analyzer optimized for social media
- Uses sentiment lexicon with intensity scores
- No training required

**Implementation**:
```python
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon
nltk.download('vader_lexicon', quiet=True)

# Initialize analyzer
analyzer = SentimentIntensityAnalyzer()

def predict_vader(text):
    """Predict sentiment using VADER"""
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    # Classification thresholds
    if compound >= 0.05:
        return 'POSITIVE'  # Encoded as 2
    elif compound <= -0.05:
        return 'NEGATIVE'  # Encoded as 0
    else:
        return 'NEUTRAL'   # Encoded as 1
```

**Advantages**:
- Very fast (< 0.1ms per comment)
- No training required
- Handles social media slang, emoticons, capitalization
- Explainable (lexicon-based)

**Disadvantages**:
- Limited by lexicon coverage
- Cannot learn from data
- May miss context-dependent sentiment

---

### 3.3 Model 2: TextBlob

**Type**: Rule-based, pattern-based

**Description**:
- Simple sentiment analyzer based on pattern library
- Uses pre-trained sentiment patterns
- No training required

**Implementation**:
```python
from textblob import TextBlob

def predict_textblob(text):
    """Predict sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    # Classification thresholds
    if polarity > 0.1:
        return 'POSITIVE'  # Encoded as 2
    elif polarity < -0.1:
        return 'NEGATIVE'  # Encoded as 0
    else:
        return 'NEUTRAL'   # Encoded as 1
```

**Advantages**:
- Simple API
- Fast processing
- Easy to integrate

**Disadvantages**:
- Less sophisticated than VADER
- Limited to English
- Lower accuracy than ML models

---

### 3.4 Model 3: TF-IDF + Logistic Regression

**Type**: Traditional Machine Learning

**Description**:
- Feature extraction: TF-IDF (Term Frequency-Inverse Document Frequency)
- Classifier: Logistic Regression (multinomial)
- Supervised learning

**Feature Extraction**:
```python
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    max_features=5000,       # Top 5000 most important words
    ngram_range=(1, 2),      # Unigrams and bigrams
    min_df=2,                # Minimum document frequency
    max_df=0.95,             # Maximum document frequency (filter common words)
    strip_accents='unicode', # Remove accents
    lowercase=True,          # Convert to lowercase
    analyzer='word',         # Word-level analysis
    stop_words='english'     # Remove English stop words
)

# Fit and transform training data
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print(f"TF-IDF matrix shape: {X_train_tfidf.shape}")
# Output: (825780, 5000) - 825K samples, 5K features
```

**Classifier Training**:
```python
from sklearn.linear_model import LogisticRegression

# Initialize logistic regression
model = LogisticRegression(
    max_iter=1000,            # Maximum iterations
    solver='lbfgs',           # Optimization algorithm
    multi_class='multinomial', # Multinomial classification
    class_weight='balanced',  # Handle class imbalance
    random_state=42,          # Reproducibility
    n_jobs=-1                 # Use all CPU cores
)

# Train model
model.fit(X_train_tfidf, y_train)

# Predict
y_pred = model.predict(X_test_tfidf)
```

**Advantages**:
- Good balance of accuracy and speed
- Interpretable features (word importance)
- Fast training and inference
- Works well for text classification

**Disadvantages**:
- Requires training data
- Limited by bag-of-words representation
- Doesn't capture word order or context

---

### 3.5 Model 4: TF-IDF + Support Vector Machine (SVM)

**Type**: Traditional Machine Learning

**Description**:
- Feature extraction: TF-IDF (same as Logistic Regression)
- Classifier: Support Vector Machine with RBF kernel
- Supervised learning

**Implementation**:
```python
from sklearn.svm import SVC

# Initialize SVM
model = SVC(
    kernel='rbf',              # Radial Basis Function kernel
    C=1.0,                     # Regularization parameter
    gamma='scale',             # Kernel coefficient
    class_weight='balanced',   # Handle class imbalance
    random_state=42,           # Reproducibility
    cache_size=2000            # Memory cache (MB)
)

# Train model (use sampled data for speed)
model.fit(X_train_tfidf_sample, y_train_sample)

# Predict
y_pred = model.predict(X_test_tfidf)
```

**Advantages**:
- Good generalization
- Robust to overfitting
- Handles non-linear relationships (with RBF kernel)

**Disadvantages**:
- Slow training on large datasets
- Memory intensive
- Less interpretable than Logistic Regression
- Longer inference time

---

## 4. Training Methodology

### 4.1 Training Process

**Step-by-Step Procedure**:

1. **Data Loading**:
   ```python
   df = pd.read_csv('youtube_comments_cleaned.csv')
   ```

2. **Preprocessing**:
   ```python
   df = df.dropna(subset=['CommentText', 'Sentiment'])
   df['CommentText_Processed'] = df['CommentText'].apply(preprocess_text)
   ```

3. **Label Encoding**:
   ```python
   label_encoder = LabelEncoder()
   y = label_encoder.fit_transform(df['Sentiment'])
   ```

4. **Train/Test Split**:
   ```python
   X_train, X_test, y_train, y_test = train_test_split(
       df['CommentText_Processed'], y, 
       test_size=0.20, random_state=42, stratify=y
   )
   ```

5. **Feature Extraction**:
   ```python
   vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
   X_train_tfidf = vectorizer.fit_transform(X_train)
   X_test_tfidf = vectorizer.transform(X_test)
   ```

6. **Model Training**:
   ```python
   model = LogisticRegression(max_iter=1000, solver='lbfgs', 
                               multi_class='multinomial')
   model.fit(X_train_tfidf, y_train)
   ```

7. **Prediction**:
   ```python
   y_pred = model.predict(X_test_tfidf)
   ```

8. **Evaluation**:
   ```python
   from sklearn.metrics import accuracy_score, f1_score, classification_report
   
   accuracy = accuracy_score(y_test, y_pred)
   f1 = f1_score(y_test, y_pred, average='macro')
   print(f"Accuracy: {accuracy:.2%}")
   print(f"F1-Score: {f1:.2%}")
   ```

---

### 4.2 Hyperparameter Tuning

**TF-IDF Parameters**:
```python
# Grid search for optimal TF-IDF parameters
from sklearn.model_selection import GridSearchCV

tfidf_params = {
    'max_features': [3000, 5000, 10000],
    'ngram_range': [(1, 1), (1, 2), (1, 3)],
    'min_df': [2, 5, 10],
    'max_df': [0.90, 0.95, 0.99]
}

# Note: Full grid search is computationally expensive
# Selected parameters based on literature and quick tests
```

**Logistic Regression Parameters**:
```python
lr_params = {
    'max_iter': [500, 1000, 2000],
    'solver': ['lbfgs', 'saga', 'newton-cg'],
    'C': [0.1, 1.0, 10.0]  # Regularization strength
}

# Selected: max_iter=1000, solver='lbfgs', C=1.0 (default)
```

**Selected Hyperparameters** (based on performance):
- TF-IDF: `max_features=5000, ngram_range=(1,2), min_df=2, max_df=0.95`
- Logistic Regression: `max_iter=1000, solver='lbfgs', multi_class='multinomial'`

---

### 4.3 Cross-Validation

**K-Fold Cross-Validation** (for model selection):
```python
from sklearn.model_selection import cross_val_score

# 5-fold cross-validation
cv_scores = cross_val_score(
    model, X_train_tfidf, y_train, 
    cv=5,           # 5 folds
    scoring='f1_macro',  # F1-score (macro average)
    n_jobs=-1       # Parallel processing
)

print(f"CV Scores: {cv_scores}")
print(f"Mean CV F1: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
```

**Why 5-fold CV**:
- Balances computational cost vs. validation thoroughness
- Each fold has ~165K training, ~41K validation samples
- Provides confidence in model generalization

---

### 4.4 Model Serialization

**Saving Trained Models**:
```python
import pickle

# Save model, vectorizer, and label encoder
model_artifacts = {
    'model': model,                   # Trained classifier
    'vectorizer': vectorizer,         # TF-IDF vectorizer
    'label_encoder': label_encoder,   # Sentiment label encoder
    'metadata': {
        'accuracy': accuracy,
        'f1_score': f1_score,
        'training_date': datetime.now().isoformat(),
        'training_samples': len(X_train)
    }
}

with open('tfidf_logistic_model.pkl', 'wb') as f:
    pickle.dump(model_artifacts, f)

print(f"Model saved: {os.path.getsize('tfidf_logistic_model.pkl') / 1024:.0f} KB")
```

**Loading and Using Model**:
```python
# Load model
with open('tfidf_logistic_model.pkl', 'rb') as f:
    artifacts = pickle.load(f)

model = artifacts['model']
vectorizer = artifacts['vectorizer']
label_encoder = artifacts['label_encoder']

# Predict new comment
def predict_sentiment(comment_text):
    # Preprocess
    processed = preprocess_text(comment_text)
    
    # Vectorize
    tfidf = vectorizer.transform([processed])
    
    # Predict
    pred_encoded = model.predict(tfidf)[0]
    sentiment = label_encoder.inverse_transform([pred_encoded])[0]
    
    return sentiment
```

---

## 5. Evaluation Metrics

### 5.1 Primary Metrics

**Accuracy**:
```python
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
```

**Definition**: Proportion of correct predictions
**Formula**: `Accuracy = (TP + TN) / (TP + TN + FP + FN)`
**Interpretation**: Overall correctness across all classes

---

**F1-Score (Macro Average)**:
```python
from sklearn.metrics import f1_score

f1_macro = f1_score(y_test, y_pred, average='macro')
print(f"F1-Score (Macro): {f1_macro:.4f} ({f1_macro*100:.2f}%)")
```

**Definition**: Harmonic mean of precision and recall, averaged across classes
**Formula**: `F1 = 2 × (Precision × Recall) / (Precision + Recall)`
**Why Macro**: Treats all classes equally (important for balanced evaluation)

---

### 5.2 Per-Class Metrics

**Classification Report**:
```python
from sklearn.metrics import classification_report

# Get detailed per-class metrics
report = classification_report(
    y_test, y_pred, 
    target_names=['Negative', 'Neutral', 'Positive'],
    digits=4
)

print(report)
```

**Example Output**:
```
              precision    recall  f1-score   support

    Negative     0.6596    0.6601    0.6599     69215
     Neutral     0.6549    0.6532    0.6540     68567
    Positive     0.6708    0.6710    0.6709     68663

    accuracy                         0.6614    206445
   macro avg     0.6618    0.6614    0.6616    206445
weighted avg     0.6618    0.6614    0.6616    206445
```

**Metrics Explained**:
- **Precision**: Of predicted class X, how many were actually X?
- **Recall**: Of actual class X, how many were predicted as X?
- **F1-Score**: Balance between precision and recall
- **Support**: Number of true instances for each class

---

### 5.3 Confusion Matrix

**Generate Confusion Matrix**:
```python
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Compute confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Visualize
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Negative', 'Neutral', 'Positive'],
            yticklabels=['Negative', 'Neutral', 'Positive'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.savefig('confusion_matrix.png', dpi=300)
```

**Example Confusion Matrix** (TF-IDF + Logistic Regression, Full Dataset):
```
                  Predicted
              Neg      Neu      Pos
Actual Neg   45,639   17,057   6,519
       Neu   14,217   44,848   9,502
       Pos    8,725   13,885  46,053
```

**Interpretation**:
- **Diagonal**: Correct predictions
- **Off-diagonal**: Misclassifications
- **Neg→Neu**: 17,057 negative comments misclassified as neutral

---

### 5.4 Performance Metrics

**Processing Speed**:
```python
import time

# Measure inference time
start_time = time.time()

# Predict on test set
y_pred = model.predict(X_test_tfidf)

elapsed_time = time.time() - start_time
comments_per_second = len(X_test) / elapsed_time

print(f"Total time: {elapsed_time:.2f}s")
print(f"Speed: {comments_per_second:.0f} comments/second")
print(f"Time per comment: {1000*elapsed_time/len(X_test):.2f}ms")
```

**Memory Usage**:
```python
import sys

# Model size
model_size_bytes = sys.getsizeof(pickle.dumps(model))
vectorizer_size_bytes = sys.getsizeof(pickle.dumps(vectorizer))

print(f"Model size: {model_size_bytes / 1024:.0f} KB")
print(f"Vectorizer size: {vectorizer_size_bytes / 1024:.0f} KB")
```

---

## 6. Statistical Analysis

### 6.1 Model Comparison

**Performance Comparison Table**:

| Model | Accuracy | F1 (Macro) | Speed (s/comment) | Model Size |
|-------|----------|------------|-------------------|------------|
| VADER | 53.43% | 52.98% | 0.0001 | N/A |
| TextBlob | 48.80% | 46.80% | 0.0001 | N/A |
| TF-IDF + LR | **66.14%** | **66.28%** | 0.0000 | ~10 MB |
| TF-IDF + SVM | 62.46% | 62.67% | 0.0439 | ~500 MB |

**Winner**: TF-IDF + Logistic Regression (best accuracy, fast speed)

---

### 6.2 Statistical Significance Testing

**McNemar's Test** (compare two classifiers):
```python
from statsmodels.stats.contingency_tables import mcnemar

# Create contingency table
# Counts: [both correct, model1 correct but model2 wrong, 
#          model1 wrong but model2 correct, both wrong]

# Example: Compare VADER vs TF-IDF+LR
vader_correct = (y_test == y_pred_vader)
lr_correct = (y_test == y_pred_lr)

# McNemar contingency table
table = [[
    sum(vader_correct & lr_correct),    # Both correct
    sum(vader_correct & ~lr_correct)    # VADER correct, LR wrong
], [
    sum(~vader_correct & lr_correct),   # VADER wrong, LR correct
    sum(~vader_correct & ~lr_correct)   # Both wrong
]]

# McNemar test
result = mcnemar(table, exact=False, correction=True)
print(f"McNemar's chi-squared: {result.statistic:.2f}")
print(f"p-value: {result.pvalue:.4f}")

if result.pvalue < 0.05:
    print("Difference is statistically significant (p < 0.05)")
else:
    print("Difference is NOT statistically significant")
```

---

### 6.3 Error Analysis

**Identify Common Misclassifications**:
```python
# Find misclassified examples
misclassified_idx = y_test != y_pred

# Sample misclassifications
misclassified_df = pd.DataFrame({
    'text': X_test[misclassified_idx].values,
    'true_label': label_encoder.inverse_transform(y_test[misclassified_idx]),
    'pred_label': label_encoder.inverse_transform(y_pred[misclassified_idx])
})

# Group by error type
error_types = misclassified_df.groupby(['true_label', 'pred_label']).size()
print("Most common errors:")
print(error_types.sort_values(ascending=False).head(10))
```

**Qualitative Analysis**:
```python
# Sample 10 random misclassifications
sample = misclassified_df.sample(10, random_state=42)

for idx, row in sample.iterrows():
    print(f"\nText: {row['text']}")
    print(f"True: {row['true_label']}, Predicted: {row['pred_label']}")
```

**Common Error Patterns**:
1. **Sarcasm**: Model misses sarcastic comments
2. **Mixed sentiment**: Comments with both positive and negative aspects
3. **Context-dependent**: Sentiment depends on external context
4. **Slang/abbreviations**: Informal language not in training data

---

## 7. Reproducibility

### 7.1 Environment Setup

**System Requirements**:
```bash
# Minimum
- Python 3.11 or higher
- 8 GB RAM
- 10 GB disk space
- Internet connection (for dataset download)

# Recommended
- Python 3.12
- 16 GB RAM
- 20 GB disk space
- GPU (for transformer models, optional)
```

**Installation**:
```bash
# Navigate to evaluation directory
cd packages/containers/sentiment_analysis/evaluation/model_evaluation

# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt**:
```
kagglehub==0.2.5
pandas==2.2.0
numpy==1.26.4
scikit-learn==1.4.0
nltk==3.8.1
textblob==0.17.1
matplotlib==3.8.2
seaborn==0.13.2
statsmodels==0.14.1
```

---

### 7.2 Running Model Evaluation

**VADER Evaluation**:
```bash
python vader_classification_report.py

# Outputs:
# - vader_results_full_dataset.txt
# - Accuracy, F1-score, confusion matrix
```

**TextBlob Evaluation**:
```bash
python textblob_classification_report.py

# Outputs:
# - textblob_results_full_dataset.txt
```

**TF-IDF + Logistic Regression**:
```bash
python tfidf_logistic_classification_report.py

# Outputs:
# - tfidf_logistic_results.txt
# - tfidf_logistic_model.pkl (trained model)
```

**TF-IDF + SVM**:
```bash
python svm_classification_report.py

# Note: Uses 50,000 sample for speed
# Outputs:
# - svm_results.txt
# - svm_model.pkl
```

**Comprehensive Comparison**:
```bash
python comprehensive_model_comparison.py

# Generates comparison across all models
# Outputs:
# - comprehensive_model_comparison.txt
# - Comparison table, graphs
```

---

### 7.3 Expected Results

**Expected Metrics** (may vary slightly due to randomness):

| Model | Expected Accuracy | Expected F1 | Variance |
|-------|-------------------|-------------|----------|
| VADER | 53.43% ± 0.5% | 52.98% ± 0.5% | Low |
| TextBlob | 48.80% ± 0.5% | 46.80% ± 0.5% | Low |
| TF-IDF + LR | 66.14% ± 1.0% | 66.28% ± 1.0% | Medium |
| TF-IDF + SVM | 62.46% ± 2.0% | 62.67% ± 2.0% | Higher |

**Why variance exists**:
- **Random seed**: Different random seeds affect train/test split
- **Initialization**: Model initialization randomness (for LR, SVM)
- **Sampling**: Sampling for SVM (uses 50K subset)

**Reproducibility tips**:
- Use `random_state=42` consistently
- Save random seeds in results
- Document Python version, library versions

---

## 8. Limitations

### 8.1 Dataset Limitations

**Language**: 
- **Limitation**: Primarily English comments
- **Impact**: Models may not generalize to other languages
- **Mitigation**: Document limitation, consider multilingual models

**Bias**:
- **Limitation**: Dataset may have platform bias (YouTube)
- **Impact**: May not generalize to other platforms (Twitter, Reddit)
- **Mitigation**: Test on diverse datasets when possible

**Temporal**:
- **Limitation**: Dataset snapshot from specific time period
- **Impact**: May not capture evolving language trends
- **Mitigation**: Regular model retraining with fresh data

---

### 8.2 Model Limitations

**Context**:
- **Limitation**: TF-IDF models don't capture word order, context
- **Impact**: May miss sarcasm, irony, context-dependent sentiment
- **Mitigation**: Consider transformer models for higher accuracy

**Domain Adaptation**:
- **Limitation**: Models trained on YouTube comments
- **Impact**: May perform poorly on other domains (product reviews, news)
- **Mitigation**: Domain-specific training for production use

**Class Imbalance** (if it exists):
- **Limitation**: If certain sentiments are rare
- **Impact**: Model may bias toward majority class
- **Mitigation**: Use class weights, stratified sampling

---

### 8.3 Evaluation Limitations

**Held-out Test Set**:
- **Limitation**: Single test set (20%)
- **Impact**: Results may vary on different test sets
- **Mitigation**: Cross-validation, multiple runs

**Metrics**:
- **Limitation**: Accuracy/F1 don't capture all nuances
- **Impact**: May not reflect real-world user satisfaction
- **Mitigation**: Include qualitative error analysis

---

### 8.4 Assumptions

**Key Assumptions**:

1. **Ground Truth Labels are Correct**:
   - **Assumption**: Dataset labels are accurate
   - **Reality**: Human annotation may have errors (~5-10%)
   - **Impact**: Ceiling on achievable accuracy

2. **IID (Independent and Identically Distributed)**:
   - **Assumption**: Train and test data come from same distribution
   - **Reality**: Language evolves, platform changes
   - **Impact**: Model may degrade over time

3. **Representative Sample**:
   - **Assumption**: Test set represents real-world usage
   - **Reality**: May not cover all edge cases
   - **Impact**: Production performance may differ

---

## 9. Conclusion

This methodology provides a rigorous, reproducible approach to sentiment analysis model evaluation. Key strengths:

✅ **Large Dataset**: 1M+ comments for robust evaluation  
✅ **Multiple Models**: Comprehensive comparison across 4 model types  
✅ **Rigorous Metrics**: Accuracy, F1, precision, recall, confusion matrix  
✅ **Speed Analysis**: Computational efficiency measured  
✅ **Reproducible**: Detailed procedures, scripts, random seeds  
✅ **Transparent**: Limitations and assumptions documented  

**Final Model Selection**: **TF-IDF + Logistic Regression**
- **Accuracy**: 66.14% (best among ML models)
- **Speed**: Very fast (< 1ms per comment)
- **Deployment**: Easy (small model size, simple inference)
- **Production**: Deployed in YouTube Comment Reader API

---

**Document Version**: 1.0  
**Last Updated**: October 27, 2025  
**Author**: Guilherme Avelino  
**Status**: Complete  

---

## 10. References

**Dataset**:
- [YouTube Comments Sentiment Dataset (Kaggle)](https://www.kaggle.com/datasets/amaanpoonawala/youtube-comments-sentiment-dataset)

**Libraries**:
- [scikit-learn Documentation](https://scikit-learn.org/stable/)
- [NLTK VADER](https://www.nltk.org/howto/sentiment.html)
- [TextBlob](https://textblob.readthedocs.io/)
- [Pandas](https://pandas.pydata.org/)

**Academic**:
- Pang, B., & Lee, L. (2008). *Opinion mining and sentiment analysis*. Foundations and Trends in Information Retrieval, 2(1-2), 1-135.
- Hutto, C. J., & Gilbert, E. (2014). VADER: A parsimonious rule-based model for sentiment analysis of social media text. ICWSM.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. JMLR, 12, 2825-2830.


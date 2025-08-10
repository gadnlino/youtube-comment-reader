# VADER Sentiment Analysis for YouTube Comments

This directory contains scripts to perform VADER sentiment analysis on the YouTube comments dataset and calculate classification metrics.

## 📁 Files

### Main Scripts
- `vader_classification_report.py` - Comprehensive analysis script that processes the full dataset
- `vader_quick_test.py` - Quick test script for smaller samples (faster execution)
- `fix_nltk_ssl.py` - Helper script to fix NLTK SSL certificate issues
- `nltk_setup.py` - NLTK setup script for Jupyter notebooks

### Results
- `vader_results_full_dataset.txt` - Results from analyzing the full dataset
- `vader_results_1000.txt`, `vader_results_5000.txt`, etc. - Results from different sample sizes

## 🚀 Quick Start

### Option 1: Quick Test (Recommended for testing)
```bash
python vader_quick_test.py
```

### Option 2: Full Analysis
```bash
python vader_classification_report.py
```

## 📊 Results Summary

### Full Dataset Analysis (1,032,225 comments)
- **Accuracy**: 53.43%
- **F1 (Macro)**: 52.98%
- **F1 (Weighted)**: 52.98%
- **Processing Time**: 101.86 seconds
- **Average per comment**: 0.0001 seconds

### Per-Class Performance (Full Dataset)
| Class    | Precision | Recall | F1-Score | Support |
|----------|-----------|--------|----------|---------|
| Negative | 0.6305    | 0.4236 | 0.5068   | 346,075 |
| Neutral  | 0.4960    | 0.4942 | 0.4951   | 342,833 |
| Positive | 0.5140    | 0.6858 | 0.5876   | 343,317 |

### Quick Test Results (1,000 comments)
- **Accuracy**: 51.80%
- **F1 (Macro)**: 51.47%
- **Processing Time**: 0.11 seconds

## 🔧 Technical Details

### Dataset
- **Source**: YouTube Comments Sentiment Dataset from Kaggle
- **Size**: 1,032,225 comments after cleaning
- **Classes**: Negative, Neutral, Positive
- **Features**: CommentText, VideoTitle, Sentiment

### VADER Configuration
- **Threshold**: ±0.05 compound score
- **Lexicon**: VADER lexicon from NLTK
- **SSL Fix**: Automatic SSL certificate handling for macOS

### Performance Characteristics
- **Speed**: ~0.0001 seconds per comment
- **Memory**: Efficient processing with progress tracking
- **Scalability**: Can handle full dataset (>1M comments)

## 📈 Comparison with Other Models

The VADER results can be compared with the transformer models in the Jupyter notebook:

| Model | Accuracy | F1 (Macro) | Processing Time |
|-------|----------|-------------|-----------------|
| VADER | 53.43% | 52.98% | ~102s |
| DeBERTa-v3-small | ~73% | ~73% | ~20min |
| Twitter-XLM-RoBERTa | ~71% | ~71% | ~30min |

## 🛠️ Troubleshooting

### SSL Certificate Issues
If you encounter SSL certificate errors:
```bash
python fix_nltk_ssl.py
```

### NLTK Download Issues
The scripts automatically handle NLTK SSL issues, but if problems persist:
1. Run `python fix_nltk_ssl.py`
2. Check your internet connection
3. Try running with a VPN if needed

## 📝 Usage in Jupyter Notebooks

You can import the setup script in your notebook:
```python
import nltk_setup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# VADER is now ready to use
analyzer = SentimentIntensityAnalyzer()
```

## 🎯 Key Findings

1. **Baseline Performance**: VADER provides a reasonable baseline with ~53% accuracy
2. **Speed**: Very fast processing (~0.0001s per comment)
3. **Class Imbalance**: Handles the balanced dataset well
4. **Positive Bias**: Slightly better at identifying positive sentiments
5. **Resource Efficient**: No GPU required, minimal memory usage

## 🔄 Next Steps

1. **Compare with other baselines**: TextBlob, AFINN, etc.
2. **Fine-tune thresholds**: Experiment with different compound score thresholds
3. **Feature engineering**: Combine with other features
4. **Ensemble methods**: Combine VADER with transformer models

## 📚 References

- VADER: [Valence Aware Dictionary and sEntiment Reasoner](https://github.com/cjhutto/vaderSentiment)
- Dataset: [YouTube Comments Sentiment Dataset](https://www.kaggle.com/datasets/amaanpoonawala/youtube-comments-sentiment-dataset)
- NLTK: [Natural Language Toolkit](https://www.nltk.org/) 
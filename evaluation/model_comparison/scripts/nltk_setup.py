#!/usr/bin/env python3
"""
NLTK setup script for Jupyter notebooks
Handles SSL certificate issues and VADER lexicon download
"""

import ssl
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def setup_nltk():
    """Setup NLTK with SSL certificate fixes"""
    # Fix SSL certificate issues on macOS
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    # Download VADER lexicon with error handling
    try:
        nltk.download('vader_lexicon', quiet=True)
        print("✅ VADER lexicon downloaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error downloading VADER lexicon: {e}")
        print("The lexicon may already be downloaded or you may need to run "
              "the fix_nltk_ssl.py script.")
        return False


def get_vader_analyzer():
    """Get a VADER sentiment analyzer instance"""
    try:
        analyzer = SentimentIntensityAnalyzer()
        return analyzer
    except Exception as e:
        print(f"❌ Error creating VADER analyzer: {e}")
        return None


# Auto-setup when imported
if __name__ == "__main__":
    setup_nltk()
else:
    # When imported in notebook, setup automatically
    setup_nltk() 
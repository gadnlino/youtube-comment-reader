#!/usr/bin/env python3
"""
Helper script to fix NLTK SSL certificate issues on macOS
"""

import ssl
import nltk
import os
import urllib.request
import zipfile


def fix_nltk_ssl():
    """Fix SSL certificate issues for NLTK downloads"""
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context


def download_vader_lexicon():
    """Download VADER lexicon with fallback methods"""
    try:
        # Try normal download first
        nltk.download('vader_lexicon', quiet=True)
        print("VADER lexicon downloaded successfully!")
        return True
    except Exception as e:
        print(f"Standard download failed: {e}")
        print("Trying alternative download method...")
        
        try:
            # Manual download
            nltk_data_dir = os.path.expanduser('~/nltk_data')
            sentiment_dir = os.path.join(nltk_data_dir, "sentiment")
            os.makedirs(sentiment_dir, exist_ok=True)
            
            # Download VADER lexicon
            vader_url = ("https://raw.githubusercontent.com/nltk/nltk_data/"
                         "gh-pages/packages/sentiment/vader_lexicon.zip")
            vader_zip_path = os.path.join(sentiment_dir, "vader_lexicon.zip")
            
            print("Downloading VADER lexicon...")
            urllib.request.urlretrieve(vader_url, vader_zip_path)
            
            # Extract the zip file
            with zipfile.ZipFile(vader_zip_path, 'r') as zip_ref:
                zip_ref.extractall(sentiment_dir)
            
            # Clean up zip file
            os.remove(vader_zip_path)
            
            print("VADER lexicon downloaded and extracted successfully!")
            return True
            
        except Exception as e2:
            print(f"Alternative download also failed: {e2}")
            return False


if __name__ == "__main__":
    fix_nltk_ssl()
    success = download_vader_lexicon()
    if success:
        print("NLTK setup completed successfully!")
    else:
        print("NLTK setup failed. You may need to manually download the "
              "VADER lexicon.") 
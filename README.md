# YouTube Comment Sentiment Analysis (SVM vs VADER)

This project is an end-to-end NLP web application that analyzes the sentiment of YouTube video comments.  
It compares a custom-trained Machine Learning model (SVM) with a rule-based sentiment analyzer (VADER) and displays the results side by side.

---
<img width="1855" height="947" alt="image" src="https://github.com/user-attachments/assets/20fd04ae-18cf-4e89-bf0a-b50cc5254301" />

## Project Overview

The application takes a YouTube video URL as input, fetches comments using the YouTube Data API, and classifies them into Positive, Neutral, and Negative sentiments.

Two different approaches are used:
- A supervised Machine Learning model (TF-IDF + Linear SVM)
- A rule-based NLP model (VADER)

This helps in understanding the difference between trained models and lexicon-based approaches on real-world data.

---

## Features

- Accepts YouTube video URL
- Fetches comments using YouTube Data API
- Sentiment analysis using:
  - SVM (custom trained model)
  - VADER (rule-based)
- Side-by-side comparison of sentiment results
- Flask backend with HTML, CSS, and JavaScript frontend
- Clean and modular project structure

---

## Sentiment Techniques Used

### SVM (Supervised Machine Learning)
- Uses TF-IDF for text vectorization
- Linear Support Vector Machine classifier
- Trained on labeled sentiment data
- Better handling of neutral and contextual text

### VADER (Rule-Based NLP)
- Lexicon and rule-based approach
- No training required
- Optimized for social media text
- Faster but tends to be optimistic

---

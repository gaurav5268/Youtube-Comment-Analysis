import joblib
import requests
import re
import os
from dotenv import load_dotenv

# ===== VADER =====
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")

load_dotenv()
YOUTUBE_API_KEY = os.getenv("api")

if not YOUTUBE_API_KEY:
    raise RuntimeError("YouTube API key not found in .env")


pipeline = joblib.load("sentiment_pipeline.pkl")
vader = SentimentIntensityAnalyzer()


def extract_video_id(url):
    patterns = [
        r"(?:v=)([0-9A-Za-z_-]{11})",
        r"(?:youtu\.be/)([0-9A-Za-z_-]{11})",
        r"(?:embed/)([0-9A-Za-z_-]{11})",
        r"(?:shorts/)([0-9A-Za-z_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_comments(video_id, max_comments=100):
    comments = []
    url = "https://www.googleapis.com/youtube/v3/commentThreads"

    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": YOUTUBE_API_KEY,
        "maxResults": 100,
        "textFormat": "plainText"
    }

    while len(comments) < max_comments:
        response = requests.get(url, params=params).json()

        if "error" in response:
            print("YouTube API error:", response["error"])
            break

        for item in response.get("items", []):
            text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(text)

        if "nextPageToken" in response:
            params["pageToken"] = response["nextPageToken"]
        else:
            break

    return comments[:max_comments]


def vader_sentiment(text):
    score = vader.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def analyze_comments(comments):
    # ---- SVM ----
    svm_preds = pipeline.predict(comments)

    svm_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for p in svm_preds:
        if p == "Irrelevant":
            svm_counts["Neutral"] += 1
        else:
            svm_counts[p] += 1

    # ---- VADER ----
    vader_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for c in comments:
        v = vader_sentiment(c)
        vader_counts[v] += 1

    return svm_counts, vader_counts

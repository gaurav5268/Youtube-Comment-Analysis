from flask import Flask, request, jsonify, render_template

from youtube_comments import extract_video_id, fetch_comments
from sentiment_model import predict_sentiment

app = Flask(__name__)


# -----------------------------
# Frontend page
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# -----------------------------
# Sentiment API
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "YouTube URL is required"}), 400

    url = data["url"]

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    comments = fetch_comments(video_id)

    positive = negative = neutral = 0

    for comment in comments:
        sentiment = predict_sentiment(comment)

        if sentiment == "positive":
            positive += 1
        elif sentiment == "negative":
            negative += 1
        else:
            neutral += 1

    return jsonify({
        "total_comments": len(comments),
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    })


if __name__ == "__main__":
    app.run(debug=True)

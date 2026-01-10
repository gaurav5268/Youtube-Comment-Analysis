from flask import Flask, request, jsonify, render_template
from services import (
    extract_video_id,
    fetch_comments,
    analyze_comments
)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        video_url = data.get("url")

        if not video_url:
            return jsonify({"error": "YouTube URL is required"}), 400

        video_id = extract_video_id(video_url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        comments = fetch_comments(video_id)
        if not comments:
            return jsonify({"error": "No comments found or comments disabled"}), 404

        svm_counts, vader_counts = analyze_comments(comments)

        return jsonify({
            "total_comments": len(comments),
            "svm": svm_counts,
            "vader": vader_counts
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

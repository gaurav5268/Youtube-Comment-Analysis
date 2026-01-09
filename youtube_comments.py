import re
import pandas as pd
from googleapiclient.discovery import build
import dotenv
dotenv.load_dotenv()


API_KEY = dotenv.get_key(".env", "api")
MAX_COMMENTS = 300


def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def fetch_comments(video_id, max_comments=MAX_COMMENTS):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    comments = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )

    while request and len(comments) < max_comments:
        response = request.execute()

        for item in response["items"]:
            text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(text)

            if len(comments) >= max_comments:
                break

        request = youtube.commentThreads().list_next(request, response)

    return comments

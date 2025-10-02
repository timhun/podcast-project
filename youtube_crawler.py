import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from supabase import create_client

load_dotenv()

def main():
    youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
    supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    request = youtube.search().list(
        part="snippet",
        q="investment QQQ",
        type="video",
        maxResults=5,
        order="viewCount"
    )
    response = request.execute()

    count = 0
    for item in response["items"]:
        video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        title = item["snippet"]["title"]
        supabase.table("raw_data").insert({
            "url": video_url,
            "title": title,
            "source": "YouTube"
        }).execute()
        count += 1

    return {"status": f"Fetched and stored {count} videos"}

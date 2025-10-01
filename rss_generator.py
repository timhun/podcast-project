import os
import xml.etree.ElementTree as ET
from supabase import create_client
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def generate_rss():
    # 從 Supabase 獲取 metadata
    response = supabase.table("metadata").select("episode_id, title, gcs_mp3_url").eq("status", "Synthesized").execute()
    root = ET.Element("rss", version="2.0")
    channel = ET.SubElement(root, "channel")
    ET.SubElement(channel, "title").text = "AI Investment Podcast"
    ET.SubElement(channel, "description").text = "Daily AI-driven investment insights"
    for item in response.data:
        episode = ET.SubElement(channel, "item")
        ET.SubElement(episode, "title").text = item["title"] or "Episode"
        ET.SubElement(episode, "description").text = "Investment episode"
        ET.SubElement(episode, "pubDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        ET.SubElement(episode, "enclosure", url=item["gcs_mp3_url"], type="audio/mpeg")
    tree = ET.ElementTree(root)
    tree.write("rss.xml")
    print("Generated rss.xml")

if __name__ == "__main__":
    generate_rss()
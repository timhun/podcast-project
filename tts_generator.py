import os
import asyncio
from supabase import create_client
from edge_tts import Communicate
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

async def generate_podcast(episode_id, text, output_file="output.mp3"):
    tts = Communicate(text=text, voice="en-US-GuyNeural")
    await tts.save(output_file)
    supabase.table("metadata").update({
        "gcs_mp3_url": output_file,  # 臨時路徑，後續改為 GCS URL
        "status": "Synthesized"
    }).eq("episode_id", episode_id).execute()
    print(f"Generated MP3: {output_file}")

if __name__ == "__main__":
    # 模擬從 Supabase 獲取稿件
    response = supabase.table("processed_data").select("final_script, episode_id").limit(1).execute()
    if response.data:
        episode_id = response.data[0]["episode_id"]
        text = response.data[0]["final_script"] or "Welcome to the AI Investment Podcast!"
        asyncio.run(generate_podcast(episode_id, text))
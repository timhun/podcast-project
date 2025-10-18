from __future__ import annotations
import wmill
import logging
from datetime import datetime, UTC
import requests
from dotenv import load_dotenv
from supabase import create_client
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
youtube_api_key = wmill.get_variable("u/timoneway/YOUTUBE_API_KEY")
supabase_url = "http://localhost:5432"  # 本地 PostgreSQL
supabase_key = "dummy"  # 本地無需 key
groq_api_key = wmill.get_variable("u/timoneway/GROQ_API_KEY")
client = create_client(supabase_url, supabase_key)

def build_prompt(videos: list[dict], market_data: dict) -> str:
    prompt = ("Create a 2-minute podcast script for beginner investors about 'investment QQQ'. "
              "Use a friendly, engaging tone with an introduction, key insights from each video, a section on recent QQQ market trends, and a motivational closing. "
              "Include video titles, key takeaways, and one actionable investment tip:\n")
    for video in videos:
        prompt += f"- Title: {video.get('title', 'Unknown')}\n  URL: {video.get('url', '#')}\n"
    prompt += f"\nRecent QQQ Price: {market_data.get('Time Series (Daily)', {}).get('2025-10-15', {}).get('4. close', 'N/A')}\n"
    prompt += ("\nEnsure the script is concise, avoids jargon, includes one actionable tip, and inspires listeners.")
    return prompt

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=60), retry=retry_if_exception_type(requests.exceptions.HTTPError))
def fetch_market_data():
    api_key = wmill.get_variable("u/timoneway/ALPHA_VANTAGE_API_KEY")
    if not api_key:
        logger.warning("ALPHA_VANTAGE_API_KEY not set, returning empty market data")
        return {}
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=QQQ&apikey={api_key}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=60), retry=retry_if_exception_type(requests.exceptions.HTTPError))
def call_groq_api(prompt: str) -> dict:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_api_key}"}
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()

def main() -> dict:
    try:
        videos = client.table("raw_data").select("*").order("fetched_at", desc=True).limit(5).execute().data
        if not videos:
            raise ValueError("No data found in raw_data table")
        logger.info(f"Fetched {len(videos)} videos")
        market_data = fetch_market_data()
        prompt = build_prompt(videos, market_data)
        response_json = call_groq_api(prompt)
        script = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not script:
            raise RuntimeError("No script content returned by Groq")
        client.table("podcast_scripts").insert([{
            "script": script,
            "source": "LLM_Groq",
            "created_at": datetime.now(UTC).isoformat()
        }]).execute()
        logger.info("Script stored successfully")
        return {"status": "Generated podcast script", "script": script}
    except Exception as exc:
        logger.exception("Failed to generate podcast script")
        return {"status": "Error", "error": str(exc)}

if __name__ == "__main__":
    result = main()
    print(result)
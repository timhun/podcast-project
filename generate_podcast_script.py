from __future__ import annotations
import wmill
import os
import logging
from datetime import datetime, UTC  # 添加 UTC 導入
import requests
from dotenv import load_dotenv
from supabase import create_client
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
youtube_api_key = wmill.get_variable("u/timoneway/YOUTUBE_API_KEY")
SUPABASE_URL = wmill.get_variable("u/timoneway/SUPABASE_URL")
SUPABASE_KEY = wmill.get_variable("u/timoneway/SUPABASE_KEY")
GROQ_API_KEY = wmill.get_variable("u/timoneway/GROQ_API_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, GROQ_API_KEY]):
    missing = [k for k, v in {"SUPABASE_URL": SUPABASE_URL,
                              "SUPABASE_KEY": SUPABASE_KEY,
                              "GROQ_API_KEY": GROQ_API_KEY}.items() if not v]
    raise RuntimeError(f"Missing environment variables: {missing}")

client = create_client(SUPABASE_URL, SUPABASE_KEY)

def build_prompt(videos: list[dict], market_data: dict) -> str:
    """Create the user prompt from the recent YouTube videos."""
    prompt = ("Create a 2-minute podcast script summarizing the following YouTube videos about 'investment QQQ' for beginner investors. "
              "Use a friendly, engaging tone and structure the script with an introduction, key insights from each video, and a motivational closing. "
              "Include video titles and key takeaways:\n")
    for video in videos:
        prompt += f"- Title: {video.get('title', 'Unknown')}\n  URL: {video.get('url', '#')}\n"
    prompt += f"\nRecent QQQ Price: {market_data.get('Time Series (Daily)', {}).get('2025-10-11', {}).get('4. close', 'N/A')}\n"
    prompt += ("\nEnsure the script is concise, avoids jargon, and inspires listeners to explore QQQ investments.")
    return prompt

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type(requests.exceptions.HTTPError),
)
def call_groq_api(prompt: str) -> dict:
    """Call Groq and return the raw JSON response."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        error_message = f"HTTP Error {e.response.status_code}: {e.response.text}"
        logger.error(error_message)
        raise requests.exceptions.HTTPError(error_message)

def fetch_market_data():
    import requests
    api_key = wmill.get_variable("u/timoneway/ALPHA_VANTAGE_API_KEY")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=QQQ&apikey={api_key}"
    response = requests.get(url)
    return response.json()

def main() -> dict:
    try:
        videos = client.table("raw_data")\
            .select("*")\
            .order("fetched_at", desc=True)\
            .limit(5)\
            .execute().data

        if not videos:
            raise ValueError("No data found in raw_data table")

        logger.info(f"Fetched {len(videos)} videos")
        market_data = fetch_market_data()  # 添加調用
        prompt = build_prompt(videos, market_data)

        response_json = call_groq_api(prompt)
        script = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")

        if not script:
            raise RuntimeError("No script content returned by Groq")

        client.table("podcast_scripts")\
            .insert([{
                "script": script,
                "source": "LLM_Groq",
                "created_at": datetime.now(UTC).isoformat()
            }])\
            .execute()

        logger.info("Script stored successfully")
        return {"status": "Generated podcast script", "script": script}

    except Exception as exc:  # pragma: no cover
        logger.exception("Failed to generate podcast script")
        return {"status": "Error", "error": str(exc)}
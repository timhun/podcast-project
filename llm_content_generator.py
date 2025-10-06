from __future__ import annotations

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
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, GROQ_API_KEY]):
    missing = [k for k, v in {"SUPABASE_URL": SUPABASE_URL,
                              "SUPABASE_KEY": SUPABASE_KEY,
                              "GROQ_API_KEY": GROQ_API_KEY}.items() if not v]
    raise RuntimeError(f"Missing environment variables: {missing}")

client = create_client(SUPABASE_URL, SUPABASE_KEY)

def build_prompt(videos: list[dict]) -> str:
    """Create the user prompt from the recent YouTube videos."""
    prompt = ("Create a 2-minute podcast script summarizing the following "
              "YouTube videos about 'investment QQQ':\n")
    for video in videos:
        prompt += f"- Title: {video.get('title', 'Unknown')}\n  URL: {video.get('url', '#')}\n"
    prompt += ("\nGenerate the script in a conversational tone, "
               "mentioning the video titles.")
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
        "max_tokens": 500,
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        error_message = f"HTTP Error {e.response.status_code}: {e.response.text}"
        logger.error(error_message)
        raise requests.exceptions.HTTPError(error_message)

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
        prompt = build_prompt(videos)

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

if __name__ == "__main__":  # pragma: no cover
    result = main()
    print(result)
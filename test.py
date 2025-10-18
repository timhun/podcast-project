import os
import requests

api_key = os.getenv("GROQ_API_KEY")
headers = {"Authorization": f"Bearer {api_key}"}

resp = requests.get("https://api.groq.com/openai/v1/models", headers=headers)
print(resp.status_code)
print(resp.json() if resp.ok else resp.text)
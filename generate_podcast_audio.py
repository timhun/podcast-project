from gtts import gTTS
import wmill
import logging
from datetime import datetime, UTC

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(script_result: dict) -> dict:
    try:
        script_content = script_result.get('script', '')
        if not script_content:
            raise ValueError("No script content provided")

        # 清理腳本格式，移除 Markdown 標記
        clean_text = script_content.replace('**', '').replace('\n\n', '\n').strip()

        # 生成音頻
        tts = gTTS(text=clean_text, lang='en', slow=False)
        output_path = f"/app/project/podcast_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.mp3"
        tts.save(output_path)

        logger.info(f"Audio generated at {output_path}")
        return {"status": "Audio generated", "audio_path": output_path}
    except Exception as exc:
        logger.exception("Failed to generate audio")
        return {"status": "Error", "error": str(exc)}
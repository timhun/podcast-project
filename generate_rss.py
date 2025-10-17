import xml.etree.ElementTree as ET
from datetime import datetime, UTC
import wmill
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(script_result: dict, audio_result: dict | None = None) -> dict:
    try:
        script_content = script_result.get('script', 'No script generated')
        audio_path = audio_result.get('audio_path', 'No audio generated') if audio_result is not None else 'No audio result provided'
        if not audio_path or audio_path == 'No audio result provided':
            raise ValueError("No valid audio path provided")

        # RSS 結構
        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")
        ET.SubElement(channel, "title").text = "Investing in QQQ Podcast"
        ET.SubElement(channel, "description").text = "Daily podcast on QQQ investment strategies"
        ET.SubElement(channel, "language").text = "en-us"
        ET.SubElement(channel, "pubDate").text = datetime.now(UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")

        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = "Episode: Investing in QQQ"
        ET.SubElement(item, "description").text = script_content[:200] + "..."
        ET.SubElement(item, "pubDate").text = datetime.now(UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")
        ET.SubElement(item, "enclosure", url=f"file://{audio_path}", type="audio/mpeg")

        # 保存 RSS
        output_path = f"/app/project/podcast_rss_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.xml"
        tree = ET.ElementTree(rss)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

        logger.info(f"RSS generated at {output_path}")
        return {"status": "RSS generated", "rss_path": output_path}
    except Exception as exc:
        logger.exception("Failed to generate RSS")
        return {"status": "Error", "error": str(exc)}
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
        rss = ET.Element("rss", version="2.0", attrib={"xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})
        channel = ET.SubElement(rss, "channel")
        ET.SubElement(channel, "title").text = "Investing in QQQ Podcast"
        ET.SubElement(channel, "description").text = "Daily podcast on QQQ investment strategies"
        ET.SubElement(channel, "language").text = "en-us"
        ET.SubElement(channel, "itunes:author").text = "Tim Oneway"
        ET.SubElement(channel, "itunes:explicit").text = "no"
        ET.SubElement(channel, "pubDate").text = datetime.now(UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")

        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = "Episode: Investing in QQQ"
        ET.SubElement(item, "description").text = script_content[:200] + "..."
        ET.SubElement(item, "pubDate").text = datetime.now(UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")
        # 使用公開 URL（模擬未來雲端）
        public_url = f"http://example.com/podcast/{audio_path.split('/')[-1]}"  # 未來替換為真實雲端 URL
        ET.SubElement(item, "enclosure", url=public_url, type="audio/mpeg")
        ET.SubElement(item, "itunes:duration").text = "120"  # 假設 2 分鐘

        # 保存 RSS
        output_path = f"/app/project/podcast_rss_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.xml"
        tree = ET.ElementTree(rss)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

        logger.info(f"RSS generated at {output_path}")
        return {"status": "RSS generated", "rss_path": output_path, "public_url": public_url}
    except Exception as exc:
        logger.exception("Failed to generate RSS")
        return {"status": "Error", "error": str(exc)}
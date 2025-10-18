import psycopg2
from supabase import create_client
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # 本地 PostgreSQL 連線
        local_conn = psycopg2.connect(
            dbname="windmill",
            user="postgres",
            password="postgres",
            host="localhost"
        )
        cursor = local_conn.cursor()

        # 提取最小資料集
        cursor.execute("SELECT title, url, fetched_at FROM raw_data ORDER BY fetched_at DESC LIMIT 5")
        raw_data = cursor.fetchall()
        
        # ✅ 修正：加入 source 欄位
        cursor.execute("SELECT script, source, created_at FROM podcast_scripts ORDER BY created_at DESC LIMIT 5")
        podcast_scripts = cursor.fetchall()
        
        cursor.close()
        local_conn.close()

        # Supabase 連線
        supabase_url = "https://aynxwbozwlftwurmylkv.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF5bnh3Ym96d2xmdHd1cm15bGt2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5ODgwMTUsImV4cCI6MjA3NDU2NDAxNX0.ofjt6mDxwW7HZjXce3gq4-4kXxQRYtV0GGOXo-QTXGE"
        client = create_client(supabase_url, supabase_key)

        # 上傳 raw_data
        for title, url, fetched_at in raw_data:
            client.table("raw_data").insert({
                "title": title,
                "url": url,
                "fetched_at": fetched_at.isoformat()
            }).execute()
            logger.info(f"Inserted raw_data: {title}")

        # ✅ 修正：上傳 podcast_scripts 時包含 source
        for script, source, created_at in podcast_scripts:
            client.table("podcast_scripts").insert({
                "script": script,
                "source": source if source else "Unknown",  # 如果 source 為 None，使用預設值
                "created_at": created_at.isoformat()
            }).execute()
            logger.info(f"Inserted podcast_script with source: {source}")

        return {"status": "Minimal data migrated"}
    except Exception as exc:
        logger.exception("Failed to migrate data")
        return {"status": "Error", "error": str(exc)}

if __name__ == "__main__":
    print(main())
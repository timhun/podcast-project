import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import wmill
from datetime import datetime, UTC

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(script_result: dict, audio_result: dict) -> dict:
    smtp_server = wmill.get_variable("u/timoneway/SMTP_SERVER") or "smtp.gmail.com"
    smtp_port = int(wmill.get_variable("u/timoneway/SMTP_PORT") or "587")
    smtp_user = wmill.get_variable("u/timoneway/SMTP_USER")
    smtp_password = wmill.get_variable("u/timoneway/SMTP_PASSWORD")
    recipient_email = wmill.get_variable("u/timoneway/RECIPIENT_EMAIL")

    if not all([smtp_user, smtp_password, recipient_email]):
        raise RuntimeError(f"Missing SMTP environment variables")

    script_content = script_result.get('script', 'No script generated')
    audio_path = audio_result.get('audio_path', 'No audio generated')
    msg = MIMEMultipart('alternative')
    msg["Subject"] = f"Podcast Script Run - {datetime.now(UTC).isoformat()}"
    msg["From"] = smtp_user
    msg["To"] = recipient_email

    text = f"New Podcast Script Generated\n\n{script_content}\n\nAudio Path: {audio_path}\n\nStatus: {script_result.get('status', 'Unknown')}"
    html = f"""<html><body><h2>New Podcast Script Generated</h2><pre>{script_content}</pre><p><b>Audio Path:</b> {audio_path}</p><p><b>Status:</b> {script_result.get('status', 'Unknown')}</p></body></html>"""
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, recipient_email, msg.as_string())
        logger.info("Notification sent successfully")
        return {"status": "Notification sent"}
    except Exception as e:
        logger.exception("Failed to send notification")
        raise RuntimeError(f"Failed to send notification: {str(e)}")
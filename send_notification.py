import smtplib
from email.mime.text import MIMEText
import wmill
from datetime import datetime, UTC

def main(script_result: dict) -> dict:
    smtp_server = wmill.get_variable("u/timoneway/SMTP_SERVER") or "smtp.gmail.com"
    smtp_port = int(wmill.get_variable("u/timoneway/SMTP_PORT") or "587")
    smtp_user = wmill.get_variable("u/timoneway/SMTP_USER")
    smtp_password = wmill.get_variable("u/timoneway/SMTP_PASSWORD")
    recipient_email = wmill.get_variable("u/timoneway/RECIPIENT_EMAIL")

    if not all([smtp_user, smtp_password, recipient_email]):
        raise RuntimeError(f"Missing SMTP environment variables: {[k for k, v in {'SMTP_USER': smtp_user, 'SMTP_PASSWORD': smtp_password, 'RECIPIENT_EMAIL': recipient_email}.items() if not v]}")

    script_content = script_result.get('script', 'No script generated')
    msg = MIMEText(f"New Podcast Script Generated\n\n{script_content}\n\nStatus: {script_result.get('status', 'Unknown')}")
    msg["Subject"] = f"Podcast Script Run - {datetime.now(UTC).isoformat()}"
    msg["From"] = smtp_user
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, recipient_email, msg.as_string())
        return {"status": "Notification sent"}
    except Exception as e:
        raise RuntimeError(f"Failed to send notification: {str(e)}")
#!/usr/bin/env python3
import argparse
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_email, subject, body_html, smtp_config=None):
    if not smtp_config:
        print(f"--- [EMAIL SIMULATION] TO: {to_email} ---")
        print(f"Subject: {subject}")
        print(f"Body: {body_html}")
        return True

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_config.get("from", "lemino.production@antigravity.ai")
    msg["To"] = to_email
    msg.attach(MIMEText(body_html, "html"))

    host = smtp_config.get("host", "smtp.gmail.com")
    port = smtp_config.get("port", 587)
    user = smtp_config.get("user")
    password = smtp_config.get("password")

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        if user and password:
            server.login(user, password)
        server.send_message(msg)
    print(f"Email successfully sent to {to_email}!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send episode completion email")
    parser.add_argument("--to", required=True, help="Recipient email")
    parser.add_argument("--episode", required=True, help="Episode number / title")
    parser.add_argument("--link", required=True, help="Google Drive link")
    args = parser.parse_args()

    html = f"""
    <h2>🎬 LEMiNO Documentary Production Completed!</h2>
    <p>สารคดีสืบสวนตอนใหม่ได้รับการผลิตและเรนเดอร์เสร็จสมบูรณ์เรียบร้อยแล้ว:</p>
    <ul>
      <li><b>Episode:</b> {args.episode}</li>
      <li><b>Status:</b> Rendered 1080p 30fps & Uploaded to Google Drive</li>
      <li><b>Google Drive Link:</b> <a href="{args.link}">{args.link}</a></li>
    </ul>
    """
    send_email(args.to, f"[LEMiNO Production] Finished: {args.episode}", html)

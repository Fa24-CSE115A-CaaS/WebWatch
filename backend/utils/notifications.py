import os, smtplib, ssl, requests, json
from dotenv import load_dotenv
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_mail(subject: str, message: str, recipients: list[str]):
    load_dotenv()

    smtp_server = os.getenv("EMAIL_SERVER")
    smtp_port = int(os.getenv("EMAIL_PORT"))
    sender_email = os.getenv("EMAIL_FROM")
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")

    formatted_sender = formataddr(("WebWatch", sender_email))

    recipientsString = ""
    for s in recipients:
        recipientsString = recipientsString + s + " "

    msg = MIMEMultipart()
    msg["From"] = formatted_sender
    msg["To"] = recipientsString
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP(smtp_server, port=smtp_port) as server:
        server.ehlo()
        server.starttls(context=ssl.create_default_context())
        server.login(username, password)
        server.sendmail(sender_email, recipientsString, msg.as_string())
        server.quit()


def send_discord_msg(webhook_url, message):
    payload = {
        "username": "WebWatch",
        "avatar_url": "https://cdn.discordapp.com/icons/1290530538226061385/5cc1bbbc655fa34f00b1d8c02bd1e9a4.webp?size=1024",
        "embeds": [
            {
                "author": {
                    "name": "WebWatch",
                    "icon_url": "https://cdn.discordapp.com/icons/1290530538226061385/5cc1bbbc655fa34f00b1d8c02bd1e9a4.webp?size=1024",
                    "url": "https://webwatch.live",
                },
                "description": message,
                "color": 0x00b0f4,
                "footer": {"text": "WebWatch.live"},
                "timestamp": datetime.utcnow().isoformat(),
            }
        ],
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    response.raise_for_status()

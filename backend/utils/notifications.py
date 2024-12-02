import os, smtplib, ssl, requests, json, time
from dotenv import load_dotenv
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_mail(subject: str, message: str, recipients: list[str]):
    message = str(message)
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


def send_discord_msg(webhook_url, message, retries=5):
    headers = {"Content-Type": "application/json"}
    while message:
        chunk = message[:2048]
        message = message[2048:]
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
                    "description": chunk,
                    "color": 0x00B0F4,
                    "footer": {"text": "WebWatch.live"},
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ],
        }

        for attempt in range(retries):
            try:
                response = requests.post(
                    webhook_url, data=json.dumps(payload), headers=headers
                )
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                if attempt < retries - 1:
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(1.1 ** attempt)  # Exponential backoff
                else:
                    print(f"All {retries} attempts failed: {e}")
                    raise


def send_password_reset_email(recipient_email: str, reset_link: str):
    reset_link = str(reset_link)
    load_dotenv()

    smtp_server = os.getenv("EMAIL_SERVER")
    smtp_port = int(os.getenv("EMAIL_PORT"))
    sender_email = os.getenv("EMAIL_FROM")
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")

    subject = "Email Login Link"
    body = f"""
    Hi,

    It looks like you've requested an email login link. Click the link below to log in:

    {reset_link}

    If you didn't request this, please ignore this email.

    Thanks!
    """

    formatted_sender = formataddr(("WebWatch", sender_email))

    message = MIMEMultipart()
    message["From"] = formatted_sender
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(username, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email login link sent successfully.")
    except Exception as e:
        print(f"Error sending email login link: {e}")

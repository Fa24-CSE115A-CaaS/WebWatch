import os, smtplib, ssl, requests
from dotenv import load_dotenv
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
    requests.post(webhook_url, data={"content": message})


def send_password_reset_email(recipient_email: str, reset_link: str):
    # Load environment variables
    load_dotenv()
    
    # Email server configuration from environment variables
    smtp_server = os.getenv("EMAIL_SERVER")
    smtp_port = int(os.getenv("EMAIL_PORT"))
    sender_email = os.getenv("EMAIL_FROM")
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")

    # Email content
    subject = "Password Reset Request"
    body = f"""
    Hi,

    It looks like you've requested to reset your password. Click the link below to reset it:

    {reset_link}

    If you didn't request this, please ignore this email.

    Thanks!
    """
    
    # Format sender name
    formatted_sender = formataddr(("WebWatch", sender_email))
    
    # Create the email message
    message = MIMEMultipart()
    message["From"] = formatted_sender
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    # Send the email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(username, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Password reset email sent successfully.")
    except Exception as e:
        print(f"Error sending password reset email: {e}")
import os, smtplib, ssl, requests
from dotenv import load_dotenv

def send_mail(subject: str, message: str, recipients: list[str]):
    load_dotenv()
    
    smtp_server = os.getenv('EMAIL_SERVER')
    smtp_port = os.getenv('EMAIL_PORT')
    sender_email = os.getenv('EMAIL_FROM')
    password = os.getenv('EMAIL_PASSWORD')

    msg = (f'Subject: {subject}\n\n{message}').encode('utf-8')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port=smtp_port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipients, msg)
        
        
def send_discord_msg(webhook_url, message):
    requests.post(webhook_url, data={"content": message})
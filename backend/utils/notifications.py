import os, smtplib, ssl, requests
from dotenv import load_dotenv
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(subject: str, message: str, recipients: list[str]):
    load_dotenv()
    
    smtp_server = os.getenv('EMAIL_SERVER')
    smtp_port = int(os.getenv('EMAIL_PORT'))
    sender_email = os.getenv('EMAIL_FROM')
    username = os.getenv('EMAIL_USERNAME')
    password = os.getenv('EMAIL_PASSWORD')

    formatted_sender = formataddr(('WebWatch', sender_email))

    recipientsString = ""
    for s in recipients:
        recipientsString = recipientsString + s + " "
    
    msg = MIMEMultipart()
    msg['From'] = formatted_sender
    msg['To'] = recipientsString
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port=smtp_port, context=context) as server:
        server.login(username, password)
        server.sendmail(sender_email, recipientsString, msg.as_string())
        server.quit()
        
        
def send_discord_msg(webhook_url, message):
    requests.post(webhook_url, data={"content": message})
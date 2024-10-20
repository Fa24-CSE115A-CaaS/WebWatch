import os, smtplib, ssl, requests

def send_mail(subject: str, message: str, recipients: list[str]):
    smtp_server = "smtp.gmail.com"
    sender_email = os.getenv('MAIL_EMAIL')
    password = os.getenv('MAIL_PASSWORD')
    msg = f'Subject: {subject}\n\n{message}'

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port=465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipients, msg)
        
        
def send_discord_msg(webhook_url, message):
    requests.post(webhook_url, data={"content": message})
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.helpers.config import config


def send_mail(to: str, subject: str, text: str):
    smtp = smtplib.SMTP_SSL(config.smtp_host, config.smtp_port)
    smtp.ehlo()
    smtp.login(config.smtp_user, config.smtp_password)

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = config.smtp_from
    message["To"] = to

    html_part = MIMEText(text, "html")
    message.attach(html_part)
    smtp.sendmail(config.smtp_from, to, message.as_string())
    smtp.quit()

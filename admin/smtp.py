"""Function send an email with the opportunity to attach a file. Return True if the email is sent"""
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import Logger
from typing import Optional

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')


def send_email(subject: str = 'TelegramBot',
               message: str = 'Message from telegrambot. ',
               file: str = '../logconfig.log',
               attach_file: bool = True,
               logger: Optional[Logger] = None) -> bool:
    """Send an email with the opportunity to attach a file. Return True if the email is sent

    :param subject: Subject of email. Defaults to 'TelegramBot'.
    :type subject: str, optional
    :param message: Message of email. Defaults to 'Message from telegrambot. '.
    :type message: str, optional
    :param file: Path to attach file if existed. Defaults to '../logconfig.log'.
    :type file: str, optional
    :param attach_file: True if attach file to email exist. Defaults to True.
    :type attach_file: bool, optional
    :param logger: Logger. Defaults to None.
    :type logger: Logger, optional

    :return: True if the email is sent, False if not.
    :rtype: bool
    """
    status: bool = False
    msg = MIMEMultipart()

    msg['From'] = EMAIL_SENDER
    password = EMAIL_PASSWORD
    msg['To'] = EMAIL_RECIPIENT
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    if attach_file:
        try:
            part = MIMEBase('application', 'octet-stream')
            with open(file, 'rb') as file:
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename={}'.format('logconfig.log'))
            msg.attach(part)
        except FileNotFoundError as e:
            logger.exception(f'Error attach file: {str(e)}')
            msg.attach(MIMEText(f'Error attach file: {str(e)}', 'plain'))
    try:
        with smtplib.SMTP('smtp.gmail.com: 587') as smtp:
            # with smtplib.SMTP_SSL('smtp.gmail.com: 465') as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_SENDER, password)
            smtp.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
            logger.info(f'Email send to {EMAIL_RECIPIENT}')
            status = True

    except (smtplib.SMTPAuthenticationError, smtplib.SMTPSenderRefused, smtplib.SMTPRecipientsRefused,
            smtplib.SMTPConnectError, TimeoutError) as e:
        logger.exception(f'Error send email: {str(e)}')

    return status


if __name__ == '__main__':
    send_email()

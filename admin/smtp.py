import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from create import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT
from admin.logsetting import logger


def send_email(subject='TelegramBot',
               message='Message from telegrambot. ',
               file='../logconfig.log',
               attach_file=True) -> bool:
    """Send an email with the opportunity to attach a file. Return True if the email is sent"""
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

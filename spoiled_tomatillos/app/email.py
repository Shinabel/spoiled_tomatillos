from flask_mail import Message
import logging
from app import app, mail

def send_email(to, subject, template):
    #logging.info("Sending email to: {} \n Using template: ")
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

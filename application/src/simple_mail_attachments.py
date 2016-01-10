__author__ = 'shishir'

import os
import smtplib
from application.config.email_config import MailConfig
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


class Email(object):

    def __init__(self, smtp_host=None, smtp_port=None, user=None, password=None):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.user = user
        self.password = password
        self.msg = MIMEMultipart()

    def send(self, subject=None, _from=None, to=None, text_msg=None, attachments=None):
        assert _from is not None
        assert to is not None
        try:
            server = smtplib.SMTP()
            server.connect(self.smtp_host, self.smtp_port)
            server.ehlo()
            server.starttls()
            self.msg['Subject'] = subject
            server.login(self.user, self.password)
            self._build_email_body(text_msg=text_msg, attachments=attachments)
            server.sendmail(_from, to, self.msg.as_string())
        except smtplib.SMTPException:
            raise
        finally:
            server.quit()

    def _build_email_body(self, text_msg='', attachments=None):
        self.msg.attach(MIMEText(text_msg))
        if attachments is not None:
            self._attach_files(attachments=attachments)

    def _attach_files(self, attachments=None):
        for path in attachments:
            try:
                fp = open(path, 'rb')
                file_name = os.path.basename(path)
                file_type = file_name.split(".").pop()
                attachment = MIMEImage(fp.read()) if file_type in ['jpg'] else MIMEText(fp.read())
                attachment.add_header("Content-Disposition", "attachment", filename=file_name)
                self.msg.attach(attachment)
                fp.close()
            except:
                raise


def bootstrap():
    email = Email(smtp_host=MailConfig.smtp_host,
                  smtp_port=MailConfig.smtp_port,
                  user=MailConfig.user,
                  password=MailConfig.password)

    email.send(subject='Email Reporting - TEST EMAIL',
               _from='XXXX@gmail.com',
               to=['XXXX@gmail.com'],
               text_msg="Email Reporting - TEST EMAIL",
               attachments=['C:\working\\attachment.txt',
                            'C:\working\input.txt',
                            'C:\working\did it.jpg',
                            'C:\working\pandas_tut.csv'])

bootstrap()
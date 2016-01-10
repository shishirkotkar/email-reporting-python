__author__ = 'shishir'

import os
import smtplib
import jinja2
from application.config.email_config import MailConfig, TABLE_TEMPLATE, TEMPLATES_DIR
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_DIR))


class Email(object):
    def __init__(self, smtp_host=None, smtp_port=None, user=None, password=None):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.user = user
        self.password = password
        self.msg = MIMEMultipart('alternative')

    def send(self, subject=None, _from=None, to=None, text_msg=None, attachments=None, table=None):
        assert _from is not None
        assert to is not None
        try:
            server = smtplib.SMTP()
            server.connect(self.smtp_host, self.smtp_port)
            server.ehlo()
            server.starttls()
            server.login(self.user, self.password)
            self.msg['Subject'] = subject
            self._build_email_body(text_msg=text_msg, attachments=attachments, table=table)
            server.sendmail(_from, to, self.msg.as_string())
        except smtplib.SMTPException:
            raise

    def _build_email_body(self, text_msg='', attachments=None, table=None):
        self.msg.attach(MIMEText(text_msg, 'plain'))
        if table is not None:
            self._build_table(text_msg=text_msg, table=table)
        if attachments is not None:
            self._attach_files(attachments=attachments)

    def _build_table(self, text_msg, table=None):
        try:
            template = JINJA_ENVIRONMENT.get_template(TABLE_TEMPLATE)
            template_variables = {"text_message": text_msg, "data": table['data'], "header": table['header']}
            rendered_html = template.render(template_variables)
            self.msg.attach(MIMEText(rendered_html, 'html'))
        except:
            raise

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

    # Sample Data
    table_data = [(12.34, 17.234, 3.00, 1234.67), ("India", "Now York", "Goa", "Tokyo")]
    header = ("Americas", "Brazil", "London", "Costa Rica")
    table = {'header': header, 'data': table_data}

    email.send(subject="Email Reporting - HTML TABLE TEST",
               _from='XXXX@gmail.com',
               to=['XXXX@gmail.com'],
               text_msg="Email Reporting - HTML TABLE TEST",
               table=table)


bootstrap()
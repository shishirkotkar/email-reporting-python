__author__ = 'shishir'

import os


class MailConfig(object):
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    user = 'XXXX@gmail.com'
    password = 'XXXX' # yeah - please use encryption!!

TEMPLATES_DIR = os.path.realpath("templates")
TABLE_TEMPLATE = 'table.jinja'

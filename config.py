import os.path

from dotenv import dotenv_values

from utils.utils import check_folder_accessibility

config = dotenv_values('.env')
EMAIL_LOGIN = config['EMAIL_LOGIN']
EMAIL_PASSWORD = config['EMAIL_PASSWORD']

SMTP_SERVER = 'smtp.yandex.ru'

SMTP_PORT = 465

# Куда отправлять Email:
SEND_EMAIL_TO = ('itexpert_mailing_list@itexpert.ru',)
# SEND_EMAIL_TO = ('g.savushkin@itexpert.ru',)

#    *.txt файлы на Server
DIR_TXT = os.path.join('//', '192.168.20.100', 'Administrative server', 'ДНИ РОЖДЕНИЯ СОТРУДНИКОВ')
IGNORE_FILE = os.path.join(DIR_TXT, 'ignore.txt')

if not check_folder_accessibility(DIR_TXT):
    raise f'{check_folder_accessibility(DIR_TXT)}'

SYSTEM_LOG = './system_log.txt'
LOG = './log.txt'

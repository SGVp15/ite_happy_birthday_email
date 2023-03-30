from dotenv import dotenv_values


config = dotenv_values('.env')
EMAIL_LOGIN = config['EMAIL_LOGIN']
EMAIL_PASSWORD = config['EMAIL_PASSWORD']

# Куда отправлять Email:
SEND_EMAIL_TO = ('ite@itexpert.ru',)

# Где хрянятся txt файлы на Server
DIR_TXT = '//server/Administrative server/РАБОТА СЕКРЕТАРЯ/СОТРУДНИКИ/Дни рождения сотрудников из 1C/'


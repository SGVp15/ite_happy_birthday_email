import base64
import os
import random
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import dotenv_values

from config import SMTP_SERVER, SMTP_PORT

config = dotenv_values('./.env')
EMAIL_LOGIN = config['EMAIL_LOGIN']
EMAIL_PASSWORD = config['EMAIL_PASSWORD']


def get_random_image(path):
    all_image = os.listdir(path)
    r = random.choice(all_image)
    return f'{path}{r}'


def get_random_congratulation(path='./congratulation.txt'):
    with open(path, encoding='utf-8', mode='r') as f:
        s = f.read()
    rows = s.split('\n')
    while True:
        row = random.choice(rows).strip()
        if len(row) > 10:
            return row


def send_email_happy_birthday(send_to, user):
    msg = MIMEMultipart("alternative")
    msg['From'] = EMAIL_LOGIN
    msg['Subject'] = f'Сегодня празднует день рождения {user.last_name} {user.first_name} &#129395;'
    msg['To'] = ';'.join(send_to)

    path = './images/'
    with open(get_random_image(path), mode='rb') as f:
        s = f.read()
    base64_file = base64.b64encode(s)
    base64_file = base64_file.decode("utf-8")

    html = f"""
    <html>
      <body>
        <p style="color:black; font-family:'arial',sans-serif;">
            &#127881;
            <em>Сегодня свой день рождения отмечает {user.first_name} {user.last_name}</em> &#129395;<br>
            <em>{get_random_congratulation()}</em> &#10024;
        </p>
        
        <img src="data:image/jpg;base64,{base64_file}" width="320" />
        
        <p style="color:black; font-family:'arial',sans-serif; font-size:10pt">
            С заботой и наилучшими пожеланиями,<br>
            Команда IT Expert &#129293;<br>
            <img src="https://itexpert.ru/local/templates/kennet/img/main-logo.svg#9993" width="120">
        </p>
            
        
      </body>
    </html>"""

    msg.attach(MIMEText(html, "html"))
    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

    smtp.set_debuglevel(True)
    smtp.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    smtp.send_message(msg)
    smtp.quit()
    print(f'{user.last_name} {user.first_name} - Письмо отправлено!^_^')
    time.sleep(1)

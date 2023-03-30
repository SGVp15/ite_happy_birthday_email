import base64
import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import dotenv_values


config = dotenv_values('./.env')
EMAIL_LOGIN = config['EMAIL_LOGIN']
EMAIL_PASSWORD = config['EMAIL_PASSWORD']


def get_random_image(path):
    all_image = os.listdir(path)
    r = random.choice(all_image)
    return f'{path}{r}'


def send_email_happy_birthday(send_to, user):
    msg = MIMEMultipart("alternative")
    msg['From'] = EMAIL_LOGIN
    msg['Subject'] = f'Сегодня празднует день рождения {user.last_name} {user.first_name}!'
    msg['To'] = ';'.join(send_to)

    if user.is_woman:
        path = './images/woman/'
    else:
        path = './images/man/'

    with open(get_random_image(path), mode='rb') as f:
        s = f.read()
    base64_file = base64.b64encode(s)
    base64_file = base64_file.decode("utf-8")

    html = f"""
    <html>
      <body>
        <p style="color:red; font-family:'arial',sans-serif; font-size:16pt">
        {user.last_name} {user.first_name}! Поздравляем с Днем Рождения!</p>
        <img src="data:image/jpg;base64,{base64_file}" width="600" />
        <p style="color:blue; font-family:'arial',sans-serif; font-size:16pt">С уважением IT Expert.</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    smtp = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    smtp.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    smtp.send_message(msg)
    smtp.quit()
    print(f'{user.last_name} {user.first_name} - Письмо отправлено!^_^')

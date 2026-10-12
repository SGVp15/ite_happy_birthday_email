import base64
import logging
import os
import random
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import dotenv_values

from config import SMTP_SERVER, SMTP_PORT

config = dotenv_values('./.env')
EMAIL_LOGIN = config.get('EMAIL_LOGIN')
EMAIL_PASSWORD = config.get('EMAIL_PASSWORD')


def get_random_image(path='./images/'):
    try:
        all_image = os.listdir(path)
        if not all_image:
            raise FileNotFoundError(f"Папка с изображениями пуста: {path}")
        r = random.choice(all_image)
        full_path = os.path.join(path, r)
        return full_path
    except Exception as e:
        logging.error(f"Ошибка при выборе случайного изображения из {path}: {e}")
        raise


def get_random_congratulation(path='./congratulation.txt'):
    try:
        with open(path, encoding='utf-8', mode='r') as f:
            s = f.read()
        rows = s.split('\n')
        while True:
            row = random.choice(rows).strip()
            if len(row) > 10:
                return row
    except Exception as e:
        logging.error(f"Ошибка при чтении файла поздравлений {path}: {e}")
        return "С днем рождения!"

path = './images/'


def send_email_happy_birthday(send_to, user):
    user_fullname = f"{getattr(user, 'last_name', '')} {getattr(user, 'first_name', '')}".strip()
    logging.info(f"Подготовка к отправке письма для пользователя: {user_fullname}")

    try:
        msg = MIMEMultipart("alternative")
        msg['From'] = EMAIL_LOGIN
        msg['Subject'] = f'Сегодня празднует день рождения {user_fullname} &#129395;'

        if isinstance(send_to, list):
            msg['To'] = ';'.join(send_to)
        else:
            msg['To'] = send_to

        base64_file = encode_image_to_base64(get_random_image())

        congratulation_text = get_random_congratulation()

        html = f"""
        <html>
          <body>
            <p style="color:black; font-family:'arial',sans-serif;">
                &#127881;
                <em>Сегодня свой день рождения отмечает {getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}</em> &#129395;<br>
                <em>{congratulation_text}</em> &#10024;
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

        logging.debug(f"Подключение к SMTP-серверу {SMTP_SERVER}:{SMTP_PORT}...")
        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        smtp.set_debuglevel(0)  # Установите 1, если нужен отладочный вывод smtplib в консоль

        smtp.login(EMAIL_LOGIN, EMAIL_PASSWORD)
        smtp.send_message(msg)
        time.sleep(1)
        smtp.quit()

        logging.info(f"Письмо успешно отправлено для: {user_fullname}")
        print(f'{user_fullname} - Письмо отправлено!^_^')

    except Exception as e:
        logging.error(f"Не удалось отправить письмо для {user_fullname}: {e}")
        raise

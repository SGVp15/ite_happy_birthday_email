import datetime
from utils.log import log
import os
import re

from Contact.Contact import Contact
from Email.send_email import send_email_happy_birthday
from config import DIR_TXT, SEND_EMAIL_TO, IGNORE_FILE, LOG


def is_birthday_today(birthday_month: int, birthday_day: int):
    return birthday_day == datetime.datetime.now().day and birthday_month == datetime.datetime.now().month


def get_all_users_from_txt(filename, encoding='utf-8'):
    contacts = []
    with open(file=filename, mode='r', encoding=encoding) as f:
        s = f.read()
    rows = s.split('\n')
    for row in rows:
        try:
            birthday = re.findall(r'\s*(\d{2}.\d{2}.\d{4})', row)[0]
            name = re.findall(r'([А-Яа-я ]+)', row)[0]
            contacts.append(Contact(name, birthday=birthday))
        except (IndexError,):
            pass
    log.debug(f"Успешно прочитано контактов из файла {filename}: {len(contacts)}")
    return contacts


def is_contact_a_woman(name: str, women_list: list) -> bool:
    for name in name.split():
        if name in women_list:
            return True
    return False


if __name__ == '__main__':
    log.info("Скрипт проверки дней рождений запущен.")

    if not os.path.exists(DIR_TXT) or not os.path.isdir(DIR_TXT):
        log.critical(f"Критическая ошибка: Папка с днями рождения недоступна или не существует: {DIR_TXT}")
        exit(1)

    try:
        txt_files = set([x for x in os.listdir(DIR_TXT) if x.endswith('.txt')])
        log.info(f"Найдено текстовых файлов в папке: {len(txt_files)}")
    except Exception as e:
        log.critical(f"Ошибка при сканировании папки {DIR_TXT}: {e}")
        exit(1)

    all_users = []
    for file in txt_files:
        file_path = os.path.join(DIR_TXT, file)
        try:
            all_users.extend(get_all_users_from_txt(filename=file_path, encoding='1251'))
        except (IOError, UnicodeDecodeError):
            try:
                all_users.extend(get_all_users_from_txt(filename=file_path))
            except Exception as e:
                log.error(f"Не удалось прочитать файл {file}: {e}")

    ignore_users = []
    if os.path.exists(IGNORE_FILE):
        try:
            ignore_users.extend(get_all_users_from_txt(filename=IGNORE_FILE, encoding='1251'))
        except UnicodeDecodeError:
            ignore_users.extend(get_all_users_from_txt(filename=IGNORE_FILE))
        except Exception as e:
            log.error(f"Ошибка при чтении ignore-файла: {e}")

        all_users = [user for user in all_users if user not in ignore_users]
        log.info(f"Исключено пользователей из списка игнорирования: {len(ignore_users)}")

    birthday_users = [user for user in all_users if is_birthday_today(birthday_month=user.month, birthday_day=user.day)]

    # Удаление дубликатов
    users: [Contact] = []
    for user in birthday_users:
        if user not in users:
            users.append(user)

    log.info(f"Именинников сегодня: {len(users)}")

    try:
        with open(LOG, encoding='utf-8', mode='a') as f:
            f.write(f'{datetime.datetime.now()} run - ok\n')
            for user in users:
                try:
                    send_email_happy_birthday(send_to=SEND_EMAIL_TO, user=user)
                    f.write(str(user) + '\n')
                    log.info(f"Отправлено поздравление для: {user}")
                except Exception as e:
                    log.error(f"Ошибка при отправке письма для {user}: {e}")
    except Exception as e:
        log.error(f"Ошибка записи в локальный log.txt: {e}")

    log.info("Скрипт успешно завершил работу.")

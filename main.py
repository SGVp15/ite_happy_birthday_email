import datetime
import os
import re

from Contact.Contact import Contact
from Email.send_email import send_email_happy_birthday
from config import DIR_TXT, SEND_EMAIL_TO, IGNORE_FILE


def is_birthday_today(birthday_month: int, birthday_day: int):
    return birthday_day == datetime.datetime.now().day and birthday_month == datetime.datetime.now().month


def get_all_users_from_txt(filename, encoding='utf-8'):
    contacts = []
    with open(file=filename, mode='r', encoding=encoding) as f:
        s = f.read()
        s = re.sub(r' {2,}', '\t', s)
        rows = s.split('\n')
        for s in rows:
            try:
                name = re.findall(r'^([А-Яа-я ]+)\t', s)[0]
                birthday = re.findall(r'\t(\d{2}.\d{2}.\d{4})', s)[0]
                is_woman = is_contact_a_woman(name, women)
                contacts.append(Contact(name, birthday=birthday, is_woman=is_woman))
            except (IndexError,):
                pass
    return contacts


def is_contact_a_woman(name: str, women_list: list) -> bool:
    for name in name.split():
        if name in women_list:
            return True
    return False


if __name__ == '__main__':
    with open('./Contact/women.txt', encoding='utf-8', mode='r') as f:
        women = f.read().split('\n')

    txt = set([x for x in os.listdir(DIR_TXT) if x.endswith('.txt')])

    all_users = []
    for file in txt:
        try:
            all_users.extend(get_all_users_from_txt(filename=os.path.join(DIR_TXT, file), encoding='1251'))
        except (IOError, UnicodeDecodeError):
            all_users.extend(get_all_users_from_txt(filename=os.path.join(DIR_TXT, file)))

    ignore_users = []
    if os.path.exists(IGNORE_FILE):
        try:
            ignore_users.extend(get_all_users_from_txt(filename=IGNORE_FILE, encoding='1251'))
        except UnicodeDecodeError:
            ignore_users.extend(get_all_users_from_txt(filename=IGNORE_FILE))

        all_users = [user for user in all_users if user not in ignore_users]

    # Удаление дубликатов
    send_email = [user for user in all_users if is_birthday_today(birthday_month=user.month, birthday_day=user.day)]

    users: [Contact] = []
    for user in send_email:
        if user not in users:
            users.append(user)

    with open('./log.txt', encoding='utf-8', mode='a') as f:
        f.write(f'{datetime.datetime.now()} run - ok\n')
        for user in users:
            print(user)
            send_email_happy_birthday(send_to=SEND_EMAIL_TO, user=user)
            f.write(str(user))

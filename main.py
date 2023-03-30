import datetime
import os
import re

from Contact.Contact import Contact
from Email.send_email import send_email_happy_birthday
from config import DIR_TXT, SEND_EMAIL_TO


def is_birthday_today(birthday_month: int, birthday_day: int):
    return birthday_day == datetime.datetime.now().day and birthday_month == datetime.datetime.now().month


# def get_all_users_from_excel(filename):
#     with open('./Contact/women.txt', encoding='utf-8', mode='r') as f:
#         women = f.read().split('\n')
#
#     excel = load_workbook(filename=filename, data_only=True)
#     sheet_ranges = excel[LIST_NAME]
#     contacts = []
#     for row in range(10, 100):
#         try:
#             name = str(sheet_ranges[f'{NAME_COLUMN}{row}'].value)
#             birthday = str(sheet_ranges[f'{BIRTHDAY_COLUMN}{row}'].value)
#             is_woman = is_contact_a_woman(name, women)
#             contacts.append(Contact(name, birthday=birthday, is_woman=is_woman))
#         except:
#             pass
#     return contacts


def get_all_users_from_csv(filename):
    contacts = []
    with open(file=filename, mode='r', encoding='1251') as f:
        s = f.read()
        rows = s.split('\n')
        for s in rows:
            try:
                name = re.findall(r'^([А-Яа-я ]+)\t', s)[0]
                birthday = re.findall(r'\t(\d{2}.\d{2}.\d{4})', s)[0]
                is_woman = is_contact_a_woman(name, women)
                contacts.append(Contact(name, birthday=birthday, is_woman=is_woman))
            except:
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
        all_users.extend(get_all_users_from_csv(filename=DIR_TXT + file))

    # Удаление дубликатов
    users = []
    for user in all_users:
        if user not in users:
            users.append(user)

    # Проверка если сегодня др
    for user in users:
        if is_birthday_today(user.month, user.day):
            send_email_happy_birthday(send_to=SEND_EMAIL_TO, user=user)

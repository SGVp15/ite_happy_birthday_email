class Contact:
    def __init__(self, name: str, birthday: str, is_woman=False):
        self.word = name.split(' ')
        self.first_name = self.word[1]
        self.last_name = self.word[0]
        self.is_woman = is_woman
        self.birthday = birthday.strip()
        day_month = self.birthday.split('.')
        self.day = int(day_month[0])
        self.month = int(day_month[1])

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.is_woman} {self.birthday}'

    def __repr__(self):
        return f'Name = [{self.last_name} {self.first_name}] [Is woman = {self.is_woman}] [Birthday = {self.birthday}]'

    def __eq__(self, other):
        if (
                self.first_name == other.first_name
                and self.first_name == other.first_name
                and self.birthday == other.birthday
        ):
            return True
        return False

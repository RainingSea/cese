from datetime import datetime

class AgeCalculator:
    def __init__(self, birthdate: str):
        self.birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
        self.current_date = datetime.now()

    def calculate_age(self) -> str:
        age = self.current_date.year - self.birthdate.year
        if (self.current_date.month, self.current_date.day) < (self.birthdate.month, self.birthdate.day):
            age -= 1
        return str(age)

    def days_until_next_birthday(self) -> int:
        next_birthday = datetime(self.current_date.year, self.birthdate.month, self.birthdate.day)
        if next_birthday < self.current_date:
            next_birthday = datetime(self.current_date.year + 1, self.birthdate.month, self.birthdate.day)
        return (next_birthday - self.current_date).days

    def save_birthdate(self) -> None:
        with open('birthdates.txt', 'a') as file:
            file.write(self.birthdate.strftime('%Y-%m-%d') + '\n')
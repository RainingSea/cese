import os
from datetime import datetime

class BirthdateManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_birthdates(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def save_birthdate(self, birthdate: str):
        with open(self.file_path, 'a') as file:
            file.write(birthdate + '\n')

    def calculate_age(self, birthdate: str) -> tuple:
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        age_years = today.year - birthdate.year
        age_months = today.month - birthdate.month
        age_days = today.day - birthdate.day

        if age_days < 0:
            age_months -= 1
            age_days += (birthdate.replace(year=today.year, month=today.month) - 
                         birthdate.replace(year=today.year, month=today.month - 1)).days

        if age_months < 0:
            age_years -= 1
            age_months += 12

        return age_years, age_months, age_days

    def days_until_next_birthday(self, birthdate: str) -> int:
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        next_birthday = birthdate.replace(year=today.year)

        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)

        return (next_birthday - today).days
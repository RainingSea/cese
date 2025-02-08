from datetime import datetime
import os

class AgeCalculator:
    def __init__(self, birthdate: str):
        self.birthdate = datetime.strptime(birthdate, '%Y-%m-%d')

    def calculate_age(self) -> dict:
        today = datetime.today()
        age_years = today.year - self.birthdate.year
        age_months = today.month - self.birthdate.month
        age_days = today.day - self.birthdate.day

        if age_days < 0:
            age_months -= 1
            age_days += (self.birthdate.replace(month=self.birthdate.month + 1, day=1) - self.birthdate.replace(month=self.birthdate.month, day=1)).days

        if age_months < 0:
            age_years -= 1
            age_months += 12

        return {'years': age_years, 'months': age_months, 'days': age_days}

    def days_until_next_birthday(self) -> int:
        today = datetime.today()
        next_birthday = self.birthdate.replace(year=today.year)

        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)

        return (next_birthday - today).days

    def save_birthdate(self) -> None:
        with open('users_data.txt', 'a') as file:
            file.write(f"{self.birthdate.strftime('%Y-%m-%d')}\n")
from datetime import datetime
import os

class AgeCalculator:
    def __init__(self, birthdate: str):
        self.birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        self.age_years = 0
        self.age_months = 0
        self.age_days = 0
        self.days_until_birthday = 0
        self.calculate_age()

    def calculate_age(self) -> None:
        today = datetime.today()
        self.age_years = today.year - self.birthdate.year
        self.age_months = today.month - self.birthdate.month
        self.age_days = today.day - self.birthdate.day

        if self.age_days < 0:
            self.age_months -= 1
            self.age_days += (self.get_days_in_month(today.month - 1, today.year) if today.month > 1 else self.get_days_in_month(12, today.year - 1))

        if self.age_months < 0:
            self.age_years -= 1
            self.age_months += 12

    def days_until_next_birthday(self) -> None:
        today = datetime.today()
        next_birthday = datetime(today.year, self.birthdate.month, self.birthdate.day)

        if today > next_birthday:
            next_birthday = datetime(today.year + 1, self.birthdate.month, self.birthdate.day)

        self.days_until_birthday = (next_birthday - today).days

    def store_birthdate(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.birthdate.strftime('%Y-%m-%d')}\n")

    def display_age(self) -> str:
        return f"Age: {self.age_years} years, {self.age_months} months, {self.age_days} days"

    def display_days_until_birthday(self) -> str:
        self.days_until_next_birthday()
        return f"Days until next birthday: {self.days_until_birthday}"

    @staticmethod
    def get_days_in_month(month: int, year: int) -> int:
        if month == 2:
            return 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31
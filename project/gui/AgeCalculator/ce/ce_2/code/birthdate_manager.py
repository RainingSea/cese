from datetime import datetime, timedelta
import os

class BirthdateManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.birthdates = []

    def load_birthdates(self) -> list:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r") as file:
            return [line.strip() for line in file.readlines()]

    def save_birthdate(self, birthdate: str) -> None:
        with open(self.file_path, "a") as file:
            file.write(birthdate + "\n")

    def calculate_age(self, birthdate: str, current_date: datetime) -> tuple:
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        age_years = current_date.year - birthdate.year
        age_months = current_date.month - birthdate.month
        age_days = current_date.day - birthdate.day

        if age_days < 0:
            age_months -= 1
            age_days += (birthdate.replace(year=current_date.year, month=current_date.month) - timedelta(days=1)).day

        if age_months < 0:
            age_years -= 1
            age_months += 12

        return age_years, age_months, age_days

    def days_until_next_birthday(self, birthdate: str, current_date: datetime) -> int:
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        next_birthday = birthdate.replace(year=current_date.year)

        if next_birthday < current_date:
            next_birthday = next_birthday.replace(year=current_date.year + 1)

        return (next_birthday - current_date).days

    def validate_birthdate(self, birthdate: str) -> bool:
        try:
            datetime.strptime(birthdate, "%Y-%m-%d")
            return True
        except ValueError:
            return False
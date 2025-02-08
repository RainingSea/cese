from datetime import datetime
import os

class AgeCalculator:
    def __init__(self):
        self.birthdate = ""

    def set_birthdate(self, birthdate: str) -> None:
        self.birthdate = birthdate

    def calculate_age(self) -> str:
        birthdate_obj = datetime.strptime(self.birthdate, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birthdate_obj.year - ((today.month, today.day) < (birthdate_obj.month, birthdate_obj.day))
        return f"You are {age} years old."

    def days_until_next_birthday(self) -> int:
        birthdate_obj = datetime.strptime(self.birthdate, "%Y-%m-%d")
        today = datetime.today()
        next_birthday = datetime(today.year, birthdate_obj.month, birthdate_obj.day)
        if next_birthday < today:
            next_birthday = datetime(today.year + 1, birthdate_obj.month, birthdate_obj.day)
        return (next_birthday - today).days

    def save_birthdate(self) -> None:
        with open("birthdates.txt", "a") as file:
            file.write(f"{self.birthdate}\n")
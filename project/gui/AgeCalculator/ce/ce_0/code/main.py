import tkinter as tk
from datetime import datetime

class Main:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Age Calculator")
        
        self.instruction_label = tk.Label(self.window, text="Enter your birthdate (YYYY-MM-DD):")
        self.instruction_label.pack()

        self.birthdate_entry = tk.Entry(self.window)
        self.birthdate_entry.pack()

        self.submit_button = tk.Button(self.window, text="Submit", command=self.main)
        self.submit_button.pack()

        self.age_label = tk.Label(self.window, text="")
        self.age_label.pack()

        self.days_until_birthday_label = tk.Label(self.window, text="")
        self.days_until_birthday_label.pack()

        self.window.mainloop()

    def main(self):
        birthdate = self.birthdate_entry.get()
        self.save_birthdate(birthdate)
        age = self.calculate_age(birthdate)
        days_until_birthday = self.days_until_next_birthday(birthdate)

        self.age_label.config(text=age)
        self.days_until_birthday_label.config(text=f"Days until next birthday: {days_until_birthday}")

    def calculate_age(self, birthdate: str) -> str:
        birthdate_date = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        
        age_years = today.year - birthdate_date.year
        age_months = today.month - birthdate_date.month
        age_days = today.day - birthdate_date.day

        if age_days < 0:
            age_months -= 1
            age_days += (birthdate_date.replace(year=today.year, month=today.month) - 
                          birthdate_date.replace(year=today.year, month=today.month - 1)).days

        if age_months < 0:
            age_years -= 1
            age_months += 12

        return f"Age: {age_years} years, {age_months} months, {age_days} days"

    def days_until_next_birthday(self, birthdate: str) -> int:
        birthdate_date = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        next_birthday = birthdate_date.replace(year=today.year)

        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)

        return (next_birthday - today).days

    def save_birthdate(self, birthdate: str) -> None:
        with open("birthdates.txt", "a") as file:
            file.write(birthdate + "\n")
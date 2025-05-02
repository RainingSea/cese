import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import os

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Age Calculator")
        
        self.birthdate_manager = BirthdateManager('birthdates.txt')
        self.load_birthdates()

        self.label = tk.Label(master, text="Enter your birthdate (YYYY-MM-DD):")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.submit_button = tk.Button(master, text="Calculate Age", command=self.calculate_age)
        self.submit_button.pack()

        self.clear_button = tk.Button(master, text="Clear", command=self.clear_fields)
        self.clear_button.pack()

        self.age_label = tk.Label(master, text="")
        self.age_label.pack()

        self.days_label = tk.Label(master, text="")
        self.days_label.pack()

    def calculate_age(self):
        birthdate_str = self.entry.get()
        try:
            years, months, days = DateUtils.calculate_age(birthdate_str, datetime.today())
            days_until_birthday = DateUtils.days_until_next_birthday(birthdate_str, datetime.today())
            self.age_label.config(text=f"Age: {years} years, {months} months, {days} days")
            self.days_label.config(text=f"Days until next birthday: {days_until_birthday}")
            self.birthdate_manager.save_birthdate(birthdate_str)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date, please enter a valid date.")

    def clear_fields(self):
        self.entry.delete(0, tk.END)
        self.age_label.config(text="")
        self.days_label.config(text="")

    def load_birthdates(self):
        birthdates = self.birthdate_manager.load_birthdates()
        for birthdate in birthdates:
            self.entry.insert(tk.END, birthdate)

class BirthdateManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_birthdates(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def save_birthdate(self, birthdate):
        with open(self.file_path, 'a') as file:
            file.write(f"{birthdate}\n")

class DateUtils:
    @staticmethod
    def calculate_age(birthdate: str, reference_date: datetime) -> tuple:
        birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d")
        age_years = reference_date.year - birthdate_obj.year
        age_months = reference_date.month - birthdate_obj.month
        age_days = reference_date.day - birthdate_obj.day

        if age_days < 0:
            age_months -= 1
            age_days += (birthdate_obj.replace(year=reference_date.year, month=reference_date.month) - timedelta(days=1)).day

        if age_months < 0:
            age_years -= 1
            age_months += 12

        return age_years, age_months, age_days

    @staticmethod
    def days_until_next_birthday(birthdate: str, reference_date: datetime) -> int:
        birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d")
        next_birthday = birthdate_obj.replace(year=reference_date.year)

        if next_birthday < reference_date:
            next_birthday = next_birthday.replace(year=reference_date.year + 1)

        return (next_birthday - reference_date).days

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

class AgeCalculator:
    def __init__(self):
        self.birthdate = ""

    def input_birthdate(self, birthdate: str) -> bool:
        """Validates the input birthdate format."""
        try:
            datetime.strptime(birthdate, "%Y-%m-%d")
            self.birthdate = birthdate
            return True
        except ValueError:
            return False

    def calculate_age(self, current_date: datetime = None) -> str:
        """Calculates the age based on the birthdate."""
        if not self.birthdate:
            return "Invalid birthdate"
        if current_date is None:
            current_date = datetime.today()
        birth_date = datetime.strptime(self.birthdate, "%Y-%m-%d")
        age_years, age_months, age_days = self._calculate_age_components(birth_date, current_date)

        return f"{age_years} years, {age_months} months, {age_days} days"

    def _calculate_age_components(self, birth_date: datetime, current_date: datetime) -> tuple:
        """Calculates age components: years, months, and days."""
        age_years = current_date.year - birth_date.year
        age_months = current_date.month - birth_date.month
        age_days = current_date.day - birth_date.day

        if age_days < 0:
            age_months -= 1
            age_days += (birth_date.replace(month=birth_date.month + 1, day=1) - birth_date.replace(month=birth_date.month, day=1)).days

        if age_months < 0:
            age_years -= 1
            age_months += 12

        return age_years, age_months, age_days

    def days_until_next_birthday(self, current_date: datetime = None) -> int:
        """Calculates the number of days until the next birthday."""
        if not self.birthdate:
            return -1
        if current_date is None:
            current_date = datetime.today()
        birth_date = datetime.strptime(self.birthdate, "%Y-%m-%d")
        next_birthday = birth_date.replace(year=current_date.year)

        if next_birthday < current_date:
            next_birthday = next_birthday.replace(year=current_date.year + 1)

        return (next_birthday - current_date).days

class FileManager:
    def __init__(self):
        self.valid_file = "birthdates.txt"
        self.invalid_file = "invalid_birthdates.txt"

    def save_valid_birthdate(self, birthdate: str):
        """Saves a valid birthdate to the valid file."""
        with open(self.valid_file, "a") as file:
            file.write(birthdate + "\n")

    def log_invalid_birthdate(self, birthdate: str):
        """Logs an invalid birthdate to the invalid file."""
        with open(self.invalid_file, "a") as file:
            file.write(birthdate + "\n")

    def load_birthdates(self) -> list:
        """Loads valid birthdates from the valid file."""
        if not os.path.exists(self.valid_file):
            return []
        with open(self.valid_file, "r") as file:
            return [line.strip() for line in file.readlines()]

class AgeCalculatorApp:
    def __init__(self, master):
        """Initializes the GUI components."""
        self.master = master
        self.master.title("Age Calculator")
        self.age_calculator = AgeCalculator()
        self.file_manager = FileManager()

        self.label = tk.Label(master, text="Enter your birthdate (YYYY-MM-DD):")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.calculate_button = tk.Button(master, text="Calculate Age", command=self.calculate_age)
        self.calculate_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        self.load_birthdates()

    def calculate_age(self):
        """Handles the age calculation and updates the GUI."""
        birthdate = self.entry.get()
        if self.age_calculator.input_birthdate(birthdate):
            self.file_manager.save_valid_birthdate(birthdate)
            age = self.age_calculator.calculate_age()
            days_until_birthday = self.age_calculator.days_until_next_birthday()
            self.result_label.config(text=f"Age: {age}\nDays until next birthday: {days_until_birthday}")
        else:
            self.file_manager.log_invalid_birthdate(birthdate)
            messagebox.showerror("Invalid Input", "Please enter a valid birthdate in YYYY-MM-DD format.")

    def load_birthdates(self):
        """Loads existing valid birthdates into the entry field."""
        birthdates = self.file_manager.load_birthdates()
        if birthdates:
            self.entry.insert(0, birthdates[0])  # Load the first valid birthdate for convenience

if __name__ == "__main__":
    root = tk.Tk()
    app = AgeCalculatorApp(root)
    root.mainloop()
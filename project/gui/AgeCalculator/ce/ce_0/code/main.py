import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from typing import List

class Main:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Age Calculator")
        self.birthdate_manager = BirthdateManager("birthdates.txt", "invalid_birthdates.txt")
        self.create_widgets()
        self.birthdate_manager.load_birthdates()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.frame, text="Enter your birthdate (YYYY-MM-DD):")
        self.label.grid(row=0, column=0)

        self.birthdate_entry = tk.Entry(self.frame)
        self.birthdate_entry.grid(row=0, column=1)

        self.submit_button = tk.Button(self.frame, text="Calculate Age", command=self.calculate_age)
        self.submit_button.grid(row=0, column=2)

        self.result_label = tk.Label(self.frame, text="")
        self.result_label.grid(row=1, columnspan=3)

        self.error_label = tk.Label(self.frame, text="", fg="red")
        self.error_label.grid(row=2, columnspan=3)

    def calculate_age(self):
        birthdate_str = self.birthdate_entry.get()
        try:
            age = self.birthdate_manager.calculate_age(birthdate_str, datetime.today())
            days_until_birthday = self.birthdate_manager.days_until_next_birthday(birthdate_str, datetime.today())
            self.result_label.config(text=f"Age: {age}, Days until next birthday: {days_until_birthday}")
            self.birthdate_manager.save_birthdate(birthdate_str)
            self.error_label.config(text="")
        except ValueError:
            self.error_label.config(text="Invalid birthdate format. Please use YYYY-MM-DD.")

class BirthdateManager:
    def __init__(self, valid_file_path: str, invalid_file_path: str):
        self.valid_file_path = valid_file_path
        self.invalid_file_path = invalid_file_path
        self.valid_birthdates: List[str] = []
        self.invalid_birthdates: List[str] = []

    def load_birthdates(self) -> None:
        try:
            with open(self.valid_file_path, "r") as file:
                self.valid_birthdates = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            self.valid_birthdates = []

    def save_birthdate(self, birthdate: str) -> None:
        with open(self.valid_file_path, "a") as file:
            file.write(f"{birthdate}\n")

    def calculate_age(self, birthdate: str, current_date: datetime) -> str:
        if not self.validate_birthdate_format(birthdate):
            self.log_invalid_birthdate(birthdate)
            raise ValueError("Invalid date format")

        birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d")
        years = current_date.year - birthdate_obj.year
        months = current_date.month - birthdate_obj.month
        days = current_date.day - birthdate_obj.day

        if days < 0:
            months -= 1
            days += (birthdate_obj.replace(month=birthdate_obj.month % 12 + 1, day=1) - 
                      birthdate_obj.replace(month=birthdate_obj.month, day=1)).days

        if months < 0:
            years -= 1
            months += 12

        return f"{years} years, {months} months, {days} days"

    def days_until_next_birthday(self, birthdate: str, current_date: datetime) -> int:
        birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d")
        next_birthday = birthdate_obj.replace(year=current_date.year)

        if next_birthday < current_date:
            next_birthday = next_birthday.replace(year=current_date.year + 1)

        return (next_birthday - current_date).days

    def validate_birthdate_format(self, birthdate: str) -> bool:
        try:
            datetime.strptime(birthdate, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def log_invalid_birthdate(self, birthdate: str) -> None:
        with open(self.invalid_file_path, "a") as file:
            file.write(f"{birthdate}\n")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()
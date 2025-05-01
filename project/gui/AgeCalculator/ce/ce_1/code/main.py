import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

class Main:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Age Calculator")
        
        self.birthdate_entry = tk.Entry(self.window)
        self.birthdate_entry.pack(pady=10)
        
        self.calculate_button = tk.Button(self.window, text="Calculate Age", command=self.calculate_age)
        self.calculate_button.pack(pady=10)
        
        self.age_label = tk.Label(self.window, text="")
        self.age_label.pack(pady=10)
        
        self.days_until_birthday_label = tk.Label(self.window, text="")
        self.days_until_birthday_label.pack(pady=10)
        
        self.load_birthdates()
        
    def main(self):
        self.window.mainloop()
        
    def calculate_age(self):
        birthdate_str = self.birthdate_entry.get()
        try:
            years, months, days = DateUtils.calculate_age(birthdate_str)
            days_until_birthday = DateUtils.days_until_next_birthday(birthdate_str)
            self.age_label.config(text=f"Age: {years} years, {months} months, {days} days")
            self.days_until_birthday_label.config(text=f"Days until next birthday: {days_until_birthday}")
            self.save_birthdate(birthdate_str)
        except ValueError:
            messagebox.showerror("Invalid date", "Please enter a valid date in the format YYYY-MM-DD")
        
    def load_birthdates(self):
        if os.path.exists('birthdates.txt'):
            with open('birthdates.txt', 'r') as file:
                for line in file:
                    self.birthdate_entry.insert(tk.END, line.strip())
        
    def save_birthdate(self, birthdate):
        with open('birthdates.txt', 'a') as file:
            file.write(birthdate + '\n')

class DateUtils:
    @staticmethod
    def calculate_age(birthdate: str) -> tuple:
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        
        years = today.year - birthdate.year
        months = today.month - birthdate.month
        days = today.day - birthdate.day
        
        if days < 0:
            months -= 1
            days += (birthdate.replace(year=today.year, month=today.month) - birthdate.replace(year=today.year, month=today.month - 1)).days
        
        if months < 0:
            years -= 1
            months += 12
        
        return years, months, days
    
    @staticmethod
    def days_until_next_birthday(birthdate: str) -> int:
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        next_birthday = birthdate.replace(year=today.year)
        
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        
        return (next_birthday - today).days

if __name__ == "__main__":
    app = Main()
    app.main()
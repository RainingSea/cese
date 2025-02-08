import tkinter as tk
from tkinter import messagebox
from age_calculator import AgeCalculator

class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Age Calculator")
        self.age_calculator = None
        self.create_widgets()

    def create_widgets(self) -> None:
        tk.Label(self.root, text="Enter your birthdate (YYYY-MM-DD):").pack()

        self.birthdate_entry = tk.Entry(self.root)
        self.birthdate_entry.pack()

        self.calculate_button = tk.Button(self.root, text="Calculate Age", command=self.calculate_age)
        self.calculate_button.pack()

        self.results_label = tk.Label(self.root, text="")
        self.results_label.pack()

        self.root.mainloop()

    def calculate_age(self) -> None:
        birthdate = self.birthdate_entry.get()
        try:
            self.age_calculator = AgeCalculator(birthdate)
            age = self.age_calculator.calculate_age()
            days_until_birthday = self.age_calculator.days_until_next_birthday()
            self.display_results(age, days_until_birthday)
            self.age_calculator.save_birthdate()
        except ValueError:
            messagebox.showerror("Invalid date", "Please enter a valid date in YYYY-MM-DD format.")

    def display_results(self, age: str, days_until_birthday: int) -> None:
        self.results_label.config(text=f"Your age: {age} years\nDays until next birthday: {days_until_birthday}")
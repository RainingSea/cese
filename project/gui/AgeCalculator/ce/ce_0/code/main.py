import tkinter as tk
from tkinter import messagebox
from age_calculator import AgeCalculator

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Age Calculator")

        self.label = tk.Label(self.root, text="Enter your birthdate (YYYY-MM-DD):")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate)
        self.calculate_button.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

    def run(self) -> None:
        self.root.mainloop()

    def calculate(self) -> None:
        birthdate = self.entry.get()
        try:
            age_calculator = AgeCalculator(birthdate)
            age = age_calculator.calculate_age()
            days = age_calculator.days_until_next_birthday()
            self.display_results(age, days)
            age_calculator.save_birthdate()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter the date in the format YYYY-MM-DD.")

    def display_results(self, age: dict, days: int) -> None:
        result_text = f"Age: {age['years']} years, {age['months']} months, {age['days']} days\n"
        result_text += f"Days until next birthday: {days} days"
        self.result_label.config(text=result_text)

if __name__ == "__main__":
    app = MainApp()
    app.run()
import tkinter as tk
from tkinter import messagebox
from age_calculator import AgeCalculator

class Main:
    def __init__(self):
        self.age_calculator = AgeCalculator()

    def main(self) -> None:
        self.root = tk.Tk()
        self.root.title("Age Calculator")

        self.label = tk.Label(self.root, text="Enter your birthdate (YYYY-MM-DD):")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.calculate_button = tk.Button(self.root, text="Calculate Age", command=self.calculate_age)
        self.calculate_button.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        self.days_label = tk.Label(self.root, text="")
        self.days_label.pack()

        self.root.mainloop()

    def calculate_age(self) -> None:
        birthdate = self.entry.get()
        self.age_calculator.set_birthdate(birthdate)
        age_message = self.age_calculator.calculate_age()
        days_message = f"Days until next birthday: {self.age_calculator.days_until_next_birthday()}"

        self.result_label.config(text=age_message)
        self.days_label.config(text=days_message)

        self.age_calculator.save_birthdate()

if __name__ == "__main__":
    app = Main()
    app.main()
import tkinter as tk
from tkinter import messagebox
from age_calculator import AgeCalculator

class Main:
    def __init__(self, master):
        self.master = master
        master.title("Age Calculator")

        self.label = tk.Label(master, text="Enter your birthdate (YYYY-MM-DD):")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.calculate_button = tk.Button(master, text="Calculate Age", command=self.calculate_age)
        self.calculate_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        self.days_label = tk.Label(master, text="")
        self.days_label.pack()

        self.username_label = tk.Label(master, text="Enter your username:")
        self.username_label.pack()

        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        self.save_button = tk.Button(master, text="Save Birthdate", command=self.save_birthdate)
        self.save_button.pack()

    def calculate_age(self):
        birthdate = self.entry.get()
        try:
            age_calculator = AgeCalculator(birthdate)
            age_years, age_months, age_days = age_calculator.calculate_age()
            days_until_birthday = age_calculator.days_until_next_birthday()

            self.result_label.config(text=f"Age: {age_years} years, {age_months} months, {age_days} days")
            self.days_label.config(text=f"Days until next birthday: {days_until_birthday}")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")

    def save_birthdate(self):
        username = self.username_entry.get()
        birthdate = self.entry.get()
        if username and birthdate:
            age_calculator = AgeCalculator(birthdate)
            age_calculator.save_birthdate(username)
            messagebox.showinfo("Success", "Birthdate saved successfully.")
        else:
            messagebox.showerror("Input Error", "Please enter both username and birthdate.")

if __name__ == "__main__":
    root = tk.Tk()
    main_app = Main(root)
    root.mainloop()
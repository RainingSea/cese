import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from birthdate_manager import BirthdateManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Age and Birthday Calculator")
        self.birthdate_manager = BirthdateManager("birthdates.txt")
        self.create_widgets()
        self.load_birthdates()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Enter your birthdate (YYYY-MM-DD):")
        self.label.pack()

        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.calculate_button = tk.Button(self.root, text="Calculate Age", command=self.calculate_age)
        self.calculate_button.pack()

        self.age_label = tk.Label(self.root, text="")
        self.age_label.pack()

        self.days_label = tk.Label(self.root, text="")
        self.days_label.pack()

    def calculate_age(self):
        birthdate_str = self.entry.get()
        if not self.birthdate_manager.validate_birthdate(birthdate_str):
            messagebox.showerror("Invalid Input", "Please enter a valid birthdate in YYYY-MM-DD format.")
            return
        
        try:
            years, months, days = self.birthdate_manager.calculate_age(birthdate_str, datetime.today())
            days_until_birthday = self.birthdate_manager.days_until_next_birthday(birthdate_str, datetime.today())
            self.age_label.config(text=f"Age: {years} years, {months} months, {days} days")
            self.days_label.config(text=f"Days until next birthday: {days_until_birthday}")
            self.birthdate_manager.save_birthdate(birthdate_str)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_birthdates(self):
        birthdates = self.birthdate_manager.load_birthdates()
        for birthdate in birthdates:
            self.entry.insert(tk.END, birthdate + "\n")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()
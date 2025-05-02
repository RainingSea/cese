import tkinter as tk
from tkinter import messagebox
from birthdate_manager import BirthdateManager

class Main:
    def __init__(self):
        self.birthdate_manager = BirthdateManager('birthdates.txt')
        self.window = tk.Tk()
        self.window.title("Age Calculator")
        self.create_widgets()

    def create_widgets(self):
        """Creates the GUI components."""
        self.label = tk.Label(self.window, text="Enter your birthdate (YYYY-MM-DD):")
        self.label.pack()

        self.birthdate_entry = tk.Entry(self.window)
        self.birthdate_entry.pack()

        self.submit_button = tk.Button(self.window, text="Calculate Age", command=self.calculate_age)
        self.submit_button.pack()

        self.result_label = tk.Label(self.window, text="")
        self.result_label.pack()

        self.days_label = tk.Label(self.window, text="")
        self.days_label.pack()

    def calculate_age(self):
        """Handles the age calculation and updates the GUI with results."""
        birthdate = self.birthdate_entry.get()
        if not self.birthdate_manager.validate_birthdate_format(birthdate):
            messagebox.showerror("Invalid Input", "Please enter a valid date in YYYY-MM-DD format.")
            return

        self.birthdate_manager.save_birthdate(birthdate)
        age = self.birthdate_manager.calculate_age(birthdate)
        days_until_birthday = self.birthdate_manager.days_until_next_birthday(birthdate)

        self.result_label.config(text=f"Age: {age[0]} years, {age[1]} months, {age[2]} days")
        self.days_label.config(text=f"Days until next birthday: {days_until_birthday}")

    def main(self):
        """The entry point of the application that initializes the GUI and handles user interactions."""
        self.window.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()
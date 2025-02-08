import tkinter as tk
from tkinter import messagebox
from age_calculator import AgeCalculator

class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Age Calculator")
        self.age_calculator = None
        self.create_widgets()

    def create_widgets(self) -> None:
        tk.Label(self.root, text="Enter your birthdate (YYYY-MM-DD):").pack()

        self.birthdate_entry = tk.Entry(self.root)
        self.birthdate_entry.pack()

        submit_button = tk.Button(self.root, text="Submit", command=self.submit_birthdate)
        submit_button.pack()

        self.age_label = tk.Label(self.root, text="")
        self.age_label.pack()

        self.days_label = tk.Label(self.root, text="")
        self.days_label.pack()

        clear_button = tk.Button(self.root, text="Clear", command=self.clear_fields)
        clear_button.pack()

    def submit_birthdate(self) -> None:
        birthdate = self.birthdate_entry.get()
        try:
            self.age_calculator = AgeCalculator(birthdate)
            self.age_calculator.store_birthdate()
            self.age_label.config(text=self.age_calculator.display_age())
            self.days_label.config(text=self.age_calculator.display_days_until_birthday())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid date in YYYY-MM-DD format.")

    def clear_fields(self) -> None:
        self.birthdate_entry.delete(0, tk.END)
        self.age_label.config(text="")
        self.days_label.config(text="")

    def run(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    ui = UserInterface()
    ui.run()
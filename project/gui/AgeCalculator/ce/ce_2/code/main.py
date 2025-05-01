import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from birthdate_manager import BirthdateManager

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Age Calculator")
        
        self.birthdate_manager = BirthdateManager("birthdates.txt")
        
        self.label = tk.Label(master, text="Enter your birthdate (YYYY-MM-DD):")
        self.label.pack()
        
        self.birthdate_entry = tk.Entry(master)
        self.birthdate_entry.pack()
        
        self.calculate_button = tk.Button(master, text="Calculate Age", command=self.calculate_age)
        self.calculate_button.pack()
        
        self.result_label = tk.Label(master, text="")
        self.result_label.pack()
        
        self.days_label = tk.Label(master, text="")
        self.days_label.pack()

    def calculate_age(self):
        birthdate_str = self.birthdate_entry.get()
        try:
            age = self.birthdate_manager.calculate_age(birthdate_str)
            days_until_birthday = self.birthdate_manager.days_until_next_birthday(birthdate_str)
            self.result_label.config(text=f"Age: {age[0]} years, {age[1]} months, {age[2]} days")
            self.days_label.config(text=f"Days until next birthday: {days_until_birthday}")
            self.birthdate_manager.save_birthdate(birthdate_str)
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in the format YYYY-MM-DD.")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()
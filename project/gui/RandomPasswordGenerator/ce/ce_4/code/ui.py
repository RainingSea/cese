import tkinter as tk
from tkinter import messagebox
from password_generator import PasswordGenerator

class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Generator")
        self.password_generator = PasswordGenerator(12, True, True, True, True, False)
        self.create_widgets()

    def create_widgets(self) -> None:
        tk.Label(self.root, text="Password Length:").grid(row=0, column=0)
        self.length_entry = tk.Entry(self.root)
        self.length_entry.grid(row=0, column=1)
        self.length_entry.insert(0, str(self.password_generator.length))

        self.include_upper = tk.BooleanVar(value=self.password_generator.include_upper)
        tk.Checkbutton(self.root, text="Include Uppercase", variable=self.include_upper).grid(row=1, columnspan=2)

        self.include_lower = tk.BooleanVar(value=self.password_generator.include_lower)
        tk.Checkbutton(self.root, text="Include Lowercase", variable=self.include_lower).grid(row=2, columnspan=2)

        self.include_numbers = tk.BooleanVar(value=self.password_generator.include_numbers)
        tk.Checkbutton(self.root, text="Include Numbers", variable=self.include_numbers).grid(row=3, columnspan=2)

        self.include_symbols = tk.BooleanVar(value=self.password_generator.include_symbols)
        tk.Checkbutton(self.root, text="Include Symbols", variable=self.include_symbols).grid(row=4, columnspan=2)

        self.exclude_ambiguous = tk.BooleanVar(value=self.password_generator.exclude_ambiguous)
        tk.Checkbutton(self.root, text="Exclude Ambiguous Characters", variable=self.exclude_ambiguous).grid(row=5, columnspan=2)

        self.generate_button = tk.Button(self.root, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=6, columnspan=2)

        self.save_button = tk.Button(self.root, text="Save Preferences", command=self.save_preferences)
        self.save_button.grid(row=7, columnspan=2)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=8, columnspan=2)

        self.load_preferences()

    def generate_password(self) -> None:
        try:
            self.password_generator.length = int(self.length_entry.get())
            self.password_generator.include_upper = self.include_upper.get()
            self.password_generator.include_lower = self.include_lower.get()
            self.password_generator.include_numbers = self.include_numbers.get()
            self.password_generator.include_symbols = self.include_symbols.get()
            self.password_generator.exclude_ambiguous = self.exclude_ambiguous.get()
            password = self.password_generator.generate_password()
            self.result_label.config(text=password)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for password length.")

    def save_preferences(self) -> None:
        self.password_generator.length = int(self.length_entry.get())
        self.password_generator.include_upper = self.include_upper.get()
        self.password_generator.include_lower = self.include_lower.get()
        self.password_generator.include_numbers = self.include_numbers.get()
        self.password_generator.include_symbols = self.include_symbols.get()
        self.password_generator.exclude_ambiguous = self.exclude_ambiguous.get()
        self.password_generator.save_preferences()

    def load_preferences(self) -> None:
        self.password_generator.load_preferences()
        self.length_entry.delete(0, tk.END)
        self.length_entry.insert(0, str(self.password_generator.length))
        self.include_upper.set(self.password_generator.include_upper)
        self.include_lower.set(self.password_generator.include_lower)
        self.include_numbers.set(self.password_generator.include_numbers)
        self.include_symbols.set(self.password_generator.include_symbols)
        self.exclude_ambiguous.set(self.password_generator.exclude_ambiguous)

    def run(self) -> None:
        self.root.mainloop()
import tkinter as tk
from tkinter import messagebox
from user_preferences import UserPreferences
from password_generator import PasswordGenerator

class GUI:
    def __init__(self):
        self.user_preferences = UserPreferences()
        self.user_preferences.load_preferences()
        self.create_main_window()

    def create_main_window(self) -> None:
        self.root = tk.Tk()
        self.root.title("Random Password Generator")

        tk.Label(self.root, text="Password Length:").grid(row=0, column=0)
        self.length_entry = tk.Entry(self.root)
        self.length_entry.insert(0, str(self.user_preferences.length))
        self.length_entry.grid(row=0, column=1)

        self.uppercase_var = tk.BooleanVar(value=self.user_preferences.include_uppercase)
        tk.Checkbutton(self.root, text="Include Uppercase", variable=self.uppercase_var).grid(row=1, columnspan=2)

        self.lowercase_var = tk.BooleanVar(value=self.user_preferences.include_lowercase)
        tk.Checkbutton(self.root, text="Include Lowercase", variable=self.lowercase_var).grid(row=2, columnspan=2)

        self.numbers_var = tk.BooleanVar(value=self.user_preferences.include_numbers)
        tk.Checkbutton(self.root, text="Include Numbers", variable=self.numbers_var).grid(row=3, columnspan=2)

        self.symbols_var = tk.BooleanVar(value=self.user_preferences.include_symbols)
        tk.Checkbutton(self.root, text="Include Symbols", variable=self.symbols_var).grid(row=4, columnspan=2)

        self.ambiguous_var = tk.BooleanVar(value=self.user_preferences.exclude_ambiguous)
        tk.Checkbutton(self.root, text="Exclude Ambiguous Characters", variable=self.ambiguous_var).grid(row=5, columnspan=2)

        self.generate_button = tk.Button(self.root, text="Generate Password", command=self.on_generate_button_click)
        self.generate_button.grid(row=6, columnspan=2)

        self.password_display = tk.Text(self.root, height=2, width=30)
        self.password_display.grid(row=7, columnspan=2)

        self.root.mainloop()

    def on_generate_button_click(self) -> None:
        length = int(self.length_entry.get())
        include_uppercase = self.uppercase_var.get()
        include_lowercase = self.lowercase_var.get()
        include_numbers = self.numbers_var.get()
        include_symbols = self.symbols_var.get()
        exclude_ambiguous = self.ambiguous_var.get()

        generator = PasswordGenerator(length, include_uppercase, include_lowercase, 
                                      include_numbers, include_symbols, exclude_ambiguous)
        password = generator.generate_password()
        self.password_display.delete(1.0, tk.END)
        self.password_display.insert(tk.END, password)
        generator.save_generated_password(password)
        self.user_preferences.length = length
        self.user_preferences.include_uppercase = include_uppercase
        self.user_preferences.include_lowercase = include_lowercase
        self.user_preferences.include_numbers = include_numbers
        self.user_preferences.include_symbols = include_symbols
        self.user_preferences.exclude_ambiguous = exclude_ambiguous
        self.user_preferences.save_user_preferences()
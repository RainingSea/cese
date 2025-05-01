import tkinter as tk
from tkinter import messagebox
import random
import string
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self, length=12, include_uppercase=True, include_lowercase=True,
                 include_numbers=True, include_symbols=True, exclude_ambiguous=False):
        self._length = length
        self.include_uppercase = include_uppercase
        self.include_lowercase = include_lowercase
        self.include_numbers = include_numbers
        self.include_symbols = include_symbols
        self.exclude_ambiguous = exclude_ambiguous

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        if value < 1:
            raise ValueError("Password length must be at least 1.")
        self._length = value

    def generate_password(self) -> str:
        """Generates a random password based on the selected criteria."""
        characters = ''
        if self.include_uppercase:
            characters += string.ascii_uppercase
        if self.include_lowercase:
            characters += string.ascii_lowercase
        if self.include_numbers:
            characters += string.digits
        if self.include_symbols:
            characters += string.punctuation

        if self.exclude_ambiguous:
            characters = characters.replace('l', '').replace('1', '').replace('O', '').replace('0', '').replace('I', '')

        if not characters:
            raise ValueError("At least one character type must be selected.")

        password = ''.join(random.choice(characters) for _ in range(self.length))
        return password

    def save_password(self, password: str):
        """Saves the generated password to a file with a timestamp."""
        with open('generated_passwords.txt', 'a') as f:
            f.write(f"{password} | {datetime.now()}\n")

    def load_preferences(self):
        """Loads user preferences from a file."""
        if os.path.exists('user_preferences.txt'):
            with open('user_preferences.txt', 'r') as f:
                preferences = f.read().strip().split('|')
                self.length = int(preferences[0])
                self.include_uppercase = preferences[1] == 'True'
                self.include_lowercase = preferences[2] == 'True'
                self.include_numbers = preferences[3] == 'True'
                self.include_symbols = preferences[4] == 'True'
                self.exclude_ambiguous = preferences[5] == 'True'

    def save_preferences(self):
        """Saves user preferences to a file."""
        with open('user_preferences.txt', 'w') as f:
            f.write(f"{self.length}|{self.include_uppercase}|{self.include_lowercase}|"
                     f"{self.include_numbers}|{self.include_symbols}|{self.exclude_ambiguous}\n")

    def handle_invalid_input(self, message: str):
        """Displays an error message for invalid input."""
        messagebox.showerror("Input Error", message)

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.password_generator = PasswordGenerator()
        self.password_generator.load_preferences()

        self.create_widgets()

    def create_widgets(self):
        """Creates the GUI widgets."""
        tk.Label(self.root, text="Password Length:").grid(row=0, column=0)
        self.length_entry = tk.Entry(self.root)
        self.length_entry.insert(0, str(self.password_generator.length))
        self.length_entry.grid(row=0, column=1)

        self.uppercase_var = tk.BooleanVar(value=self.password_generator.include_uppercase)
        tk.Checkbutton(self.root, text="Include Uppercase", variable=self.uppercase_var).grid(row=1, columnspan=2)

        self.lowercase_var = tk.BooleanVar(value=self.password_generator.include_lowercase)
        tk.Checkbutton(self.root, text="Include Lowercase", variable=self.lowercase_var).grid(row=2, columnspan=2)

        self.numbers_var = tk.BooleanVar(value=self.password_generator.include_numbers)
        tk.Checkbutton(self.root, text="Include Numbers", variable=self.numbers_var).grid(row=3, columnspan=2)

        self.symbols_var = tk.BooleanVar(value=self.password_generator.include_symbols)
        tk.Checkbutton(self.root, text="Include Symbols", variable=self.symbols_var).grid(row=4, columnspan=2)

        self.ambiguous_var = tk.BooleanVar(value=self.password_generator.exclude_ambiguous)
        tk.Checkbutton(self.root, text="Exclude Ambiguous Characters", variable=self.ambiguous_var).grid(row=5, columnspan=2)

        self.generate_button = tk.Button(self.root, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=6, columnspan=2)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=7, columnspan=2)

    def generate_password(self):
        """Handles the password generation process."""
        try:
            self.password_generator.length = int(self.length_entry.get())
            self.password_generator.include_uppercase = self.uppercase_var.get()
            self.password_generator.include_lowercase = self.lowercase_var.get()
            self.password_generator.include_numbers = self.numbers_var.get()
            self.password_generator.include_symbols = self.symbols_var.get()
            self.password_generator.exclude_ambiguous = self.ambiguous_var.get()

            password = self.password_generator.generate_password()
            self.result_label.config(text=password)
            self.password_generator.save_password(password)
            self.password_generator.save_preferences()
        except ValueError as e:
            self.password_generator.handle_invalid_input(str(e))

def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()
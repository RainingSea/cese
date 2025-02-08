import tkinter as tk
from tkinter import messagebox
from password_generator import PasswordGenerator

class Main:
    def __init__(self):
        self.password_generator = PasswordGenerator(12, True, True, True, True, False)
        self.password_generator.load_preferences()
        self.create_ui()

    def create_ui(self):
        self.root = tk.Tk()
        self.root.title("Random Password Generator")

        tk.Label(self.root, text="Password Length:").grid(row=0, column=0)
        self.length_entry = tk.Entry(self.root)
        self.length_entry.insert(0, str(self.password_generator.length))
        self.length_entry.grid(row=0, column=1)

        self.include_uppercase_var = tk.BooleanVar(value=self.password_generator.include_uppercase)
        tk.Checkbutton(self.root, text="Include Uppercase", variable=self.include_uppercase_var).grid(row=1, columnspan=2)

        self.include_lowercase_var = tk.BooleanVar(value=self.password_generator.include_lowercase)
        tk.Checkbutton(self.root, text="Include Lowercase", variable=self.include_lowercase_var).grid(row=2, columnspan=2)

        self.include_numbers_var = tk.BooleanVar(value=self.password_generator.include_numbers)
        tk.Checkbutton(self.root, text="Include Numbers", variable=self.include_numbers_var).grid(row=3, columnspan=2)

        self.include_symbols_var = tk.BooleanVar(value=self.password_generator.include_symbols)
        tk.Checkbutton(self.root, text="Include Symbols", variable=self.include_symbols_var).grid(row=4, columnspan=2)

        self.exclude_ambiguous_var = tk.BooleanVar(value=self.password_generator.exclude_ambiguous)
        tk.Checkbutton(self.root, text="Exclude Ambiguous Characters", variable=self.exclude_ambiguous_var).grid(row=5, columnspan=2)

        self.generate_button = tk.Button(self.root, text="Generate", command=self.generate_password)
        self.generate_button.grid(row=6, columnspan=2)

        self.result_text = tk.Text(self.root, height=5, width=30)
        self.result_text.grid(row=7, columnspan=2)

        self.root.mainloop()

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            self.password_generator.length = length
            self.password_generator.include_uppercase = self.include_uppercase_var.get()
            self.password_generator.include_lowercase = self.include_lowercase_var.get()
            self.password_generator.include_numbers = self.include_numbers_var.get()
            self.password_generator.include_symbols = self.include_symbols_var.get()
            self.password_generator.exclude_ambiguous = self.exclude_ambiguous_var.get()

            password = self.password_generator.generate_password()
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, password)

            self.password_generator.save_preferences()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for password length.")

if __name__ == "__main__":
    Main()
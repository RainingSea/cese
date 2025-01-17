import tkinter as tk
from tkinter import messagebox
from PasswordGenerator import PasswordGenerator

class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Random Password Generator")
        self.password_generator = PasswordGenerator(12, True, True, True, True, False)
        self.create_widgets()

    def create_widgets(self) -> None:
        tk.Label(self.root, text="Password Length:").grid(row=0, column=0)
        self.length_entry = tk.Entry(self.root)
        self.length_entry.grid(row=0, column=1)
        
        self.uppercase_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Include Uppercase", variable=self.uppercase_var).grid(row=1, columnspan=2)

        self.lowercase_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Include Lowercase", variable=self.lowercase_var).grid(row=2, columnspan=2)

        self.numbers_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Include Numbers", variable=self.numbers_var).grid(row=3, columnspan=2)

        self.symbols_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Include Symbols", variable=self.symbols_var).grid(row=4, columnspan=2)

        self.exclude_ambiguous_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.root, text="Exclude Ambiguous Characters", variable=self.exclude_ambiguous_var).grid(row=5, columnspan=2)

        self.generate_button = tk.Button(self.root, text="Generate Password", command=self.generate_and_display_password)
        self.generate_button.grid(row=6, columnspan=2)

        self.password_display = tk.Text(self.root, height=5, width=30)
        self.password_display.grid(row=7, columnspan=2)

        self.save_button = tk.Button(self.root, text="Save Password", command=self.save_generated_password)
        self.save_button.grid(row=8, columnspan=2)

        self.load_preferences()

    def generate_and_display_password(self) -> None:
        try:
            length = int(self.length_entry.get())
            self.password_generator.length = length
            self.password_generator.include_uppercase = self.uppercase_var.get()
            self.password_generator.include_lowercase = self.lowercase_var.get()
            self.password_generator.include_numbers = self.numbers_var.get()
            self.password_generator.include_symbols = self.symbols_var.get()
            self.password_generator.exclude_ambiguous = self.exclude_ambiguous_var.get()

            password = self.password_generator.generate_password()
            self.password_display.delete(1.0, tk.END)
            self.password_display.insert(tk.END, password)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for password length.")

    def save_generated_password(self) -> None:
        password = self.password_display.get(1.0, tk.END).strip()
        if password:
            self.password_generator.save_password(password)
            messagebox.showinfo("Success", "Password saved successfully!")
        else:
            messagebox.showwarning("Warning", "No password to save.")

    def load_preferences(self) -> None:
        self.password_generator.load_preferences()
        self.length_entry.insert(0, str(self.password_generator.length))
        self.uppercase_var.set(self.password_generator.include_uppercase)
        self.lowercase_var.set(self.password_generator.include_lowercase)
        self.numbers_var.set(self.password_generator.include_numbers)
        self.symbols_var.set(self.password_generator.include_symbols)
        self.exclude_ambiguous_var.set(self.password_generator.exclude_ambiguous)

if __name__ == "__main__":
    app = UI()
    app.root.mainloop()
import random
import string
import tkinter as tk
from tkinter import messagebox

class PasswordGenerator:
    def __init__(self):
        self.length = 12
        self.include_uppercase = True
        self.include_lowercase = True
        self.include_numbers = True
        self.include_symbols = True
        self.exclude_ambiguous = False

    def generate_password(self) -> str:
        character_pool = ''
        if self.include_uppercase:
            character_pool += string.ascii_uppercase
        if self.include_lowercase:
            character_pool += string.ascii_lowercase
        if self.include_numbers:
            character_pool += string.digits
        if self.include_symbols:
            character_pool += string.punctuation

        if self.exclude_ambiguous:
            ambiguous_chars = 'il1Lo0O'
            character_pool = ''.join(c for c in character_pool if c not in ambiguous_chars)

        if not character_pool:
            raise ValueError("At least one character type must be selected.")

        return ''.join(random.choice(character_pool) for _ in range(self.length))

    def save_password(self, password: str) -> None:
        with open('generated_passwords.txt', 'a') as file:
            file.write(password + '\n')

    def load_config(self) -> None:
        try:
            with open('config.txt', 'r') as file:
                config = file.readlines()
                self.length = int(config[0].strip())
                self.include_uppercase = config[1].strip() == 'True'
                self.include_lowercase = config[2].strip() == 'True'
                self.include_numbers = config[3].strip() == 'True'
                self.include_symbols = config[4].strip() == 'True'
                self.exclude_ambiguous = config[5].strip() == 'True'
        except Exception as e:
            print(f"Error loading config: {e}")

    def save_config(self) -> None:
        with open('config.txt', 'w') as file:
            file.write(f"{self.length}\n")
            file.write(f"{self.include_uppercase}\n")
            file.write(f"{self.include_lowercase}\n")
            file.write(f"{self.include_numbers}\n")
            file.write(f"{self.include_symbols}\n")
            file.write(f"{self.exclude_ambiguous}\n")

class Main:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Random Password Generator")
        self.password_generator = PasswordGenerator()
        self.password_generator.load_config()

        self.create_widgets()

    def create_widgets(self):
        self.length_label = tk.Label(self.root, text="Password Length:")
        self.length_label.pack()

        self.length_entry = tk.Entry(self.root)
        self.length_entry.insert(0, str(self.password_generator.length))
        self.length_entry.pack()

        self.uppercase_var = tk.BooleanVar(value=self.password_generator.include_uppercase)
        self.uppercase_checkbox = tk.Checkbutton(self.root, text="Include Uppercase Letters", variable=self.uppercase_var)
        self.uppercase_checkbox.pack()

        self.lowercase_var = tk.BooleanVar(value=self.password_generator.include_lowercase)
        self.lowercase_checkbox = tk.Checkbutton(self.root, text="Include Lowercase Letters", variable=self.lowercase_var)
        self.lowercase_checkbox.pack()

        self.numbers_var = tk.BooleanVar(value=self.password_generator.include_numbers)
        self.numbers_checkbox = tk.Checkbutton(self.root, text="Include Numbers", variable=self.numbers_var)
        self.numbers_checkbox.pack()

        self.symbols_var = tk.BooleanVar(value=self.password_generator.include_symbols)
        self.symbols_checkbox = tk.Checkbutton(self.root, text="Include Symbols", variable=self.symbols_var)
        self.symbols_checkbox.pack()

        self.ambiguous_var = tk.BooleanVar(value=self.password_generator.exclude_ambiguous)
        self.ambiguous_checkbox = tk.Checkbutton(self.root, text="Exclude Ambiguous Characters", variable=self.ambiguous_var)
        self.ambiguous_checkbox.pack()

        self.generate_button = tk.Button(self.root, text="Generate Password", command=self.generate_password)
        self.generate_button.pack()

        self.save_button = tk.Button(self.root, text="Save Password", command=self.save_password)
        self.save_button.pack()

        self.password_display = tk.Text(self.root, height=2, width=30)
        self.password_display.pack()

    def generate_password(self):
        try:
            self.password_generator.length = int(self.length_entry.get())
            self.password_generator.include_uppercase = self.uppercase_var.get()
            self.password_generator.include_lowercase = self.lowercase_var.get()
            self.password_generator.include_numbers = self.numbers_var.get()
            self.password_generator.include_symbols = self.symbols_var.get()
            self.password_generator.exclude_ambiguous = self.ambiguous_var.get()

            password = self.password_generator.generate_password()
            self.password_display.delete(1.0, tk.END)
            self.password_display.insert(tk.END, password)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def save_password(self):
        password = self.password_display.get(1.0, tk.END).strip()
        if password:
            self.password_generator.save_password(password)
            messagebox.showinfo("Success", "Password saved successfully!")
        else:
            messagebox.showwarning("Warning", "No password to save.")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()
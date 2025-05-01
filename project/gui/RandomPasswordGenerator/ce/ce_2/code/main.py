import tkinter as tk
from tkinter import messagebox
import random

class PasswordGenerator:
    def __init__(self):
        self.length = 12
        self.include_uppercase = True
        self.include_lowercase = True
        self.include_numbers = True
        self.include_symbols = True
        self.exclude_ambiguous = False

    def generate_password(self) -> str:
        if self.length < 1:
            raise ValueError("Password length must be at least 1.")
        
        character_pool = ""
        if self.include_uppercase:
            character_pool += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.include_lowercase:
            character_pool += "abcdefghijklmnopqrstuvwxyz"
        if self.include_numbers:
            character_pool += "0123456789"
        if self.include_symbols:
            character_pool += "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        
        if self.exclude_ambiguous:
            character_pool = character_pool.replace("l", "").replace("1", "").replace("O", "").replace("0", "").replace("I", "").replace("i", "")
        
        if not character_pool:
            raise ValueError("No character types selected for password generation.")
        
        password = ''.join(random.choice(character_pool) for _ in range(self.length))
        self.save_generated_password(password)
        return password

    def save_preferences(self) -> None:
        with open('user_preferences.txt', 'w') as f:
            f.write(f"{self.length}\n")
            f.write(f"{self.include_uppercase}\n")
            f.write(f"{self.include_lowercase}\n")
            f.write(f"{self.include_numbers}\n")
            f.write(f"{self.include_symbols}\n")
            f.write(f"{self.exclude_ambiguous}\n")

    def load_preferences(self) -> None:
        try:
            with open('user_preferences.txt', 'r') as f:
                self.length = int(f.readline().strip())
                self.include_uppercase = f.readline().strip() == 'True'
                self.include_lowercase = f.readline().strip() == 'True'
                self.include_numbers = f.readline().strip() == 'True'
                self.include_symbols = f.readline().strip() == 'True'
                self.exclude_ambiguous = f.readline().strip() == 'True'
        except FileNotFoundError:
            pass

    def save_generated_password(self, password: str) -> None:
        with open('generated_passwords.txt', 'a') as f:
            f.write(password + '\n')

class Main:
    def __init__(self, root):
        self.password_generator = PasswordGenerator()
        self.password_generator.load_preferences()
        
        self.root = root
        self.root.title("Random Password Generator")

        self.length_label = tk.Label(root, text="Password Length:")
        self.length_label.pack()
        self.length_entry = tk.Entry(root)
        self.length_entry.insert(0, str(self.password_generator.length))
        self.length_entry.pack()

        self.uppercase_var = tk.BooleanVar(value=self.password_generator.include_uppercase)
        self.lowercase_var = tk.BooleanVar(value=self.password_generator.include_lowercase)
        self.numbers_var = tk.BooleanVar(value=self.password_generator.include_numbers)
        self.symbols_var = tk.BooleanVar(value=self.password_generator.include_symbols)
        self.ambiguous_var = tk.BooleanVar(value=self.password_generator.exclude_ambiguous)

        self.uppercase_check = tk.Checkbutton(root, text="Include Uppercase Letters", variable=self.uppercase_var)
        self.uppercase_check.pack()
        self.lowercase_check = tk.Checkbutton(root, text="Include Lowercase Letters", variable=self.lowercase_var)
        self.lowercase_check.pack()
        self.numbers_check = tk.Checkbutton(root, text="Include Numbers", variable=self.numbers_var)
        self.numbers_check.pack()
        self.symbols_check = tk.Checkbutton(root, text="Include Symbols", variable=self.symbols_var)
        self.symbols_check.pack()
        self.ambiguous_check = tk.Checkbutton(root, text="Exclude Ambiguous Characters", variable=self.ambiguous_var)
        self.ambiguous_check.pack()

        self.generate_button = tk.Button(root, text="Generate Password", command=self.generate_password)
        self.generate_button.pack()

        self.result_text = tk.Text(root, height=2, width=30)
        self.result_text.pack()

    def generate_password(self) -> None:
        try:
            self.password_generator.length = int(self.length_entry.get())
            self.password_generator.include_uppercase = self.uppercase_var.get()
            self.password_generator.include_lowercase = self.lowercase_var.get()
            self.password_generator.include_numbers = self.numbers_var.get()
            self.password_generator.include_symbols = self.symbols_var.get()
            self.password_generator.exclude_ambiguous = self.ambiguous_var.get()

            password = self.password_generator.generate_password()
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, password)
            self.password_generator.save_preferences()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

def main() -> None:
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()
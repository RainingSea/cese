import tkinter as tk
import random
import string

class Main:
    def __init__(self):
        self.password_length = 12
        self.include_uppercase = True
        self.include_lowercase = True
        self.include_numbers = True
        self.include_symbols = True
        self.exclude_ambiguous = False
        self.load_preferences()
        
        self.root = tk.Tk()
        self.root.title("Random Password Generator")
        
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.root, text="Password Length:").grid(row=0, column=0)
        self.length_entry = tk.Entry(self.root)
        self.length_entry.insert(0, str(self.password_length))
        self.length_entry.grid(row=0, column=1)

        self.uppercase_var = tk.BooleanVar(value=self.include_uppercase)
        tk.Checkbutton(self.root, text="Include Uppercase Letters", variable=self.uppercase_var).grid(row=1, columnspan=2)

        self.lowercase_var = tk.BooleanVar(value=self.include_lowercase)
        tk.Checkbutton(self.root, text="Include Lowercase Letters", variable=self.lowercase_var).grid(row=2, columnspan=2)

        self.numbers_var = tk.BooleanVar(value=self.include_numbers)
        tk.Checkbutton(self.root, text="Include Numbers", variable=self.numbers_var).grid(row=3, columnspan=2)

        self.symbols_var = tk.BooleanVar(value=self.include_symbols)
        tk.Checkbutton(self.root, text="Include Symbols", variable=self.symbols_var).grid(row=4, columnspan=2)

        self.ambiguous_var = tk.BooleanVar(value=self.exclude_ambiguous)
        tk.Checkbutton(self.root, text="Exclude Ambiguous Characters", variable=self.ambiguous_var).grid(row=5, columnspan=2)

        self.generate_button = tk.Button(self.root, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=6, columnspan=2)

        self.result_label = tk.Label(self.root, text="", wraplength=300)
        self.result_label.grid(row=7, columnspan=2)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def generate_password(self):
        self.password_length = int(self.length_entry.get())
        self.include_uppercase = self.uppercase_var.get()
        self.include_lowercase = self.lowercase_var.get()
        self.include_numbers = self.numbers_var.get()
        self.include_symbols = self.symbols_var.get()
        self.exclude_ambiguous = self.ambiguous_var.get()

        characters = ""
        if self.include_uppercase:
            characters += string.ascii_uppercase
        if self.include_lowercase:
            characters += string.ascii_lowercase
        if self.include_numbers:
            characters += string.digits
        if self.include_symbols:
            characters += string.punctuation

        if self.exclude_ambiguous:
            characters = characters.replace('l', '').replace('1', '').replace('O', '').replace('0', '').replace('I', '').replace('i', '')

        if characters:
            password = ''.join(random.choice(characters) for _ in range(self.password_length))
            self.result_label.config(text=password)
            self.save_password(password)
        else:
            self.result_label.config(text="No character types selected!")

    def save_password(self, password: str):
        with open('passwords.txt', 'a') as f:
            f.write(password + '\n')

    def load_preferences(self):
        try:
            with open('config.txt', 'r') as f:
                lines = f.readlines()
                if lines:
                    self.password_length = int(lines[0].strip())
                    self.include_uppercase = lines[1].strip() == 'True'
                    self.include_lowercase = lines[2].strip() == 'True'
                    self.include_numbers = lines[3].strip() == 'True'
                    self.include_symbols = lines[4].strip() == 'True'
                    self.exclude_ambiguous = lines[5].strip() == 'True'
        except FileNotFoundError:
            pass

    def save_preferences(self):
        with open('config.txt', 'w') as f:
            f.write(f"{self.password_length}\n")
            f.write(f"{self.include_uppercase}\n")
            f.write(f"{self.include_lowercase}\n")
            f.write(f"{self.include_numbers}\n")
            f.write(f"{self.include_symbols}\n")
            f.write(f"{self.exclude_ambiguous}\n")

    def on_closing(self):
        self.save_preferences()
        self.root.destroy()

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()
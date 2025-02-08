import random
import string
from tkinter import Tk, Label, Entry, Button, Text, Checkbutton, IntVar, END

class PasswordGenerator:
    def __init__(self, length: int, include_upper: bool, include_lower: bool, 
                 include_numbers: bool, include_symbols: bool, exclude_ambiguous: bool):
        self.length = length
        self.include_upper = include_upper
        self.include_lower = include_lower
        self.include_numbers = include_numbers
        self.include_symbols = include_symbols
        self.exclude_ambiguous = exclude_ambiguous

    def generate_password(self) -> str:
        character_pool = ''
        if self.include_upper:
            character_pool += string.ascii_uppercase
        if self.include_lower:
            character_pool += string.ascii_lowercase
        if self.include_numbers:
            character_pool += string.digits
        if self.include_symbols:
            character_pool += string.punctuation
        
        if self.exclude_ambiguous:
            ambiguous_characters = 'il1Lo0O'
            character_pool = ''.join(c for c in character_pool if c not in ambiguous_characters)

        return ''.join(random.choice(character_pool) for _ in range(self.length))

    def save_password(self, password: str):
        with open('generated_passwords.txt', 'a') as file:
            file.write(password + '\n')

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Password Generator")
        self.create_widgets()

    def create_widgets(self):
        Label(self.root, text="Password Length:").pack()
        self.length_entry = Entry(self.root)
        self.length_entry.pack()

        self.include_upper = IntVar()
        Checkbutton(self.root, text="Include Uppercase", variable=self.include_upper).pack()

        self.include_lower = IntVar()
        Checkbutton(self.root, text="Include Lowercase", variable=self.include_lower).pack()

        self.include_numbers = IntVar()
        Checkbutton(self.root, text="Include Numbers", variable=self.include_numbers).pack()

        self.include_symbols = IntVar()
        Checkbutton(self.root, text="Include Symbols", variable=self.include_symbols).pack()

        self.exclude_ambiguous = IntVar()
        Checkbutton(self.root, text="Exclude Ambiguous Characters", variable=self.exclude_ambiguous).pack()

        Button(self.root, text="Generate Password", command=self.generate_button_clicked).pack()

        self.output_area = Text(self.root, height=5, width=50)
        self.output_area.pack()

    def generate_button_clicked(self):
        length = int(self.length_entry.get())
        password_generator = PasswordGenerator(
            length,
            self.include_upper.get(),
            self.include_lower.get(),
            self.include_numbers.get(),
            self.include_symbols.get(),
            self.exclude_ambiguous.get()
        )
        password = password_generator.generate_password()
        self.output_area.delete(1.0, END)
        self.output_area.insert(END, password)
        password_generator.save_password(password)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
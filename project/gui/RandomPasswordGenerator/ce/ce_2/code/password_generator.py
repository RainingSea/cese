import random
import string

class PasswordGenerator:
    def __init__(self, length: int, include_uppercase: bool, include_lowercase: bool,
                 include_numbers: bool, include_symbols: bool, exclude_ambiguous: bool):
        self.length = length
        self.include_uppercase = include_uppercase
        self.include_lowercase = include_lowercase
        self.include_numbers = include_numbers
        self.include_symbols = include_symbols
        self.exclude_ambiguous = exclude_ambiguous

    def generate_password(self) -> str:
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
            ambiguous_chars = 'il1Lo0O'
            characters = ''.join(c for c in characters if c not in ambiguous_chars)

        password = ''.join(random.choice(characters) for _ in range(self.length))
        return password

    def save_preferences(self) -> None:
        with open('preferences.txt', 'w') as f:
            f.write(f"{self.length}\n")
            f.write(f"{self.include_uppercase}\n")
            f.write(f"{self.include_lowercase}\n")
            f.write(f"{self.include_numbers}\n")
            f.write(f"{self.include_symbols}\n")
            f.write(f"{self.exclude_ambiguous}\n")

    def load_preferences(self) -> None:
        try:
            with open('preferences.txt', 'r') as f:
                self.length = int(f.readline().strip())
                self.include_uppercase = f.readline().strip() == 'True'
                self.include_lowercase = f.readline().strip() == 'True'
                self.include_numbers = f.readline().strip() == 'True'
                self.include_symbols = f.readline().strip() == 'True'
                self.exclude_ambiguous = f.readline().strip() == 'True'
        except FileNotFoundError:
            pass
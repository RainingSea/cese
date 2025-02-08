import random
import string

class PasswordGenerator:
    def __init__(self, length: int, include_upper: bool, include_lower: bool, include_numbers: bool, include_symbols: bool, exclude_ambiguous: bool):
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
            ambiguous_chars = 'il1Lo0O'
            character_pool = ''.join(c for c in character_pool if c not in ambiguous_chars)

        password = ''.join(random.choice(character_pool) for _ in range(self.length))
        return password

    def save_preferences(self) -> None:
        with open('user_preferences.txt', 'w') as file:
            file.write(f"{self.length}\n")
            file.write(f"{self.include_upper}\n")
            file.write(f"{self.include_lower}\n")
            file.write(f"{self.include_numbers}\n")
            file.write(f"{self.include_symbols}\n")
            file.write(f"{self.exclude_ambiguous}\n")

    def load_preferences(self) -> None:
        try:
            with open('user_preferences.txt', 'r') as file:
                self.length = int(file.readline().strip())
                self.include_upper = file.readline().strip() == 'True'
                self.include_lower = file.readline().strip() == 'True'
                self.include_numbers = file.readline().strip() == 'True'
                self.include_symbols = file.readline().strip() == 'True'
                self.exclude_ambiguous = file.readline().strip() == 'True'
        except FileNotFoundError:
            pass
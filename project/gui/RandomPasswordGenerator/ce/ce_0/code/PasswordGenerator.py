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
            characters = characters.translate(str.maketrans('', '', 'O0l1'))

        return ''.join(random.choice(characters) for _ in range(self.length))

    def save_password(self, password: str) -> None:
        with open('generated_passwords.txt', 'a') as f:
            f.write(password + '\n')

    def load_preferences(self) -> None:
        try:
            with open('user_preferences.txt', 'r') as f:
                preferences = f.read().strip().split('|')
                self.length = int(preferences[0])
                self.include_uppercase = preferences[1] == 'True'
                self.include_lowercase = preferences[2] == 'True'
                self.include_numbers = preferences[3] == 'True'
                self.include_symbols = preferences[4] == 'True'
                self.exclude_ambiguous = preferences[5] == 'True'
        except FileNotFoundError:
            pass

    def save_preferences(self) -> None:
        with open('user_preferences.txt', 'w') as f:
            f.write(f"{self.length}|{self.include_uppercase}|{self.include_lowercase}|"
                     f"{self.include_numbers}|{self.include_symbols}|{self.exclude_ambiguous}")
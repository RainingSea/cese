import random
import string

class PasswordGenerator:
    def __init__(self, length: int, include_uppercase: bool, 
                 include_lowercase: bool, include_numbers: bool, 
                 include_symbols: bool, exclude_ambiguous: bool):
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
            characters = ''.join(filter(lambda x: x not in 'il1Lo0O', characters))
        
        return ''.join(random.choice(characters) for _ in range(self.length))

    def save_generated_password(self, password: str) -> None:
        with open('generated_passwords.txt', 'a') as file:
            file.write(password + '\n')
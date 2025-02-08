import json

class UserPreferences:
    def __init__(self, length: int = 12, include_uppercase: bool = True, 
                 include_lowercase: bool = True, include_numbers: bool = True, 
                 include_symbols: bool = True, exclude_ambiguous: bool = False):
        self.length = length
        self.include_uppercase = include_uppercase
        self.include_lowercase = include_lowercase
        self.include_numbers = include_numbers
        self.include_symbols = include_symbols
        self.exclude_ambiguous = exclude_ambiguous

    def load_preferences(self) -> None:
        try:
            with open('user_preferences.txt', 'r') as file:
                data = file.read().strip().split('|')
                self.length = int(data[0])
                self.include_uppercase = data[1] == 'True'
                self.include_lowercase = data[2] == 'True'
                self.include_numbers = data[3] == 'True'
                self.include_symbols = data[4] == 'True'
                self.exclude_ambiguous = data[5] == 'True'
        except FileNotFoundError:
            self.save_user_preferences()

    def save_user_preferences(self) -> None:
        with open('user_preferences.txt', 'w') as file:
            file.write(f"{self.length}|{self.include_uppercase}|{self.include_lowercase}|"
                       f"{self.include_numbers}|{self.include_symbols}|{self.exclude_ambiguous}")
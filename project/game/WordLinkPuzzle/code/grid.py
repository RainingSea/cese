import random
from word_manager import WordManager

class Grid:
    def __init__(self):
        self.letters = self.generate_letters()
        self.word_manager = WordManager()

    def generate_letters(self):
        return [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(5)] for _ in range(5)]

    def connect_letters(self, selected: list) -> bool:
        word = ''.join(selected)
        if self.word_manager.validate_word(word):
            self.display()
            self.update_score(len(word))  # Update score based on word length
            return True
        else:
            with open('invalid_words.txt', 'a') as f:
                f.write(f'{word}\n')
            return False

    def display(self):
        # Code to render the grid on the screen
        # Placeholder for rendering logic
        pass

    def update_score(self, word_length: int):
        self.word_manager.update_score(word_length)
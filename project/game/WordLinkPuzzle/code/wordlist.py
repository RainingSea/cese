import pygame

class WordList:
    def __init__(self):
        self.words = []

    def add_word(self, word: str):
        if word not in self.words:  # Prevent duplicates
            self.words.append(word)

    def get_words(self) -> list:
        return self.words

    def clear_words(self):
        self.words.clear()  # Clear the list of formed words

    def display_words(self, screen):
        font = pygame.font.Font(None, 36)
        words_text = font.render("Words: " + "|".join(self.words), True, (0, 0, 0))
        screen.blit(words_text, (10, 50))  # Display formed words below the score
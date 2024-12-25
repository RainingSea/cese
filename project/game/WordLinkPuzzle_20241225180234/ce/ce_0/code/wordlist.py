class WordList:
    def __init__(self):
        self.words = set()

    def load_words(self, file_path: str):
        """Loads words from a specified file into the word set."""
        with open(file_path, 'r') as file:
            for line in file:
                self.words.add(line.strip())

    def is_valid_word(self, word: str) -> bool:
        """Checks if a word is valid by verifying its presence in the word set."""
        return word in self.words
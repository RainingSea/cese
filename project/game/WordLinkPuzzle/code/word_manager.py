class WordManager:
    def __init__(self):
        self.valid_words = []

    def validate_word(self, word: str) -> bool:
        return word in self.valid_words

    def load_words(self, file_path: str):
        with open(file_path, 'r') as f:
            self.valid_words = [line.strip() for line in f.readlines()]

    def update_score(self, word_length: int):
        # Assuming this method updates the score based on the word length
        pass
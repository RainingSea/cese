class WordList:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.words = self.load_words()

    def load_words(self) -> list[str]:
        with open(self.file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
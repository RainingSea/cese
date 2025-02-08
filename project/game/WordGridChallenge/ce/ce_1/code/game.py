from data_storage import DataStorage
from grid import Grid
from score import Score
from timer import Timer

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.timer = Timer()
        self.word_list = DataStorage.load_word_list()

    def start_game(self) -> None:
        self.grid.generate_grid(4)  # Example size
        self.timer.start_timer(60)   # 60 seconds timer

    def update_score(self, word: str) -> None:
        if self.check_word(word):
            self.score.add_score(len(word))  # Example scoring

    def check_word(self, word: str) -> bool:
        return word in self.word_list and word not in self.grid.found_words

    def end_game(self) -> None:
        player_name = input("Enter your name: ")
        DataStorage.save_score(player_name, self.score.get_score())
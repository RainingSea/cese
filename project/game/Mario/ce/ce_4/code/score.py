import os

class Score:
    def __init__(self):
        self.current_score = 0
        self.load_from_file()

    def increase_by(self, value: int) -> None:
        self.current_score += value

    def save_to_file(self) -> None:
        with open('scores.txt', 'w') as file:
            file.write(str(self.current_score))

    def load_from_file(self) -> None:
        if os.path.exists('scores.txt'):
            with open('scores.txt', 'r') as file:
                self.current_score = int(file.read().strip())
class Difficulty:
    def __init__(self):
        self.level = 1

    def set_difficulty(self, level: int):
        self.level = level

    def get_difficulty(self) -> int:
        return self.level
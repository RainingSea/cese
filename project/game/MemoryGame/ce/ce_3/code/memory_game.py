import random
from card import Card

class MemoryGame:
    def __init__(self):
        self.cards = []
        self.score = 0
        self.timer = 0.0
        self.game_over = False
        self.shuffle_cards()

    def shuffle_cards(self):
        faces = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']  # Example faces for pairs
        pairs = faces * 2  # Create pairs
        random.shuffle(pairs)
        self.cards = [Card(face) for face in pairs]

    def flip_card(self, index: int):
        if not self.cards[index].is_flipped and not self.game_over:
            self.cards[index].flip()

    def check_match(self, index1: int, index2: int) -> bool:
        return self.cards[index1].is_match(self.cards[index2])

    def reset_game(self):
        self.score = 0
        self.timer = 0.0
        self.game_over = False
        self.shuffle_cards()

    def update_timer(self):
        if not self.game_over:
            self.timer += 1.0  # This should be based on actual time in a real implementation

    def save_score(self, name: str):
        with open('high_scores.txt', 'a') as file:
            file.write(f"{name}|{self.score}\n")
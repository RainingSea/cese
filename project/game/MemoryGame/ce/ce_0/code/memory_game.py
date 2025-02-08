import random
import time
from card import Card

class MemoryGame:
    def __init__(self):
        self.cards = []
        self.score = 0
        self.timer = 0.0
        self.game_active = False

    def shuffle_cards(self) -> None:
        random.shuffle(self.cards)

    def flip_card(self, index: int) -> bool:
        if index < 0 or index >= len(self.cards):
            return False
        self.cards[index].flip()
        return True

    def check_match(self, card1: Card, card2: Card) -> bool:
        return card1.face == card2.face

    def update_score(self, time_taken: float) -> None:
        self.score += max(0, 100 - int(time_taken * 10))

    def restart_game(self) -> None:
        self.cards = []
        self.score = 0
        self.timer = 0.0
        self.game_active = True

    def save_score(self) -> None:
        with open('scores.txt', 'a') as score_file:
            score_file.write(f"{self.score}\n")
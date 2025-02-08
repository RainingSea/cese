import random
from card import Card

class Game:
    def __init__(self):
        self.cards = []
        self.score = 0
        self.timer = 0.0
        self.create_cards()

    def create_cards(self) -> None:
        values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] * 2  # 16 cards
        random.shuffle(values)
        self.cards = [Card(value) for value in values]

    def start_game(self) -> None:
        self.score = 0
        self.timer = 0.0
        self.create_cards()

    def flip_card(self, card: Card) -> None:
        card.flip()

    def check_match(self, card1: Card, card2: Card) -> bool:
        return card1.is_match(card2)

    def update_score(self) -> None:
        self.score += 1

    def restart_game(self) -> None:
        self.start_game()

    def save_score(self, player_name: str) -> None:
        with open('scores.txt', 'a') as file:
            file.write(f'{player_name}:{self.score}\n')
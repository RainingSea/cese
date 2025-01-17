import random
from card import Card

class Game:
    def __init__(self, num_pairs: int) -> None:
        self.cards = self._generate_cards(num_pairs)
        self.score = 0
        self.timer = 0.0

    def _generate_cards(self, num_pairs: int) -> list:
        images = [f'image_{i}.png' for i in range(num_pairs)] * 2
        random.shuffle(images)
        return [Card(image) for image in images]

    def start_game(self) -> None:
        self.score = 0
        self.timer = 0.0

    def flip_card(self, card: Card) -> None:
        card.flip()

    def check_match(self, card1: Card, card2: Card) -> bool:
        return card1.image == card2.image

    def restart_game(self) -> None:
        self.cards = self._generate_cards(len(self.cards) // 2)
        self.score = 0
        self.timer = 0.0

    def save_score(self, player_name: str) -> None:
        with open('scores.txt', 'a') as f:
            f.write(f'{player_name}:{self.score}\n')
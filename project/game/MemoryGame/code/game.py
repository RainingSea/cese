import random
from typing import List, Tuple

class Card:
    def __init__(self, value: str) -> None:
        self.value = value
        self.is_flipped = False

    def flip(self) -> None:
        self.is_flipped = not self.is_flipped

    def is_match(self, other: 'Card') -> bool:
        return self.value == other.value and self.is_flipped and other.is_flipped

class MemoryGame:
    def __init__(self) -> None:
        self.cards = []
        self.score = 0
        self.timer = 0.0
        self.game_active = False

    def start_game(self) -> None:
        self.cards = self.setup_cards()
        self.score = 0
        self.timer = 0.0
        self.game_active = True

    def restart_game(self) -> None:
        self.start_game()  # Start a new game

    def flip_card(self, index: int) -> bool:
        if index < 0 or index >= len(self.cards):
            return False
        self.cards[index].flip()  # Call flip method for the card
        return True

    def check_match(self, index1: int, index2: int) -> bool:
        if self.cards[index1].is_match(self.cards[index2]):
            self.update_score()
            return True
        return False

    def update_score(self) -> None:
        self.score += max(0, 100 - int(self.timer * 10))  # Update score based on time

    def save_score(self, player_name: str) -> None:
        with open('scores.txt', 'a') as file:
            file.write(f"{player_name}|{self.score}\n")

    def load_scores(self) -> List[Tuple[str, int]]:
        scores = []
        try:
            with open('scores.txt', 'r') as file:
                for line in file:
                    name, score = line.strip().split('|')
                    scores.append((name, int(score)))
        except FileNotFoundError:
            pass
        return scores

    def setup_cards(self) -> List[Card]:
        values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] * 2  # Example values
        random.shuffle(values)
        return [Card(value) for value in values]

    def update_timer(self, elapsed_time: float) -> None:
        self.timer = elapsed_time  # Update timer with elapsed time

    def handle_card_flip(self, index: int) -> None:
        if self.flip_card(index):
            # Check for matches if two cards are flipped
            flipped_cards = [i for i, card in enumerate(self.cards) if card.is_flipped]
            if len(flipped_cards) == 2:
                if self.check_match(flipped_cards[0], flipped_cards[1]):
                    print("It's a match!")
                else:
                    print("Not a match!")
                    # Flip cards back after a short delay (for demo purposes)
                    self.cards[flipped_cards[0]].flip()
                    self.cards[flipped_cards[1]].flip()
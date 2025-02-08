import pygame
import random
import time

class Card:
    def __init__(self, image: str) -> None:
        self.image = image
        self.is_face_up = False

    def flip(self) -> None:
        self.is_face_up = not self.is_face_up

    def is_match(self, other: 'Card') -> bool:
        return self.image == other.image


class Timer:
    def __init__(self) -> None:
        self.start_time = 0.0

    def start(self) -> None:
        self.start_time = time.time()

    def get_elapsed_time(self) -> float:
        return time.time() - self.start_time


class Game:
    def __init__(self) -> None:
        self.cards = []
        self.timer = Timer()
        self.score = 0

    def start_game(self, images: list) -> None:
        self.cards = [Card(image) for image in images] * 2
        random.shuffle(self.cards)
        self.timer.start()
        self.score = 0

    def flip_card(self, card: Card) -> None:
        card.flip()

    def check_match(self, card1: Card, card2: Card) -> bool:
        return card1.is_match(card2)

    def restart_game(self) -> None:
        self.cards.clear()
        self.score = 0

    def save_score(self) -> None:
        with open('high_scores.txt', 'a') as f:
            f.write(f"{self.score}\n")
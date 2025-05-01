import pygame
import random
import time

class Card:
    def __init__(self, image):
        self.image = image
        self.is_face_up = False

    def flip(self):
        self.is_face_up = not self.is_face_up

class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time

class Score:
    def __init__(self):
        self.points = 0

    def calculate_score(self, time):
        if time < 30:
            self.points = 100
        elif time < 60:
            self.points = 50
        else:
            self.points = 10
        return self.points

class Game:
    def __init__(self):
        self.cards = [Card(f"image_{i}.png") for i in range(8)] * 2  # 16 cards total
        self.timer = Timer()
        self.score = Score()
        self.flipped_cards = []
        self.matched_pairs = 0

    def start_game(self):
        random.shuffle(self.cards)
        self.timer.start()

    def flip_card(self, index):
        if not self.cards[index].is_face_up and len(self.flipped_cards) < 2:
            self.cards[index].flip()
            self.flipped_cards.append(index)
            if len(self.flipped_cards) == 2:
                if self.check_match():
                    self.matched_pairs += 1
                else:
                    pygame.time.delay(1000)  # Delay to show cards before flipping back
                    self.cards[self.flipped_cards[0]].flip()
                    self.cards[self.flipped_cards[1]].flip()
                self.flipped_cards = []

    def check_match(self):
        first_card = self.cards[self.flipped_cards[0]]
        second_card = self.cards[self.flipped_cards[1]]
        return first_card.image == second_card.image

    def restart_game(self):
        self.__init__()
        self.start_game()

    def update(self):
        # Update game state (e.g., check for win condition)
        if self.matched_pairs == len(self.cards) // 2:
            self.timer.stop()
            print("Game Over! Your score:", self.score.calculate_score(self.timer.elapsed_time))

    def render(self):
        # Render the game (placeholder for actual rendering code)
        pass
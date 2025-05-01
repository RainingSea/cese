import pygame
import random
import time

class Card:
    def __init__(self, image):
        self.image = image
        self.is_face_up = False

    def flip(self):
        self.is_face_up = not self.is_face_up

    def is_match(self, other):
        return self.image == other.image

class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.elapsed_time = time.time() - self.start_time

    def get_elapsed_time(self):
        return int(self.elapsed_time)

class Score:
    def __init__(self):
        self.points = 0

    def calculate_score(self, elapsed_time):
        return max(1000 - elapsed_time, 0)

    def save_score(self, player_name):
        with open('high_scores.txt', 'a') as f:
            f.write(f"{player_name}:{self.points}\n")

class Game:
    def __init__(self):
        self.cards = [Card(f"image_{i}.png") for i in range(8)] * 2  # 16 cards
        random.shuffle(self.cards)
        self.timer = Timer()
        self.score = Score()
        self.flipped_cards = []
        self.load_game_state()

    def start_game(self):
        self.timer.start()

    def restart_game(self):
        self.score.points = 0
        self.timer.start()
        self.shuffle_cards()

    def shuffle_cards(self):
        self.cards = [Card(f"image_{i}.png") for i in range(8)] * 2
        random.shuffle(self.cards)

    def flip_card(self, index):
        if not self.cards[index].is_face_up:
            self.cards[index].flip()
            self.flipped_cards.append(self.cards[index])
            if len(self.flipped_cards) == 2:
                self.check_match()

    def check_match(self):
        if len(self.flipped_cards) == 2:
            if self.flipped_cards[0].is_match(self.flipped_cards[1]):
                self.score.points += 10
            else:
                time.sleep(1)
                for card in self.flipped_cards:
                    card.flip()
            self.flipped_cards.clear()

    def update_display(self):
        # Placeholder for UI update logic
        for index, card in enumerate(self.cards):
            if card.is_face_up:
                # Logic to draw the card face up
                print(f"Card {index} is face up with image {card.image}")
            else:
                # Logic to draw the card face down
                print(f"Card {index} is face down")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            card_index = self.get_card_index(mouse_x, mouse_y)
            if card_index is not None:
                self.flip_card(card_index)

    def get_card_index(self, mouse_x, mouse_y):
        card_width = 100  # Example card width
        card_height = 100  # Example card height
        grid_width = 4  # 4 cards in a row
        index_x = mouse_x // card_width
        index_y = mouse_y // card_height
        if index_x < grid_width and index_y < 4:  # Assuming 4 rows
            return index_y * grid_width + index_x
        return None

    def load_game_state(self):
        try:
            with open('game_state.txt', 'r') as f:
                data = f.read().splitlines()
                self.score.points = int(data[0].split(':')[1])
                self.timer.elapsed_time = int(data[1].split(':')[1])
        except FileNotFoundError:
            self.score.points = 0
            self.timer.elapsed_time = 0
            self.timer.start()  # Start timer if no previous state

    def save_game_state(self):
        self.timer.stop()  # Ensure timer is stopped before saving
        with open('game_state.txt', 'w') as f:
            f.write(f"score:{self.score.points}\n")
            f.write(f"elapsed_time:{self.timer.get_elapsed_time()}\n")
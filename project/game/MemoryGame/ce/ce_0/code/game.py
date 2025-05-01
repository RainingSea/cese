import pygame
import random
import time
import json

class Card:
    def __init__(self, image):
        self.image = image
        self.is_face_up = False

    def flip(self):
        self.is_face_up = not self.is_face_up

    def is_match(self, other):
        return self.image == other.image

class Game:
    def __init__(self):
        self.cards = []
        self.score = 0
        self.timer = 0
        self.load_settings()
        self.shuffle_cards()

    def load_settings(self):
        try:
            with open('settings.txt', 'r') as file:
                self.settings = file.read()
        except FileNotFoundError:
            self.settings = "Default settings"

    def shuffle_cards(self):
        images = ['image1.png', 'image2.png', 'image3.png', 'image4.png'] * 2
        random.shuffle(images)
        self.cards = [Card(image) for image in images]

    def flip_card(self, index):
        if not self.cards[index].is_face_up:
            self.cards[index].flip()

    def check_match(self):
        flipped_cards = [card for card in self.cards if card.is_face_up]
        if len(flipped_cards) == 2:
            if flipped_cards[0].is_match(flipped_cards[1]):
                self.score += 1
            else:
                time.sleep(1)
                for card in flipped_cards:
                    card.flip()

    def restart(self):
        self.score = 0
        self.timer = 0
        self.shuffle_cards()
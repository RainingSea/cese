import pygame

class Score:
    def __init__(self):
        self.current_score = 0

    def update_score(self, points: int):
        self.current_score += points

    def display(self):
        # Logic to display the score on the screen
        pass
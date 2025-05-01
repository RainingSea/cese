import pygame
import random

class Grid:
    def __init__(self):
        self.letters = []

    def generate_grid(self, size: int):
        self.letters = [[random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size)] for _ in range(size)]

    def display_grid(self):
        # Logic to render the grid to the GUI
        pass
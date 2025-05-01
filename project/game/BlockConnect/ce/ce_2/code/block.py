import random

class Block:
    def __init__(self):
        self.color = self.get_random_color()

    def get_random_color(self):
        colors = ['red', 'green', 'blue', 'yellow']
        return random.choice(colors)

    def draw(self):
        # Logic to draw the block on the screen
        pass
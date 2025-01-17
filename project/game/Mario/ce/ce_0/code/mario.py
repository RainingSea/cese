import pygame

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        self.width = 50
        self.height = 50

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def jump(self):
        pass  # Jump logic to be implemented

    def hit_block(self):
        pass  # Block hit logic to be implemented

    def touch_mushroom(self):
        self.score += 100

    def touch_enemy(self):
        self.score -= 50  # Penalty for touching enemy

    def reach_flagpole(self):
        pass  # Logic for reaching flagpole

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height))
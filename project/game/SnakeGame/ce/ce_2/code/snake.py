import pygame

class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = 'RIGHT'

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'RIGHT':
            head_x += 10
        elif self.direction == 'LEFT':
            head_x -= 10
        elif self.direction == 'UP':
            head_y -= 10
        elif self.direction == 'DOWN':
            head_y += 10
        self.body.insert(0, (head_x, head_y))
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])  # Add a new segment at the tail

    def get_head_position(self):
        return self.body[0]

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(segment[0], segment[1], 10, 10))
import pygame

class Segment:
    def __init__(self, position):
        self.position = position

class Snake:
    def __init__(self):
        self.segments = [Segment((100, 100))]
        self.direction = 'RIGHT'

    def move(self):
        head_x, head_y = self.segments[0].position
        if self.direction == 'UP':
            head_y -= 10
        elif self.direction == 'DOWN':
            head_y += 10
        elif self.direction == 'LEFT':
            head_x -= 10
        elif self.direction == 'RIGHT':
            head_x += 10
        new_head = Segment((head_x, head_y))
        self.segments.insert(0, new_head)
        self.segments.pop()

    def grow(self):
        tail = self.segments[-1]
        self.segments.append(Segment(tail.position))

    def check_self_collision(self):
        head = self.segments[0]
        return any(segment.position == head.position for segment in self.segments[1:])

    def draw(self, screen):
        for segment in self.segments:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(segment.position[0], segment.position[1], 10, 10))
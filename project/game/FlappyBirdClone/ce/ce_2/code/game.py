import pygame
import random

class Bird:
    def __init__(self):
        self.position_y = 300
        self.velocity_y = 0

    def flap(self):
        self.velocity_y = -10

    def update(self):
        self.velocity_y += 1  # Gravity
        self.position_y += self.velocity_y

class Pipe:
    def __init__(self, position_x):
        self.position_x = position_x
        self.gap_y = random.randint(100, 300)

    def update(self):
        self.position_x -= 5  # Move left

    def is_off_screen(self):
        return self.position_x < -50

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.high_score = self.load_high_score()

    def start(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.flap()

            self.update()
            self.render()
            clock.tick(30)

    def update(self):
        self.bird.update()
        if random.randint(1, 100) < 2:  # Randomly generate pipes
            self.pipes.append(Pipe(800))
        for pipe in self.pipes:
            pipe.update()
            if pipe.is_off_screen():
                self.pipes.remove(pipe)
                self.score += 1  # Increment score for passing a pipe
        self.check_collision()

    def render(self):
        # Placeholder for rendering logic
        pass

    def check_collision(self):
        # Placeholder for collision detection logic
        pass

    def restart(self):
        self.score = 0
        self.pipes.clear()
        self.bird.position_y = 300
        self.bird.velocity_y = 0

    def save_high_score(self):
        with open('scores.txt', 'a') as file:
            file.write(f"{self.high_score}\n")

    def load_high_score(self):
        try:
            with open('scores.txt', 'r') as file:
                scores = [int(line.strip()) for line in file.readlines()]
                return max(scores) if scores else 0
        except FileNotFoundError:
            return 0
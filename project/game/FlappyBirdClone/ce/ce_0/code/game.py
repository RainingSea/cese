import pygame
import random

class Bird:
    def __init__(self):
        self.position = [100, 250]
        self.velocity = 0

    def flap(self):
        self.velocity = -10

    def update(self):
        self.velocity += 0.5  # Gravity effect
        self.position[1] += self.velocity

class Pipe:
    def __init__(self, gap_position):
        self.position = [400, 0]
        self.gap_position = gap_position

    def move(self):
        self.position[0] -= 5  # Move left

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0], self.position[1], 50, self.gap_position))
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0], self.gap_position + 150, 50, 400))

class Score:
    def __init__(self):
        self.current_score = 0
        self.high_score = self.load_high_score()

    def increment(self):
        self.current_score += 1

    def save_high_score(self):
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            with open('highscore.txt', 'w') as f:
                f.write(str(self.high_score))

    def load_high_score(self):
        try:
            with open('highscore.txt', 'r') as f:
                return int(f.read().strip())
        except FileNotFoundError:
            return 0

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = Score()
        self.running = True
        self.clock = pygame.time.Clock()

    def start(self):
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(60)

    def update(self):
        self.bird.update()
        if random.randint(1, 100) < 5:  # Randomly generate pipes
            gap_position = random.randint(100, 300)
            self.pipes.append(Pipe(gap_position))
        for pipe in self.pipes:
            pipe.move()
            if pipe.position[0] < -50:
                self.pipes.remove(pipe)
                self.score.increment()

        self.check_collision()

    def draw(self):
        screen = pygame.display.set_mode((400, 600))
        screen.fill((135, 206, 250))  # Sky blue
        pygame.draw.circle(screen, (255, 255, 0), (self.bird.position[0], self.bird.position[1]), 20)  # Bird
        for pipe in self.pipes:
            pipe.draw(screen)
        pygame.display.flip()

    def check_collision(self):
        if self.bird.position[1] > 580:  # Ground collision
            self.restart()
        for pipe in self.pipes:
            if (self.bird.position[0] + 20 > pipe.position[0] and self.bird.position[0] - 20 < pipe.position[0] + 50 and
                (self.bird.position[1] < pipe.gap_position or self.bird.position[1] > pipe.gap_position + 150)):
                self.restart()

    def restart(self):
        self.bird = Bird()
        self.pipes.clear()
        self.score.current_score = 0
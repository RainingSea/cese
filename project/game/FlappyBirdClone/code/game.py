import pygame
import random

class Bird:
    def __init__(self):
        self.position = [100, 250]  # Initial position of the bird
        self.velocity = 0  # Initial velocity

    def flap(self):
        self.velocity = -10  # Sets upward velocity on flap

    def update(self):
        self.velocity += 1  # Gravity effect
        self.position[1] += self.velocity  # Update bird's vertical position
        self.check_boundaries()  # Ensure bird stays within boundaries

    def check_boundaries(self):
        if self.position[1] > Game.FLOOR_LEVEL:
            self.position[1] = Game.FLOOR_LEVEL
        elif self.position[1] < Game.CEILING_LEVEL:
            self.position[1] = Game.CEILING_LEVEL

class Pipe:
    def __init__(self):
        self.x = 800
        self.gap_y = random.randint(100, 400)

    def move(self):
        self.x -= 5  # Move left

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, 50, self.gap_y))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.gap_y + 150, 50, 600 - self.gap_y - 150))

class Score:
    def __init__(self):
        self.current_score = 0  # Initialize current score to 0
        self.high_score = self.load_high_score()  # Load existing high score

    def increment(self):
        self.current_score += 1  # Increment current score by 1

    def save_high_score(self):
        if self.current_score > self.high_score:
            self.high_score = self.current_score  # Update high score
            with open('scores.txt', 'w') as file:
                file.write(str(self.high_score))  # Save high score into file

    def load_high_score(self):
        try:
            with open('scores.txt', 'r') as file:
                return int(file.read().strip())  # Load and return high score
        except FileNotFoundError:
            return 0  # Return 0 if file not found

class Game:
    FLOOR_LEVEL = 600
    CEILING_LEVEL = 0

    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = Score()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

    def start_game(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(30)
        self.score.save_high_score()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.flap()

    def update(self):
        self.bird.update()
        if len(self.pipes) == 0 or self.pipes[-1].x < 600:
            self.pipes.append(Pipe())
        for pipe in self.pipes:
            pipe.move()
        self.check_collisions()
        self.pipes = [pipe for pipe in self.pipes if pipe.x > -50]  # Filter out pipes that are out of bounds

    def check_collisions(self):
        for pipe in self.pipes:
            if (self.bird.position[0] + 30 > pipe.x and self.bird.position[0] < pipe.x + 50 and
                (self.bird.position[1] < pipe.gap_y or self.bird.position[1] + 30 > pipe.gap_y + 150)):
                self.restart_game()
        if self.bird.position[1] > self.FLOOR_LEVEL or self.bird.position[1] < self.CEILING_LEVEL:
            self.restart_game()

    def render(self):
        self.screen.fill((135, 206, 235))  # Sky blue
        pygame.draw.circle(self.screen, (255, 255, 0), (self.bird.position[0], self.bird.position[1]), 15)  # Bird
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.display_score()
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score.current_score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def restart_game(self):
        if self.score.current_score > self.score.high_score:
            self.score.high_score = self.score.current_score
            self.score.save_high_score()
        self.score.current_score = 0
        self.pipes.clear()
        self.bird.position[1] = 250  # Reset bird's vertical position
        self.bird.velocity = 0  # Reset bird's velocity
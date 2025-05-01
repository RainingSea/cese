import pygame
import random
import time

class Player:
    def __init__(self):
        self.position = [300, 550]  # Starting position of the player
        self.width = 20
        self.height = 20

    def move_left(self):
        if self.position[0] > 0:
            self.position[0] -= 5

    def move_right(self):
        if self.position[0] < 600 - self.width:  # Assuming screen width is 600
            self.position[0] += 5

class Block:
    def __init__(self):
        self.position = [random.randint(0, 580), 0]  # Random x position at the top
        self.speed = random.randint(3, 7)  # Random speed between 3 and 7
        self.width = 20
        self.height = 20

    def fall(self):
        self.position[1] += self.speed

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_scores = []
        self.load_scores()

    def update_score(self):
        self.score += 1  # Increment score for each update (time survived)

    def save_score(self, player_name: str):
        with open('highscores.txt', 'a') as file:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            file.write(f"{player_name}|{self.score}|{timestamp}\n")

    def load_scores(self):
        try:
            with open('highscores.txt', 'r') as file:
                self.high_scores = file.readlines()
        except FileNotFoundError:
            self.high_scores = []

class Game:
    def __init__(self):
        self.player = Player()
        self.blocks = []
        self.score_manager = ScoreManager()
        self.running = True
        self.clock = pygame.time.Clock()

    def start(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.check_collision()
            self.clock.tick(30)  # Limit to 30 frames per second

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

    def update(self):
        if random.randint(1, 20) == 1:  # Randomly generate blocks
            self.blocks.append(Block())
        for block in self.blocks[:]:  # Iterate over a copy of the list
            block.fall()
            if block.position[1] > 600:  # Remove block if it falls below the screen
                self.blocks.remove(block)
                self.score_manager.update_score()  # Increment score for each block that falls

    def render(self):
        screen = pygame.display.set_mode((600, 600))
        screen.fill((0, 0, 0))  # Clear screen with black
        pygame.draw.rect(screen, (0, 255, 0), (*self.player.position, self.player.width, self.player.height))  # Draw player
        for block in self.blocks:
            pygame.draw.rect(screen, (255, 0, 0), (*block.position, block.width, block.height))  # Draw blocks
        score_text = pygame.font.SysFont('Arial', 25).render(f'Score: {self.score_manager.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def check_collision(self):
        player_rect = pygame.Rect(*self.player.position, self.player.width, self.player.height)
        for block in self.blocks:
            block_rect = pygame.Rect(*block.position, block.width, block.height)
            if player_rect.colliderect(block_rect):
                self.running = False  # End game on collision
                self.score_manager.save_score("Player")  # Save score with a default player name
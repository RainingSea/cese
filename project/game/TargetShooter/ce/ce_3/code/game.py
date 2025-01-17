import pygame
import random
from leaderboard import Leaderboard

class Target:
    def __init__(self):
        self.position = (random.randint(0, 800), random.randint(0, 600))
        self.is_hit = False

    def move(self):
        # Logic to move the target can be implemented here
        pass

    def draw(self, screen):
        if not self.is_hit:
            pygame.draw.circle(screen, (255, 0, 0), self.position, 20)

class Game:
    def __init__(self):
        self.score = 0
        self.time_limit = 30  # 30 seconds
        self.targets = []
        self.leaderboard = Leaderboard()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Target Shooter")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def start_game(self):
        self.targets = [Target() for _ in range(5)]
        self.run_game_loop()

    def run_game_loop(self):
        start_ticks = pygame.time.get_ticks()
        running = True
        while running:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # Calculate elapsed time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_target_hit(pygame.mouse.get_pos())

            self.update()
            self.draw()
            if seconds >= self.time_limit:
                running = False
            
            self.clock.tick(60)  # Limit to 60 frames per second

        self.restart()

    def check_target_hit(self, mouse_pos):
        for target in self.targets:
            if not target.is_hit and pygame.math.Vector2(target.position).distance_to(mouse_pos) < 20:
                target.is_hit = True
                self.score += 1

    def update(self):
        # Update game logic here
        pass

    def draw(self):
        self.screen.fill((255, 255, 255))  # Clear screen with white
        for target in self.targets:
            target.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def restart(self):
        self.leaderboard.update_score("Player", self.score)  # Placeholder for player name
        self.leaderboard.save_scores()
        pygame.quit()
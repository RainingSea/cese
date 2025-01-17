import pygame
from target import Target
from leaderboard import Leaderboard

class Game:
    def __init__(self):
        self.score = 0
        self.time_left = 60
        self.targets = []
        self.is_running = True
        self.leaderboard = Leaderboard()
        self.spawn_target()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        while self.is_running:
            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def update(self):
        self.time_left -= 1/60
        for target in self.targets:
            target.move()
            if target.y > 600:
                self.targets.remove(target)
                self.spawn_target()

    def draw(self, screen):
        screen.fill((255, 255, 255))
        for target in self.targets:
            target.draw(screen)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        timer_text = font.render(f'Time Left: {int(self.time_left)}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (10, 50))

    def restart(self):
        self.score = 0
        self.time_left = 60
        self.targets.clear()
        self.spawn_target()

    def calculate_score(self, hit: bool):
        if hit:
            self.score += 1

    def spawn_target(self):
        x = random.randint(0, 780)
        y = random.randint(-100, -40)
        speed = random.randint(1, 5)
        self.targets.append(Target(x, y, speed))
import pygame
from target import Target
from leaderboard import Leaderboard

class Game:
    def __init__(self):
        self.score = 0
        self.time_limit = 30
        self.targets = []
        self.leaderboard = Leaderboard()
        self.leaderboard.load_scores()

    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Target Shooter")
        self.clock = pygame.time.Clock()
        self.run_game()

    def run_game(self):
        running = True
        while running:
            self.screen.fill((255, 255, 255))
            self.handle_events()
            self.update_targets()
            self.draw_targets()
            self.draw_score()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.shoot_target(event.pos)

    def shoot_target(self, position):
        for target in self.targets:
            if target.x - 20 < position[0] < target.x + 20 and target.y - 20 < position[1] < target.y + 20:
                self.update_score(10)
                self.targets.remove(target)

    def update_score(self, points: int):
        self.score += points

    def restart_game(self):
        self.score = 0
        self.targets.clear()

    def update_targets(self):
        if len(self.targets) < 5:
            new_target = Target(random.randint(0, 780), 0, random.randint(1, 3))
            self.targets.append(new_target)

        for target in self.targets:
            target.move()
            if target.y > 600:
                self.targets.remove(target)

    def draw_targets(self):
        for target in self.targets:
            target.draw(self.screen)

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
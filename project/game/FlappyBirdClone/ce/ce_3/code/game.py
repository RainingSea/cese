import pygame
from bird import Bird
from pipe import Pipe

class Game:
    def __init__(self):
        self.bird = Bird(100, 250)
        self.pipes = []
        self.score = 0
        self.high_score = self.load_high_score()
        self.create_pipes()

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((400, 600))
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bird.flap()

            self.update()
            self.draw(screen)
            clock.tick(60)

        self.save_high_score()
        pygame.quit()

    def update(self) -> None:
        self.bird.fall()
        for pipe in self.pipes:
            pipe.move()
            if pipe.x + pipe.width < 0:
                self.pipes.remove(pipe)
                self.score += 1

        if self.check_collision():
            self.restart()

    def draw(self, screen) -> None:
        screen.fill((135, 206, 250))  # Sky color
        pygame.draw.rect(screen, (255, 255, 0), self.bird.get_rect())  # Bird color

        for pipe in self.pipes:
            pygame.draw.rect(screen, (0, 255, 0), pipe.get_rect()[0])  # Top pipe color
            pygame.draw.rect(screen, (0, 255, 0), pipe.get_rect()[1])  # Bottom pipe color

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        high_score_text = font.render(f'High Score: {self.high_score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))
        pygame.display.flip()

    def check_collision(self) -> bool:
        bird_rect = self.bird.get_rect()
        for pipe in self.pipes:
            if bird_rect.colliderect(pipe.get_rect()[0]) or bird_rect.colliderect(pipe.get_rect()[1]):
                return True
        return False

    def restart(self) -> None:
        self.bird = Bird(100, 250)
        self.pipes.clear()
        self.score = 0
        self.create_pipes()

    def create_pipes(self) -> None:
        for i in range(1, 4):
            height = random.randint(150, 400)
            gap = 150
            self.pipes.append(Pipe(400 + i * 200, height, gap))

    def load_high_score(self) -> int:
        try:
            with open('highscore.txt', 'r') as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self) -> None:
        if self.score > self.high_score:
            self.high_score = self.score
            with open('highscore.txt', 'w') as file:
                file.write(str(self.high_score))
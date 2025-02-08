import pygame
from bird import Bird
from pipe import Pipe
from score_manager import ScoreManager

class Game:
    def __init__(self):
        self.bird = Bird(200)
        self.pipes = []
        self.score = 0
        self.high_score = 0
        self.score_manager = ScoreManager()
        self.spawn_pipe()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 600))
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
            self.draw(screen)
            clock.tick(60)

        pygame.quit()

    def update(self):
        self.bird.fall()
        for pipe in self.pipes:
            if pipe.get_position() < -50:
                self.pipes.remove(pipe)
                self.score += 1
        self.check_collision()

    def draw(self, screen):
        screen.fill((135, 206, 235))  # Sky color
        pygame.draw.circle(screen, (255, 255, 0), (100, int(self.bird.get_position())), 15)  # Draw bird
        for pipe in self.pipes:
            pygame.draw.rect(screen, (0, 255, 0), (pipe.get_position(), 0, 50, 600 - pipe.gap_height))  # Draw upper pipe
            pygame.draw.rect(screen, (0, 255, 0), (pipe.get_position(), 600 - pipe.gap_height + 150, 50, 600))  # Draw lower pipe
        pygame.display.flip()

    def check_collision(self) -> bool:
        bird_rect = pygame.Rect(100 - 15, self.bird.get_position() - 15, 30, 30)
        for pipe in self.pipes:
            pipe_rect_upper = pygame.Rect(pipe.get_position(), 0, 50, 600 - pipe.gap_height)
            pipe_rect_lower = pygame.Rect(pipe.get_position(), 600 - pipe.gap_height + 150, 50, 600)
            if bird_rect.colliderect(pipe_rect_upper) or bird_rect.colliderect(pipe_rect_lower):
                return True
        return False

    def restart(self):
        self.bird = Bird(200)
        self.pipes.clear()
        self.score = 0
        self.spawn_pipe()

    def spawn_pipe(self):
        gap_height = random.randint(100, 300)
        new_pipe = Pipe(400, gap_height)
        self.pipes.append(new_pipe)
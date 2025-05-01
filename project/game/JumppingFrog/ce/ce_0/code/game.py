import pygame
import random

class Frog:
    def __init__(self, x, y, jump_height):
        self.x = x
        self.y = y
        self.jump_height = jump_height

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def jump(self):
        self.y -= self.jump_height

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move(self):
        self.x += random.choice([-1, 1])  # Move left or right randomly

class Game:
    def __init__(self):
        self.frog = Frog(100, 400, 50)
        self.platforms = [Platform(random.randint(0, 800), random.randint(100, 300), 100, 10) for _ in range(5)]
        self.score = 0
        self.timer = 60  # 60 seconds timer

    def start_game(self):
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Jumping Frog Game")
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.frog.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.frog.move_right()
                    if event.key == pygame.K_SPACE:
                        self.frog.jump()

            self.update()
            self.render(screen)
            clock.tick(60)

        self.reset_game()

    def update(self):
        self.timer -= 1 / 60  # Decrease timer
        if self.timer <= 0:
            self.reset_game()

    def render(self, screen):
        screen.fill((0, 0, 255))  # Background color
        pygame.draw.rect(screen, (0, 255, 0), (self.frog.x, self.frog.y, 50, 50))  # Draw frog

        for platform in self.platforms:
            pygame.draw.rect(screen, (255, 0, 0), (platform.x, platform.y, platform.width, platform.height))  # Draw platforms

        # Display score and timer
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        timer_text = font.render(f'Timer: {int(self.timer)}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (10, 50))

        pygame.display.flip()

    def check_collision(self):
        for platform in self.platforms:
            if (self.frog.x < platform.x + platform.width and
                self.frog.x + 50 > platform.x and
                self.frog.y + 50 > platform.y and
                self.frog.y < platform.y + platform.height):
                self.score += 1
                self.frog.y = platform.y - 50  # Reset frog position on platform

    def reset_game(self):
        self.frog = Frog(100, 400, 50)
        self.platforms = [Platform(random.randint(0, 800), random.randint(100, 300), 100, 10) for _ in range(5)]
        self.score = 0
        self.timer = 60
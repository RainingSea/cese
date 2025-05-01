import pygame
import random

class Player:
    def __init__(self):
        self.position_x = 300

    def move_left(self):
        if self.position_x > 0:
            self.position_x -= 10

    def move_right(self):
        if self.position_x < 580:  # Assuming screen width is 600
            self.position_x += 10

class Block:
    def __init__(self):
        self.position_x = random.randint(0, 580)
        self.position_y = 0
        self.speed = 5

    def fall(self):
        self.position_y += self.speed

    def reset_position(self):
        self.position_y = 0
        self.position_x = random.randint(0, 580)

class Game:
    def __init__(self):
        self.player = Player()
        self.blocks = [Block() for _ in range(5)]
        self.score = 0
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Dodge the Falling Blocks")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def start(self):
        running = True
        while running:
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.check_collision()
            self.display_score()
            pygame.display.flip()
            self.clock.tick(60)

    def update(self):
        self.screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        for block in self.blocks:
            block.fall()
            if block.position_y > 600:
                block.reset_position()
                self.score += 1  # Increment score for each block that goes off-screen
            pygame.draw.rect(self.screen, (255, 0, 0), (block.position_x, block.position_y, 20, 20))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.player.position_x, 550, 20, 20))

    def check_collision(self):
        player_rect = pygame.Rect(self.player.position_x, 550, 20, 20)
        for block in self.blocks:
            block_rect = pygame.Rect(block.position_x, block.position_y, 20, 20)
            if player_rect.colliderect(block_rect):
                self.save_score()
                pygame.quit()

    def display_score(self):
        score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

    def save_score(self):
        with open('scores.txt', 'r') as file:
            high_score = int(file.readline().strip())
        if self.score > high_score:
            with open('scores.txt', 'w') as file:
                file.write(str(self.score))
import pygame
import random

class Player:
    def __init__(self, x: int, width: int, height: int):
        self.position_x = x
        self.width = width
        self.height = height

    def move(self, direction: str):
        if direction == 'left':
            self.position_x -= 5
        elif direction == 'right':
            self.position_x += 5

class Block:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.position_x = x
        self.position_y = y
        self.width = width
        self.height = height

    def fall(self, speed: float):
        self.position_y += speed

class Game:
    def __init__(self):
        self.player = Player(300, 50, 50)
        self.blocks = []
        self.score = 0
        self.speed = 5

    def run_game(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player.position_x > 0:
                self.player.move('left')
            if keys[pygame.K_RIGHT] and self.player.position_x < 550:
                self.player.move('right')

            self.spawn_block()
            self.update_blocks()
            self.check_collision()

            screen.fill((0, 0, 0))
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def spawn_block(self):
        if random.randint(1, 20) == 1:
            new_block = Block(random.randint(0, 550), 0, 50, 50)
            self.blocks.append(new_block)

    def update_blocks(self):
        for block in self.blocks:
            block.fall(self.speed)

    def check_collision(self) -> bool:
        for block in self.blocks:
            if (self.player.position_x < block.position_x + block.width and
                self.player.position_x + self.player.width > block.position_x and
                block.position_y + block.height > 550):
                self.end_game()
                return True
        return False

    def update_score(self):
        self.score += 1

    def end_game(self):
        self.save_high_score()
        pygame.quit()

    def save_high_score(self):
        with open('high_scores.txt', 'a') as f:
            f.write(f'score: {self.score}\n')

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.player.position_x, 550, self.player.width, self.player.height))
        for block in self.blocks:
            pygame.draw.rect(screen, (255, 0, 0), (block.position_x, block.position_y, block.width, block.height))
import pygame
import random

class Block:
    def __init__(self, x_position: int, width: int, height: int):
        self.x_position = x_position
        self.y_position = 0  # Start at the top of the screen
        self.width = width
        self.height = height

    def fall(self, speed: int):
        self.y_position += speed

class Character:
    def __init__(self, x_position: int, width: int, height: int):
        self.x_position = x_position
        self.width = width
        self.height = height

    def move(self, direction: str):
        if direction == "left":
            self.x_position -= 10
        elif direction == "right":
            self.x_position += 10

class Game:
    def __init__(self):
        self.character = Character(300, 50, 50)  # Centered at the bottom
        self.falling_blocks = []
        self.score = 0
        self.is_running = True

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        clock = pygame.time.Clock()

        while self.is_running:
            self.handle_events()
            self.spawn_block()
            self.update_blocks()
            self.check_collision()
            self.render(screen)
            clock.tick(30)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.character.move("left")
                elif event.key == pygame.K_RIGHT:
                    self.character.move("right")

    def spawn_block(self):
        if random.randint(1, 30) == 1:  # Randomly spawn blocks
            new_block = Block(random.randint(0, 550), 50, 50)
            self.falling_blocks.append(new_block)

    def update_blocks(self):
        for block in self.falling_blocks:
            block.fall(5)  # Fall speed

    def check_collision(self) -> bool:
        for block in self.falling_blocks:
            if (self.character.x_position < block.x_position + block.width and
                    self.character.x_position + self.character.width > block.x_position and
                    block.y_position + block.height > 350):  # Assuming character is at y=350
                self.score += 1
                self.falling_blocks.remove(block)
                break

    def render(self, screen):
        screen.fill((255, 255, 255))  # Clear screen
        pygame.draw.rect(screen, (0, 0, 255), (self.character.x_position, 350, self.character.width, self.character.height))
        for block in self.falling_blocks:
            pygame.draw.rect(screen, (255, 0, 0), (block.x_position, block.y_position, block.width, block.height))
        pygame.display.flip()
import pygame
import random

class Block:
    def __init__(self, x_position: int, y_position: int):
        self.x_position = x_position
        self.y_position = y_position
        self.width = random.randint(20, 50)
        self.height = random.randint(20, 50)

    def fall(self, speed: int):
        self.y_position += speed

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.x_position, self.y_position, self.width, self.height))


class Player:
    def __init__(self, x_position: int):
        self.x_position = x_position
        self.width = 50
        self.height = 50

    def move(self, direction: str):
        if direction == 'left':
            self.x_position -= 5
        elif direction == 'right':
            self.x_position += 5

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (0, 0, 255), (self.x_position, 550, self.width, self.height))


class Game:
    def __init__(self):
        self.player = Player(375)
        self.blocks = []
        self.score = 0
        self.game_speed = 5
        self.spawn_block()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move('left')
            if keys[pygame.K_RIGHT]:
                self.player.move('right')

            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        self.save_score()
        pygame.quit()

    def update(self):
        for block in self.blocks:
            block.fall(self.game_speed)
            if block.y_position > 600:
                self.blocks.remove(block)
                self.score += 1
        if random.randint(1, 20) == 1:
            self.spawn_block()

        self.check_collision()

    def check_collision(self) -> bool:
        for block in self.blocks:
            if (self.player.x_position < block.x_position + block.width and
                self.player.x_position + self.player.width > block.x_position and
                550 < block.y_position + block.height):
                return True
        return False

    def draw(self, surface: pygame.Surface):
        surface.fill((255, 255, 255))
        self.player.draw(surface)
        for block in self.blocks:
            block.draw(surface)

    def spawn_block(self):
        x_position = random.randint(0, 750)
        new_block = Block(x_position, 0)
        self.blocks.append(new_block)

    def save_score(self):
        with open('scores.txt', 'a') as file:
            file.write(f"{self.score}\n")
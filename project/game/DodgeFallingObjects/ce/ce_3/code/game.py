import pygame
import random
import time

class Character:
    def __init__(self, x: int, y: int):
        self.x_position = x
        self.y_position = y

    def move_left(self):
        self.x_position -= 10

    def move_right(self):
        self.x_position += 10

class Block:
    def __init__(self, x: int, y: int, speed: int):
        self.x_position = x
        self.y_position = y
        self.speed = speed

    def fall(self):
        self.y_position += self.speed

class Game:
    def __init__(self):
        self.character = Character(300, 550)
        self.blocks = []
        self.score = 0
        self.game_speed = 5
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Dodge the Falling Blocks')
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            self.update()
            self.draw()
            running = self.check_events()
            self.clock.tick(60)

    def update(self):
        if random.randint(1, 20) == 1:
            new_block = Block(random.randint(0, 580), 0, self.game_speed)
            self.blocks.append(new_block)

        for block in self.blocks:
            block.fall()
            if block.y_position > 600:
                self.blocks.remove(block)
                self.score += 1

        self.check_collision()

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 0, 0), (self.character.x_position, self.character.y_position, 40, 40))
        for block in self.blocks:
            pygame.draw.rect(self.screen, (0, 255, 0), (block.x_position, block.y_position, 40, 40))
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        pygame.display.flip()

    def check_collision(self):
        for block in self.blocks:
            if (self.character.x_position < block.x_position + 40 and
                self.character.x_position + 40 > block.x_position and
                self.character.y_position < block.y_position + 40 and
                self.character.y_position + 40 > block.y_position):
                self.game_over()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.character.move_left()
                if event.key == pygame.K_RIGHT:
                    self.character.move_right()
        return True

    def game_over(self):
        with open('scores.txt', 'a') as f:
            f.write(f'{self.score}|{time.ctime()}\n')
        pygame.quit()
        exit()
import pygame
import random

class Game:
    def __init__(self):
        self.mario = Mario(100, 300)
        self.blocks = [Block(150, 250), Block(300, 250)]
        self.mushrooms = []
        self.enemies = [Enemy(400, 300)]
        self.score = Score()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.handle_collisions()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.mario.move_left()
        if keys[pygame.K_RIGHT]:
            self.mario.move_right()
        if keys[pygame.K_SPACE]:
            self.mario.jump()

    def update(self):
        for mushroom in self.mushrooms:
            mushroom.fall()
            mushroom.move_left()
        for enemy in self.enemies:
            enemy.move_randomly()

    def handle_collisions(self):
        for block in self.blocks:
            if self.mario.x in range(block.x, block.x + 50) and self.mario.y >= block.y:
                self.mario.hit_block()
                self.mushrooms.append(block.release_mushroom())
        for mushroom in self.mushrooms:
            if self.mario.x in range(mushroom.x, mushroom.x + 50) and self.mario.y >= mushroom.y:
                self.mario.touch_mushroom()
                self.mushrooms.remove(mushroom)
        for enemy in self.enemies:
            if self.mario.x in range(enemy.x, enemy.x + 50) and self.mario.y >= enemy.y:
                self.mario.touch_enemy()

    def render(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.mario.x, self.mario.y, 50, 50))
        for block in self.blocks:
            pygame.draw.rect(self.screen, (100, 100, 100), (block.x, block.y, 50, 50))
        for mushroom in self.mushrooms:
            pygame.draw.rect(self.screen, (255, 0, 0), (mushroom.x, mushroom.y, 20, 20))
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, (0, 255, 0), (enemy.x, enemy.y, 50, 50))
        pygame.display.flip()

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def jump(self):
        self.y -= 10  # Simplified jump logic

    def hit_block(self):
        pass  # Logic for hitting a block

    def touch_mushroom(self):
        self.score += 10  # Increase score when touching a mushroom

    def touch_enemy(self):
        self.score -= 5  # Decrease score when touching an enemy

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def release_mushroom(self):
        return Mushroom(self.x, self.y - 20)  # Mushroom appears above the block

class Mushroom:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def fall(self):
        self.y += 5  # Fall down

    def move_left(self):
        self.x -= 1  # Move left

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_randomly(self):
        self.x += random.choice([-1, 1])  # Move left or right randomly

class Score:
    def __init__(self):
        self.current_score = 0

    def increase_score(self, amount):
        self.current_score += amount

    def save_score(self):
        with open('scores.txt', 'a') as f:
            f.write(f"{self.current_score}\n")
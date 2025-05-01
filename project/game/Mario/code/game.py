import pygame
from mario import Mario
from mushroom import Mushroom
from enemy import Enemy
from block import Block  # Import Block class

class Game:
    def __init__(self):
        self.mario = Mario(100, 300)
        self.mushrooms = [Mushroom(200, 250)]
        self.enemies = [Enemy(400, 300)]
        self.blocks = [Block(300, 400)]  # Initialize blocks
        self.score = 0
        self.running = True
        self.score_timer = 0  # Timer for score increment
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Mario Game")

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            pygame.time.delay(30)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.mario.move_left()  # Handle moving left
        if keys[pygame.K_RIGHT]:
            self.mario.move_right()  # Handle moving right
        if keys[pygame.K_SPACE]:
            self.mario.jump()  # Handle jumping

    def update(self):
        for mushroom in self.mushrooms:
            mushroom.fall()
        for enemy in self.enemies:
            enemy.move()
        self.handle_collisions()
        self.mario.update()  # Update Mario's position during jump
        self.increment_score_over_time()  # Increment score over time

    def increment_score_over_time(self):
        self.score_timer += 1
        if self.score_timer >= 30:  # Increment score every second
            self.score += 1
            self.score_timer = 0

    def draw(self):
        self.screen.fill((255, 255, 255))  # Clear screen with white
        self.mario.draw(self.screen)
        for mushroom in self.mushrooms:
            mushroom.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for block in self.blocks:  # Draw blocks
            block.draw(self.screen)
        pygame.display.flip()

    def handle_collisions(self):
        for mushroom in self.mushrooms:
            if self.check_collision(self.mario, mushroom):
                self.mario.collect_mushroom()
                self.mushrooms.remove(mushroom)
                self.score += 1000  # Correct score increment

        for enemy in self.enemies:
            if self.check_collision(self.mario, enemy):
                self.mario.touch_enemy()  # Mario touches enemy
                self.running = False  # End game on enemy collision

        for block in self.blocks:  # Check collisions with blocks
            if self.check_collision(self.mario, block):
                self.mario.hit_block()
                new_mushroom = block.release_mushroom()
                self.mushrooms.append(new_mushroom)  # Add released mushroom

    def check_collision(self, obj1, obj2):
        return (obj1.x < obj2.x + obj2.width and
                obj1.x + obj1.width > obj2.x and
                obj1.y < obj2.y + obj2.height and
                obj1.y + obj1.height > obj2.y)

    def save_game(self):
        with open('game_state.txt', 'w') as f:
            f.write(f"{self.mario.x}|{self.mario.y}|{self.score}\n")

    def load_game(self):
        try:
            with open('game_state.txt', 'r') as f:
                data = f.readline().strip().split('|')
                self.mario.x = int(data[0])
                self.mario.y = int(data[1])
                self.score = int(data[2])
        except FileNotFoundError:
            print("No saved game found.")
import pygame
import random

class Player:
    def __init__(self):
        self.position_x = 300  # Starting position at the bottom center of the screen

    def move_left(self):
        self.position_x -= 5  # Move left by 5 pixels

    def move_right(self):
        self.position_x += 5  # Move right by 5 pixels


class Block:
    def __init__(self):
        self.position_y = 0  # Start at the top of the screen
        self.speed = random.randint(3, 7)  # Random speed for falling blocks
        self.position_x = random.randint(0, 600)  # Random horizontal position

    def fall(self):
        self.position_y += self.speed  # Move block down by its speed

    def reset_position(self):
        self.position_y = 0  # Reset to the top
        self.position_x = random.randint(0, 600)  # Random horizontal position


class Game:
    def __init__(self):
        self.player = Player()
        self.blocks = []
        self.score = 0
        self.running = True
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Dodge the Falling Blocks")

    def start(self):
        clock = pygame.time.Clock()
        while self.running:
            self.update()
            self.render()
            clock.tick(60)  # Limit to 60 frames per second

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move_left()
                if event.key == pygame.K_RIGHT:
                    self.player.move_right()

        if random.randint(1, 20) == 1:  # Randomly create a block
            self.blocks.append(Block())

        for block in self.blocks:
            block.fall()
            if block.position_y > 480:  # If the block falls off the screen
                self.blocks.remove(block)
                self.score += 1  # Increase score for dodging

        self.check_collision()

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        pygame.draw.rect(self.screen, (255, 255, 255), (self.player.position_x, 450, 50, 10))  # Draw player

        for block in self.blocks:
            pygame.draw.rect(self.screen, (255, 0, 0), (block.position_x, block.position_y, 50, 50))  # Draw blocks

        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(text, (10, 10))  # Display score

        pygame.display.flip()  # Update the full display Surface to the screen

    def check_collision(self):
        for block in self.blocks:
            if (self.player.position_x < block.position_x + 50 and
                self.player.position_x + 50 > block.position_x and
                450 < block.position_y + 50):
                self.running = False  # End game on collision
                self.save_score()

    def save_score(self):
        with open('highscores.txt', 'a') as f:
            f.write(f"{self.score}\n")  # Save the score in highscores.txt
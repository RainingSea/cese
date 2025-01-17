import pygame
from player import Player
from block import Block

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.score = 0
        self.player = Player(400, 50, 50)  # Starting position and size
        self.blocks = []
        self.block_speed = 5

    def run(self) -> None:
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
            self.draw()
            clock.tick(60)

        self.save_score()
        pygame.quit()

    def update(self) -> None:
        if len(self.blocks) < 5:  # Limit the number of blocks
            new_block = Block(50)  # Block size
            self.blocks.append(new_block)

        for block in self.blocks:
            block.fall(self.block_speed)
            if self.check_collision(block):
                self.score += 1
                self.blocks.remove(block)

        self.blocks = [block for block in self.blocks if block.y_position < 600]  # Remove off-screen blocks

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))  # Clear the screen
        for block in self.blocks:
            pygame.draw.rect(self.screen, (255, 0, 0), (block.get_position()[0], block.get_position()[1], block.size, block.size))
        player_pos = self.player.get_position()
        pygame.draw.rect(self.screen, (0, 255, 0), (player_pos[0], player_pos[1], self.player.width, self.player.height))
        pygame.display.flip()

    def check_collision(self, block) -> bool:
        player_rect = pygame.Rect(self.player.get_position()[0], self.player.get_position()[1], self.player.width, self.player.height)
        block_rect = pygame.Rect(block.get_position()[0], block.get_position()[1], block.size, block.size)
        return player_rect.colliderect(block_rect)

    def save_score(self) -> None:
        with open('scores.txt', 'a') as f:
            f.write(f'score: {self.score}\n')
import pygame
from mario import Mario
from mushroom import Mushroom
from enemy import Enemy

class Game:
    def __init__(self):
        self.mario = Mario(50, 300)
        self.mushrooms = [Mushroom(100, 0), Mushroom(200, 0)]
        self.enemies = [Enemy(300, 300)]
        self.score = 0
        self.load_data()

    def run(self):
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.mario.move('left')
                    if event.key == pygame.K_RIGHT:
                        self.mario.move('right')
                    if event.key == pygame.K_SPACE:
                        self.mario.jump()
            
            self.update_game_logic()
            self.save_data()
            screen.fill((135, 206, 235))  # Clear the screen
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

    def update_game_logic(self):
        for mushroom in self.mushrooms:
            mushroom.fall()
            if mushroom.check_collision(self.mario):
                self.update_score(10)

        for enemy in self.enemies:
            enemy.move()
            if enemy.check_collision(self.mario):
                self.update_score(-5)

    def update_score(self, points):
        self.score += points

    def load_data(self):
        try:
            with open('game_data.txt', 'r') as file:
                self.score = int(file.readline().strip())
        except FileNotFoundError:
            self.score = 0

    def save_data(self):
        with open('game_data.txt', 'w') as file:
            file.write(str(self.score))

    def draw(self, screen):
        # Draw Mario
        pygame.draw.rect(screen, (255, 0, 0), (self.mario.x, self.mario.y, 50, 50))
        # Draw Mushrooms
        for mushroom in self.mushrooms:
            pygame.draw.rect(screen, (0, 255, 0), (mushroom.x, mushroom.y, 30, 30))
        # Draw Enemies
        for enemy in self.enemies:
            pygame.draw.rect(screen, (0, 0, 255), (enemy.x, enemy.y, 50, 50))
        # Draw Score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
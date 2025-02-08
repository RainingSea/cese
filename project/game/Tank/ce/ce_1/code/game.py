import pygame
from player_tank import PlayerTank
from enemy_tank import EnemyTank
from obstacle import Obstacle

class Game:
    def __init__(self):
        self.player_tank = PlayerTank(100, 100)
        self.enemy_tanks = [EnemyTank(200, 200), EnemyTank(300, 300)]
        self.obstacles = [Obstacle(150, 150), Obstacle(250, 250)]
        self.score = 0
        self.game_state = 1  # 1 for running, 0 for game over

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Tank Battle Game")
        clock = pygame.time.Clock()

        while self.game_state:
            self.handle_input()
            self.update()
            self.render(screen)
            clock.tick(60)

        self.end_game()

    def update(self) -> None:
        # Update game logic here
        pass

    def render(self, screen) -> None:
        screen.fill((0, 0, 0))  # Clear screen
        # Draw player tank, enemy tanks, and obstacles here
        pygame.display.flip()

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = 0

    def check_collisions(self) -> None:
        # Logic for checking collisions would go here
        pass

    def end_game(self) -> None:
        with open('score.txt', 'w') as f:
            f.write(str(self.score))
        pygame.quit()
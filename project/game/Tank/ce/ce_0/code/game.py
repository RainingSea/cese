import pygame
import os

class Tank:
    def __init__(self, position_x: int, position_y: int):
        self.health = 100
        self.position_x = position_x
        self.position_y = position_y

    def move(self, direction: str) -> None:
        if direction == "up":
            self.position_y -= 1
        elif direction == "down":
            self.position_y += 1
        elif direction == "left":
            self.position_x -= 1
        elif direction == "right":
            self.position_x += 1

    def fire(self) -> 'Bullet':
        return Bullet(self.position_x, self.position_y, "up")


class EnemyTank:
    def __init__(self, position_x: int, position_y: int):
        self.health = 100
        self.position_x = position_x
        self.position_y = position_y

    def shoot(self) -> 'Bullet':
        return Bullet(self.position_x, self.position_y, "down")


class Bullet:
    def __init__(self, position_x: int, position_y: int, direction: str):
        self.position_x = position_x
        self.position_y = position_y
        self.direction = direction

    def move(self) -> None:
        if self.direction == "up":
            self.position_y -= 1
        elif self.direction == "down":
            self.position_y += 1
        elif self.direction == "left":
            self.position_x -= 1
        elif self.direction == "right":
            self.position_x += 1


class Game:
    def __init__(self):
        self.grid_size = 20
        self.player_tank = Tank(10, 10)
        self.enemy_tanks = [EnemyTank(5, 5), EnemyTank(15, 15)]
        self.score = 0
        self.player_health = 100

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((400, 400))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            self.draw(screen)
        self.save_game()
        pygame.quit()

    def update(self) -> None:
        pass  # Game logic updates will go here

    def draw(self, screen) -> None:
        screen.fill((0, 0, 0))  # Clear the screen
        # Draw player tank
        pygame.draw.rect(screen, (255, 255, 0), (self.player_tank.position_x * 20, self.player_tank.position_y * 20, 20, 20))
        # Draw enemy tanks
        for enemy_tank in self.enemy_tanks:
            pygame.draw.rect(screen, (192, 192, 192), (enemy_tank.position_x * 20, enemy_tank.position_y * 20, 20, 20))
        pygame.display.flip()

    def save_game(self) -> None:
        with open("game_data.txt", "w") as file:
            file.write(f"score|{self.score}\n")
            file.write(f"player_health|{self.player_health}\n")

    def load_game(self) -> None:
        if os.path.exists("game_data.txt"):
            with open("game_data.txt", "r") as file:
                for line in file:
                    key, value = line.strip().split("|")
                    if key == "score":
                        self.score = int(value)
                    elif key == "player_health":
                        self.player_health = int(value)
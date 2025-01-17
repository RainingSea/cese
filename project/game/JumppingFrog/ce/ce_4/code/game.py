import pygame
import json
from typing import List

class Frog:
    def __init__(self, x: int, y: int, velocity: int):
        self.x = x
        self.y = y
        self.velocity = velocity

    def move_left(self) -> None:
        self.x -= self.velocity

    def move_right(self) -> None:
        self.x += self.velocity

    def jump(self) -> None:
        self.y -= 100  # Jump height

class Platform:
    def __init__(self, x: int, y: int, width: int, height: int, moving_direction: str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.moving_direction = moving_direction

    def move(self) -> None:
        if self.moving_direction == "horizontal":
            self.x += 2  # Example movement speed

    def draw(self, screen) -> None:
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))

class Game:
    def __init__(self):
        self.frog = Frog(100, 300, 10)
        self.platforms: List[Platform] = [Platform(50, 250, 100, 10, "horizontal")]
        self.score = 0
        self.timer = 0.0

    def start_game(self) -> None:
        pygame.init()
        self.load_data()
        screen = pygame.display.set_mode((800, 600))
        running = True

        while running:
            self.update()
            self.render(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.frog.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.frog.move_right()
                    if event.key == pygame.K_SPACE:
                        self.frog.jump()

        self.save_data()
        pygame.quit()

    def update(self) -> None:
        self.timer += 0.1  # Increment timer
        for platform in self.platforms:
            platform.move()

    def render(self, screen) -> None:
        screen.fill((0, 0, 0))  # Clear screen
        for platform in self.platforms:
            platform.draw(screen)
        pygame.draw.rect(screen, (255, 0, 0), (self.frog.x, self.frog.y, 50, 50))  # Draw frog
        pygame.display.flip()  # Update display

    def check_collision(self) -> None:
        pass  # Collision logic to be implemented

    def load_data(self) -> None:
        try:
            with open('game_data.txt', 'r') as file:
                data = file.readlines()
                self.score = int(data[0].split('|')[1])
        except FileNotFoundError:
            self.score = 0

    def save_data(self) -> None:
        with open('game_data.txt', 'w') as file:
            file.write(f"highest_score|{self.score}\n")
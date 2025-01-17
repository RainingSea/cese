import pygame
import random

class Platform:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move(self, direction: str, distance: int) -> None:
        if direction == "left":
            self.x -= distance
        elif direction == "right":
            self.x += distance

class Frog:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def jump(self, direction: str, distance: int) -> None:
        if direction == "up":
            self.y -= distance
        elif direction == "down":
            self.y += distance

    def move_left(self) -> None:
        self.x -= 10  # Move left by 10 pixels

    def move_right(self) -> None:
        self.x += 10  # Move right by 10 pixels

class Game:
    def __init__(self):
        self.frog = Frog(100, 300)
        self.platforms = [Platform(random.randint(0, 400), random.randint(100, 400), 100, 10) for _ in range(5)]
        self.score = 0
        self.timer = 0.0

    def start_game(self) -> None:
        self.score = 0
        self.timer = 60.0  # Start timer for 60 seconds

    def update(self) -> None:
        # Update game logic such as frog position and timer
        self.timer -= 0.016  # Assuming 60 FPS, decrease timer

    def check_collision(self) -> None:
        # Check for collision between frog and platforms
        for platform in self.platforms:
            if (self.frog.x > platform.x and self.frog.x < platform.x + platform.width and
                self.frog.y + 10 > platform.y and self.frog.y < platform.y + platform.height):
                self.score += 1  # Increment score on collision

    def end_game(self) -> None:
        with open('game_data.txt', 'a') as file:
            file.write(f'Score: {self.score}\n')
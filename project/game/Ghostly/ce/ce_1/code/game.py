import pygame
import random

class Player:
    def __init__(self):
        self.position = (0, 0)
        self.score = 0
        self.power_up = False

    def move(self, direction: str) -> None:
        x, y = self.position
        if direction == 'UP':
            self.position = (x, y - 1)
        elif direction == 'DOWN':
            self.position = (x, y + 1)
        elif direction == 'LEFT':
            self.position = (x - 1, y)
        elif direction == 'RIGHT':
            self.position = (x + 1, y)

    def eat_pellet(self) -> None:
        self.score += 1

    def eat_superpellet(self) -> None:
        self.power_up = True

class Monster:
    def __init__(self):
        self.position = (5, 5)

    def chase(self, player_position: tuple[int, int]) -> None:
        if player_position[0] > self.position[0]:
            self.position = (self.position[0] + 1, self.position[1])
        elif player_position[0] < self.position[0]:
            self.position = (self.position[0] - 1, self.position[1])
        if player_position[1] > self.position[1]:
            self.position = (self.position[0], self.position[1] + 1)
        elif player_position[1] < self.position[1]:
            self.position = (self.position[0], self.position[1] - 1)

class Wall:
    def __init__(self, position: tuple[int, int]):
        self.position = position

class Pellet:
    def __init__(self, position: tuple[int, int]):
        self.position = position

class SuperPellet:
    def __init__(self, position: tuple[int, int]):
        self.position = position

class Game:
    def __init__(self):
        self.player = Player()
        self.monster = Monster()
        self.walls = [Wall((1, 1)), Wall((1, 2)), Wall((2, 1))]
        self.pellets = [Pellet((0, 1)), Pellet((0, 2))]
        self.superpellets = [SuperPellet((3, 3))]
        self.game_ticks = 0

    def start(self) -> None:
        self.load_game_state()
        self.game_loop()

    def game_loop(self) -> None:
        running = True
        while running:
            self.update()
            self.draw()
            self.check_collisions()
            self.game_ticks += 1

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.move('UP')
        if keys[pygame.K_DOWN]:
            self.player.move('DOWN')
        if keys[pygame.K_LEFT]:
            self.player.move('LEFT')
        if keys[pygame.K_RIGHT]:
            self.player.move('RIGHT')
        
        self.monster.chase(self.player.position)

    def draw(self) -> None:
        # Placeholder for drawing logic
        pass

    def check_collisions(self) -> None:
        for pellet in self.pellets:
            if self.player.position == pellet.position:
                self.player.eat_pellet()
                self.pellets.remove(pellet)
                break

        for superpellet in self.superpellets:
            if self.player.position == superpellet.position:
                self.player.eat_superpellet()
                self.superpellets.remove(superpellet)
                break

    def load_game_state(self) -> None:
        try:
            with open('game_state.txt', 'r') as f:
                data = f.read().strip().split('|')
                self.player.position = (int(data[0]), int(data[1]))
                self.player.score = int(data[2])
                self.player.power_up = data[3] == 'True'
        except FileNotFoundError:
            pass

    def save_game_state(self) -> None:
        with open('game_state.txt', 'w') as f:
            f.write(f"{self.player.position[0]}|{self.player.position[1]}|{self.player.score}|{self.player.power_up}")
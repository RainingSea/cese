import pygame
import random
from typing import List

class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.superpellet_active = False

    def move(self, direction: str) -> None:
        if direction == "up":
            self.y -= 5
        elif direction == "down":
            self.y += 5
        elif direction == "left":
            self.x -= 5
        elif direction == "right":
            self.x += 5

    def eat_pellet(self, pellet) -> None:
        if (self.x, self.y) == (pellet.x, pellet.y):
            if pellet.is_superpellet:
                self.superpellet_active = True
            pellet.is_superpellet = False  # Pellet is eaten

class Wall:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw(self) -> None:
        pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), (self.x, self.y, 50, 10))

class Pellet:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.is_superpellet = False

    def draw(self) -> None:
        pygame.draw.circle(pygame.display.get_surface(), (255, 255, 0), (self.x, self.y), 5)

class Superpellet(Pellet):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.is_superpellet = True

    def draw(self) -> None:
        pygame.draw.circle(pygame.display.get_surface(), (255, 0, 0), (self.x, self.y), 10)

class Ghost:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw(self) -> None:
        pygame.draw.circle(pygame.display.get_surface(), (0, 255, 0), (self.x, self.y), 15)

class Monster:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.active = False

    def chase(self, player: Player) -> None:
        if self.active:
            if player.x > self.x:
                self.x += 1
            elif player.x < self.x:
                self.x -= 1
            if player.y > self.y:
                self.y += 1
            elif player.y < self.y:
                self.y -= 1

    def draw(self) -> None:
        pygame.draw.rect(pygame.display.get_surface(), (255, 0, 255), (self.x, self.y, 20, 20))

    def activate(self) -> None:
        self.active = True

class Game:
    def __init__(self):
        self.player = Player(100, 100)
        self.walls = [Wall(random.randint(0, 400), random.randint(0, 400)) for _ in range(5)]
        self.pellets = [Pellet(random.randint(0, 400), random.randint(0, 400)) for _ in range(10)]
        self.superpellets = [Superpellet(random.randint(0, 400), random.randint(0, 400)) for _ in range(2)]
        self.ghosts = [Ghost(random.randint(0, 400), random.randint(0, 400)) for _ in range(3)]
        self.monster = Monster(random.randint(0, 400), random.randint(0, 400))
        self.score = 0
        self.ticks = 0
        self.monster_activation_threshold = 50  # Example threshold for monster activation
        self.game_over = False

    def start(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_event(event.key)
            self.update()
            self.draw()
            if self.game_over:
                running = False

    def handle_key_event(self, key: int) -> None:
        if key == pygame.K_UP:
            self.player.move("up")
        elif key == pygame.K_DOWN:
            self.player.move("down")
        elif key == pygame.K_LEFT:
            self.player.move("left")
        elif key == pygame.K_RIGHT:
            self.player.move("right")

    def update(self) -> None:
        self.check_collisions()
        self.monster.chase(self.player)
        if self.score >= self.monster_activation_threshold:
            self.monster.activate()
        if self.check_game_over():
            self.game_over = True

    def draw(self) -> None:
        pygame.display.get_surface().fill((255, 255, 255))  # Clear screen
        for wall in self.walls:
            wall.draw()
        for pellet in self.pellets:
            pellet.draw()
        for superpellet in self.superpellets:
            superpellet.draw()
        for ghost in self.ghosts:
            ghost.draw()
        self.monster.draw()
        pygame.draw.circle(pygame.display.get_surface(), (0, 0, 255), (self.player.x, self.player.y), 10)  # Draw player
        pygame.display.flip()  # Update the display

    def check_collisions(self) -> None:
        for pellet in self.pellets:
            self.player.eat_pellet(pellet)
            if pellet.is_superpellet is False:
                self.pellets.remove(pellet)
                self.score += 10  # Increment score for regular pellet
        for superpellet in self.superpellets:
            self.player.eat_pellet(superpellet)
            if superpellet.is_superpellet is False:
                self.superpellets.remove(superpellet)
                self.score += 20  # Increment score for superpellet
        self.check_wall_collisions()
        self.check_monster_collisions()

    def check_wall_collisions(self) -> None:
        for wall in self.walls:
            if (self.player.x >= wall.x and self.player.x <= wall.x + 50) and \
               (self.player.y >= wall.y and self.player.y <= wall.y + 10):
                # Prevent player from moving through wall
                if self.player.x < wall.x + 25:
                    self.player.x = wall.x - 10
                else:
                    self.player.x = wall.x + 50 + 10
                if self.player.y < wall.y + 5:
                    self.player.y = wall.y - 10
                else:
                    self.player.y = wall.y + 10 + 10

    def check_monster_collisions(self) -> None:
        if (self.player.x >= self.monster.x and self.player.x <= self.monster.x + 20) and \
           (self.player.y >= self.monster.y and self.player.y <= self.monster.y + 20):
            self.game_over = True  # Player collides with monster

    def check_game_over(self) -> bool:
        if self.player.x < 0 or self.player.x > 400 or self.player.y < 0 or self.player.y > 400:
            return True  # Player goes out of bounds
        return False

    def load_high_scores(self) -> List[str]:
        try:
            with open('high_scores.txt', 'r') as file:
                return file.read().splitlines()
        except FileNotFoundError:
            return []

    def save_high_scores(self) -> None:
        with open('high_scores.txt', 'a') as file:
            file.write(f"{self.score}\n")
import pygame
import random

class Game:
    def __init__(self):
        self.player_ghost = PlayerGhost(5, 5)
        self.monster = Monster(1, 1)
        self.walls = [Wall(x, y) for x in range(10) for y in range(10) if (x + y) % 2 == 0]
        self.pellets = [Pellet(random.randint(0, 9), random.randint(0, 9)) for _ in range(5)]
        self.superpellets = [SuperPellet(random.randint(0, 9), random.randint(0, 9)) for _ in range(2)]
        self.score = 0
        self.ticks = 0
        self.running = True

    def start(self):
        screen = pygame.display.set_mode((400, 400))
        clock = pygame.time.Clock()
        
        while self.running:
            self.update()
            self.render(screen)
            self.check_collisions()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            clock.tick(60)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_ghost.move("UP", self.walls, self.monster)
        if keys[pygame.K_DOWN]:
            self.player_ghost.move("DOWN", self.walls, self.monster)
        if keys[pygame.K_LEFT]:
            self.player_ghost.move("LEFT", self.walls, self.monster)
        if keys[pygame.K_RIGHT]:
            self.player_ghost.move("RIGHT", self.walls, self.monster)
        
        self.monster.chase(self.player_ghost)
        self.ticks += 1

    def render(self, screen):
        screen.fill((0, 0, 0))
        for wall in self.walls:
            pygame.draw.rect(screen, (255, 0, 0), (wall.x * 40, wall.y * 40, 40, 40))
        for pellet in self.pellets:
            pygame.draw.circle(screen, (0, 255, 0), (pellet.x * 40 + 20, pellet.y * 40 + 20), 10)
        for superpellet in self.superpellets:
            pygame.draw.circle(screen, (255, 255, 0), (superpellet.x * 40 + 20, superpellet.y * 40 + 20), 15)
        pygame.draw.circle(screen, (0, 0, 255), (self.player_ghost.x * 40 + 20, self.player_ghost.y * 40 + 20), 20)
        pygame.draw.circle(screen, (255, 0, 255), (self.monster.x * 40 + 20, self.monster.y * 40 + 20), 20)
        pygame.display.flip()

    def check_collisions(self):
        for pellet in self.pellets[:]:  # Iterate over a copy of the list
            if self.player_ghost.x == pellet.x and self.player_ghost.y == pellet.y:
                self.player_ghost.eat_pellet(self)
                self.pellets.remove(pellet)
                self.score += 1
        for superpellet in self.superpellets[:]:  # Iterate over a copy of the list
            if self.player_ghost.x == superpellet.x and self.player_ghost.y == superpellet.y:
                self.player_ghost.eat_superpellet()
                self.superpellets.remove(superpellet)
                self.score += 5
        self.check_game_over()
        self.check_monster_collision()

    def check_game_over(self):
        if not self.pellets and not self.superpellets:
            self.running = False  # End the game if all pellets are collected

    def check_monster_collision(self):
        if self.player_ghost.x == self.monster.x and self.player_ghost.y == self.monster.y:
            self.running = False  # End the game if the monster catches the player

class PlayerGhost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.has_superpellet = False

    def move(self, direction, walls, monster):
        new_x, new_y = self.x, self.y
        if direction == "UP":
            new_y = max(0, self.y - 1)
        elif direction == "DOWN":
            new_y = min(9, self.y + 1)
        elif direction == "LEFT":
            new_x = max(0, self.x - 1)
        elif direction == "RIGHT":
            new_x = min(9, self.x + 1)

        # Check for wall collisions
        if not any(wall.x == new_x and wall.y == new_y for wall in walls) and not (new_x == monster.x and new_y == monster.y):
            self.x, self.y = new_x, new_y

    def eat_pellet(self, game):
        pass  # Logic for eating a pellet can be implemented here

    def eat_superpellet(self):
        self.has_superpellet = True

class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def chase(self, target):
        if self.x < target.x:
            self.x += 1
        elif self.x > target.x:
            self.x -= 1
        if self.y < target.y:
            self.y += 1
        elif self.y > target.y:
            self.y -= 1

class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Pellet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SuperPellet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
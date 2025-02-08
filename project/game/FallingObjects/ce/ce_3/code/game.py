import pygame
import random

class FallingObject:
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed

    def fall(self):
        self.position[1] += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.position[0], self.position[1]), 10)

class Basket:
    def __init__(self):
        self.position = [300, 550]

    def move_left(self):
        if self.position[0] > 0:
            self.position[0] -= 10

    def move_right(self):
        if self.position[0] < 600:
            self.position[0] += 10

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0], self.position[1], 100, 20))

class Game:
    def __init__(self):
        self.basket = Basket()
        self.falling_objects = []
        self.score = 0
        self.missed_objects = 0
        self.spawn_falling_object()

    def spawn_falling_object(self):
        position = [random.randint(0, 600), 0]
        speed = random.randint(1, 5)
        self.falling_objects.append(FallingObject(position, speed))

    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Catch the Falling Objects")
        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        self.screen.fill((0, 0, 0))
        self.basket.draw(self.screen)

        for obj in self.falling_objects:
            obj.fall()
            obj.draw(self.screen)
            if obj.position[1] > 600:
                self.missed_objects += 1
                self.falling_objects.remove(obj)
                self.spawn_falling_object()

        self.check_collision()
        self.display_score()
        pygame.display.flip()
        self.clock.tick(60)

    def check_collision(self):
        for obj in self.falling_objects:
            if (self.basket.position[0] < obj.position[0] < self.basket.position[0] + 100) and \
               (self.basket.position[1] < obj.position[1] < self.basket.position[1] + 20):
                self.score += 1
                self.falling_objects.remove(obj)
                self.spawn_falling_object()

    def end_game(self):
        with open('game_data.txt', 'w') as file:
            file.write(f"{self.score}\n{self.missed_objects}\n")
        pygame.quit()
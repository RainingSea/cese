import pygame
import random

class Object:
    def __init__(self, position):
        self.position = position

    def fall(self):
        self.position = (self.position[0], self.position[1] + 5)

    def get_position(self):
        return self.position

class Basket:
    def __init__(self, position):
        self.position = position

    def move_left(self):
        if self.position[0] > 0:
            self.position = (self.position[0] - 5, self.position[1])

    def move_right(self):
        if self.position[0] < 800:  # Assuming screen width is 800
            self.position = (self.position[0] + 5, self.position[1])

    def get_position(self):
        return self.position

class Game:
    def __init__(self):
        self.basket = Basket((400, 550))  # Starting position of the basket
        self.falling_objects = []
        self.score = 0
        self.missed_objects = 0
        self.game_time = 0.0

    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Catch the Falling Objects")
        self.clock = pygame.time.Clock()
        self.spawn_object()

    def update(self):
        for obj in self.falling_objects:
            obj.fall()
            if obj.get_position()[1] > 600:  # If object falls below screen
                self.missed_objects += 1
                self.falling_objects.remove(obj)
        
        self.check_collision()
        self.spawn_object()

    def render(self):
        self.screen.fill((255, 255, 255))  # Clear screen with white
        basket_pos = self.basket.get_position()
        pygame.draw.rect(self.screen, (0, 255, 0), (basket_pos[0], basket_pos[1], 100, 20))  # Draw basket

        for obj in self.falling_objects:
            obj_pos = obj.get_position()
            pygame.draw.circle(self.screen, (255, 0, 0), obj_pos, 10)  # Draw falling object

        # Display score and missed objects
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        missed_text = font.render(f'Missed: {self.missed_objects}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(missed_text, (10, 40))

        pygame.display.flip()

    def check_collision(self):
        basket_rect = pygame.Rect(self.basket.get_position()[0], self.basket.get_position()[1], 100, 20)
        for obj in self.falling_objects:
            obj_pos = obj.get_position()
            obj_rect = pygame.Rect(obj_pos[0] - 10, obj_pos[1] - 10, 20, 20)  # Object size
            if basket_rect.colliderect(obj_rect):
                self.score += 1
                self.falling_objects.remove(obj)

    def end_game(self):
        pygame.quit()

    def spawn_object(self):
        if len(self.falling_objects) < 5:  # Limit number of falling objects
            new_object = Object((random.randint(0, 790), 0))  # Spawn at random x position
            self.falling_objects.append(new_object)
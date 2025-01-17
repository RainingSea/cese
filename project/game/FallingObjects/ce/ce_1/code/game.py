import pygame
import random

class Object:
    def __init__(self):
        self.position_x = random.randint(0, 800)  # Assuming screen width is 800
        self.position_y = 0  # Start at the top

    def fall(self):
        self.position_y += 5  # Falling speed

    def get_position(self):
        return (self.position_x, self.position_y)

class Basket:
    def __init__(self):
        self.position_x = 400  # Start at the center

    def move_left(self):
        if self.position_x > 0:
            self.position_x -= 10  # Move left

    def move_right(self):
        if self.position_x < 760:  # Assuming basket width is 40
            self.position_x += 10  # Move right

    def get_position(self):
        return self.position_x

class Game:
    def __init__(self):
        self.basket = Basket()
        self.falling_objects = []
        self.score = 0
        self.missed_objects = 0
        self.spawn_object()

    def spawn_object(self):
        self.falling_objects.append(Object())

    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Catch the Falling Objects")
        self.clock = pygame.time.Clock()
        self.run_game()

    def update(self):
        for obj in self.falling_objects:
            obj.fall()
            if obj.position_y > 600:  # If object falls below the screen
                self.missed_objects += 1
                self.falling_objects.remove(obj)
                self.spawn_object()

    def render(self):
        self.screen.fill((255, 255, 255))  # Clear screen with white
        basket_pos = self.basket.get_position()
        pygame.draw.rect(self.screen, (0, 255, 0), (basket_pos, 550, 40, 20))  # Draw basket

        for obj in self.falling_objects:
            obj_pos = obj.get_position()
            pygame.draw.circle(self.screen, (255, 0, 0), obj_pos, 10)  # Draw falling object

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()  # Update the display

    def check_collisions(self):
        basket_pos = self.basket.get_position()
        for obj in self.falling_objects:
            obj_pos = obj.get_position()
            if (basket_pos < obj_pos[0] < basket_pos + 40) and (550 < obj_pos[1] < 570):
                self.score += 1
                self.falling_objects.remove(obj)
                self.spawn_object()

    def end_game(self):
        pygame.quit()
import pygame
import random

class Object:
    def __init__(self):
        self.position = random.randint(0, 800)  # Assuming screen width is 800
        self.speed = random.randint(1, 5)

    def fall(self):
        self.position += self.speed

    def get_position(self):
        return self.position

class Basket:
    def __init__(self):
        self.position = 400  # Starting position in the middle of the screen

    def move_left(self):
        if self.position > 0:
            self.position -= 10

    def move_right(self):
        if self.position < 800:  # Assuming screen width is 800
            self.position += 10

    def get_position(self):
        return self.position

class Game:
    def __init__(self):
        self.score = 0
        self.missed_objects = 0
        self.basket = Basket()
        self.falling_objects = []

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.basket.move_left()
            if keys[pygame.K_RIGHT]:
                self.basket.move_right()

            self.update()
            self.draw(screen)
            clock.tick(30)

        self.end_game()

    def update(self):
        if len(self.falling_objects) < 5:  # Limit the number of falling objects
            self.falling_objects.append(Object())

        for obj in self.falling_objects:
            obj.fall()
            if obj.get_position() > 600:  # Assuming screen height is 600
                self.missed_objects += 1
                self.falling_objects.remove(obj)

        self.check_collisions()

    def draw(self, screen):
        screen.fill((255, 255, 255))  # Clear the screen with white
        basket_pos = self.basket.get_position()
        pygame.draw.rect(screen, (0, 0, 255), (basket_pos, 550, 100, 20))  # Draw basket

        for obj in self.falling_objects:
            pygame.draw.circle(screen, (255, 0, 0), (obj.get_position(), 0), 10)  # Draw falling objects

        score_text = f"Score: {self.score} Missed: {self.missed_objects}"
        font = pygame.font.Font(None, 36)
        text = font.render(score_text, True, (0, 0, 0))
        screen.blit(text, (10, 10))

        pygame.display.flip()

    def check_collisions(self):
        basket_pos = self.basket.get_position()
        for obj in self.falling_objects:
            if obj.get_position() >= 550 and basket_pos <= obj.get_position() <= basket_pos + 100:
                self.score += 1
                self.falling_objects.remove(obj)

    def end_game(self):
        with open('scores.txt', 'a') as score_file:
            score_file.write(f"{self.score}\n")
        with open('missed_objects.txt', 'a') as missed_file:
            missed_file.write(f"{self.missed_objects}\n")
        pygame.quit()
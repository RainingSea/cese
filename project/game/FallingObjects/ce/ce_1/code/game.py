import pygame
import random

class Basket:
    def __init__(self):
        self.position = 300

    def move_left(self):
        if self.position > 0:
            self.position -= 10

    def move_right(self):
        if self.position < 580:  # Assuming the screen width is 600
            self.position += 10

class Object:
    def __init__(self):
        self.position = random.randint(0, 580)  # Assuming the screen width is 600
        self.speed = random.randint(1, 5)

    def fall(self):
        self.position += self.speed

    def reset_position(self):
        self.position = random.randint(0, 580)

class Game:
    def __init__(self):
        self.basket = Basket()
        self.falling_objects = [Object() for _ in range(5)]
        self.score = 0
        self.missed_count = 0
        self.game_over = False

    def start_game(self):
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Catch the Falling Objects")
        clock = pygame.time.Clock()

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.basket.move_left()
            if keys[pygame.K_RIGHT]:
                self.basket.move_right()

            self.update()
            self.render(screen)
            clock.tick(30)

        self.save_scores()

    def update(self):
        for obj in self.falling_objects:
            obj.fall()
            if obj.position > 600:  # Assuming the screen height is 600
                obj.reset_position()
                self.missed_count += 1
                if self.missed_count >= 5:  # End game after 5 missed objects
                    self.game_over = True

    def render(self, screen):
        screen.fill((255, 255, 255))  # White background
        pygame.draw.rect(screen, (0, 0, 255), (self.basket.position, 550, 60, 20))  # Basket
        for obj in self.falling_objects:
            pygame.draw.circle(screen, (255, 0, 0), (obj.position + 30, obj.position), 15)  # Falling objects
        score_text = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def check_game_over(self):
        return self.game_over

    def save_scores(self):
        with open('scores.txt', 'w') as score_file:
            score_file.write(str(self.score))
        with open('missed_objects.txt', 'w') as missed_file:
            missed_file.write(str(self.missed_count))
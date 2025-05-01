import pygame
from basket import Basket
from falling_object import Object

class Game:
    def __init__(self):
        self.basket = Basket()
        self.falling_objects = []
        self.score = 0
        self.missed_objects = 0
        self.max_missed = 5
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Catch the Falling Objects")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def start(self):
        self.run_game_loop()

    def run_game_loop(self):
        running = True
        while running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

            if self.missed_objects >= self.max_missed:
                self.end_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.basket.move_left()
        if keys[pygame.K_RIGHT]:
            self.basket.move_right()

    def update(self):
        if len(self.falling_objects) < 5:
            new_object = Object()
            self.falling_objects.append(new_object)

        for obj in self.falling_objects:
            obj.fall()
            if obj.position[1] > 600:
                obj.reset_position()  # Reset to a new random position
                self.missed_objects += 1

        self.check_collision()

    def render(self):
        self.screen.fill((255, 255, 255))
        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        self.basket.draw(self.screen)

        for obj in self.falling_objects:
            obj.draw(self.screen)

        pygame.display.flip()

    def check_collision(self):
        for obj in self.falling_objects:
            if self.basket.position[0] < obj.position[0] < self.basket.position[0] + self.basket.width:
                self.score += 1
                self.falling_objects.remove(obj)

    def end_game(self):
        self.save_score()
        pygame.quit()
        exit()

    def save_score(self):
        with open('scores.txt', 'w') as f:
            f.write(f'Score: {self.score}\nMissed: {self.missed_objects}\n')
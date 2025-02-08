import pygame
from car import Car
from track import Track
from score import Score

class Game:
    def __init__(self):
        self.pygame = pygame
        self.car = Car()
        self.track = Track()
        self.score = Score()
        self.screen = self.pygame.display.set_mode((800, 600))
        self.clock = self.pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self.running = False

    def update(self):
        keys = self.pygame.key.get_pressed()
        if keys[self.pygame.K_LEFT]:
            self.car.move('left')
        if keys[self.pygame.K_RIGHT]:
            self.car.move('right')
        if keys[self.pygame.K_SPACE]:
            self.score.calculate_score(self.car.drift(), self.car.speed, self.car.style_score)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.track.draw()
        self.car.draw(self.screen)
        self.pygame.display.flip()

    def load_tracks(self):
        # Placeholder for loading tracks
        pass

    def save_score(self, score):
        self.score.save_score_to_file('scores.txt')
import pygame
from pygame.locals import *
from car import Car
from track import Track
from score import Score

class Game:
    def __init__(self):
        self.car = Car()
        self.track = Track()
        self.score = Score()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Drift Rivals")
        self.clock = pygame.time.Clock()
        self.track_selection = ["track1", "track2"]
        self.current_track_index = 0

    def start_game(self) -> None:
        self.track.load(self.track_selection[self.current_track_index])  # Load the selected track
        self.run()

    def run(self) -> None:
        while True:
            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(60)

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.car.move("left")
        if keys[K_RIGHT]:
            self.car.move("right")
        if keys[K_UP]:
            self.car.move("forward")
        if keys[K_DOWN]:
            self.car.move("backward")
        if keys[K_SPACE]:
            self.car.drift()
        if keys[K_TAB]:  # Switch track on tab key press
            self.current_track_index = (self.current_track_index + 1) % len(self.track_selection)
            self.track.load(self.track_selection[self.current_track_index])

    def update(self) -> None:
        self.car.update_position()
        self.score.calculate_score(self.car.drift_metrics)

    def render(self) -> None:
        self.screen.fill((0, 0, 0))  # Clear screen
        self.track.render(self.screen)
        self.car.render(self.screen)
        self.display_score()
        pygame.display.flip()

    def display_score(self) -> None:
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score.current_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
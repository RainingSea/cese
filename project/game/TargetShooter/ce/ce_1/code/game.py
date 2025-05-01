import pygame
import random

class Target:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 20)

class Score:
    def __init__(self, player_name, score_value):
        self.player_name = player_name
        self.score_value = score_value

class Game:
    def __init__(self):
        self.score = 0
        self.time_left = 30
        self.targets = []
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Target Shooter")
        self.clock = pygame.time.Clock()

    def start_game(self):
        self.score = 0
        self.time_left = 30
        self.targets.clear()
        self.run_game_loop()

    def run_game_loop(self):
        while self.time_left > 0:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        self.calculate_score()
        self.load_leaderboard()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def update(self):
        if random.randint(1, 30) == 1:  # Randomly generate targets
            new_target = Target(random.randint(0, 780), 0, random.randint(1, 3))
            self.targets.append(new_target)

        for target in self.targets:
            target.move()
            if target.y > 600:  # Remove targets that go off screen
                self.targets.remove(target)

        self.time_left -= 1 / 60  # Decrease time left

    def draw(self):
        self.screen.fill((255, 255, 255))
        for target in self.targets:
            target.draw(self.screen)

        # Draw score and timer
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        timer_text = font.render(f'Time Left: {int(self.time_left)}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(timer_text, (10, 50))
        pygame.display.flip()

    def restart(self):
        self.start_game()

    def calculate_score(self):
        # Placeholder for score calculation logic
        pass

    def load_leaderboard(self):
        try:
            with open('scores.txt', 'r') as file:
                scores = [line.strip().split(',') for line in file.readlines()]
                scores = [Score(player_name, int(score_value)) for player_name, score_value in scores]
                scores.sort(key=lambda x: x.score_value, reverse=True)
                print("Leaderboard:")
                for score in scores:
                    print(f"{score.player_name}: {score.score_value}")
        except FileNotFoundError:
            print("No scores found.")
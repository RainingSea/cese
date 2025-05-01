import pygame
import random
import time

class Shooter:
    def aim(self, mouse_position: tuple) -> None:
        # Update the shooter's position based on mouse movement
        self.position = mouse_position

    def shoot(self) -> None:
        # Handle shooting action
        print("Shooting at", self.position)

class TargetManager:
    def __init__(self):
        self.targets = []

    def spawn_target(self) -> None:
        # Generate a new target at a random location on the screen
        target_position = (random.randint(0, 800), random.randint(0, 600))
        self.targets.append(target_position)

    def move_targets(self) -> None:
        # Update the positions of all active targets on the screen
        for i in range(len(self.targets)):
            self.targets[i] = (self.targets[i][0] + random.choice([-1, 1]), self.targets[i][1] + random.choice([-1, 1]))

class ScoreManager:
    def __init__(self):
        self.score = 0

    def calculate_score(self, hit: bool, time_taken: float) -> None:
        if hit:
            self.score += max(0, 100 - int(time_taken * 10))

    def get_score(self) -> int:
        return self.score

class Timer:
    def __init__(self):
        self.time_remaining = 0

    def start_timer(self, duration: int) -> None:
        self.time_remaining = duration

    def update_timer(self) -> None:
        if self.time_remaining > 0:
            self.time_remaining -= 1

class Leaderboard:
    def __init__(self):
        self.scores = []

    def update_leaderboard(self, new_score: int) -> None:
        self.scores.append(new_score)
        self.scores = sorted(self.scores, reverse=True)[:10]  # Keep top 10 scores

    def get_top_scores(self) -> list:
        return self.scores

class Game:
    def __init__(self):
        self.shooter = Shooter()
        self.target_manager = TargetManager()
        self.score_manager = ScoreManager()
        self.timer = Timer()
        self.leaderboard = Leaderboard()

    def start_game(self) -> None:
        self.timer.start_timer(60)  # Start a 60 seconds timer
        while self.timer.time_remaining > 0:
            self.target_manager.spawn_target()
            self.target_manager.move_targets()
            # Simulate aiming and shooting
            mouse_position = pygame.mouse.get_pos()
            self.shooter.aim(mouse_position)
            self.shooter.shoot()
            time.sleep(1)  # Simulate frame delay
            self.timer.update_timer()
        print("Game Over! Your score:", self.score_manager.get_score())

    def restart_game(self) -> None:
        self.__init__()  # Reset game state
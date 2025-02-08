import pygame
import random

class Maze:
    def __init__(self):
        self.walls = []
        self.treasure_location = None

    def generate_maze(self):
        # Simple maze generation logic (placeholder for actual algorithm)
        self.walls = [(x, y) for x in range(10) for y in range(10) if random.choice([True, False])]
        self.treasure_location = (random.randint(0, 9), random.randint(0, 9))

    def draw_maze(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 0, 0), (wall[0] * 50, wall[1] * 50, 50, 50))
        if self.treasure_location:
            pygame.draw.rect(screen, (255, 215, 0), (self.treasure_location[0] * 50, self.treasure_location[1] * 50, 50, 50))

class Player:
    def __init__(self):
        self.position = (0, 0)

    def move(self, direction: str):
        x, y = self.position
        if direction == 'UP':
            self.position = (x, y - 1)
        elif direction == 'DOWN':
            self.position = (x, y + 1)
        elif direction == 'LEFT':
            self.position = (x - 1, y)
        elif direction == 'RIGHT':
            self.position = (x + 1, y)

    def get_position(self):
        return self.position

class Timer:
    def __init__(self, time_limit: int):
        self.start_time = None
        self.time_limit = time_limit

    def start(self):
        self.start_time = pygame.time.get_ticks()

    def check_time(self):
        if self.start_time is None:
            return False
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        return elapsed_time < self.time_limit

    def get_elapsed_time(self):
        if self.start_time is None:
            return 0
        return (pygame.time.get_ticks() - self.start_time) / 1000

class ScoreManager:
    def __init__(self):
        self.score = 0

    def increase_score(self):
        self.score += 1

    def get_score(self):
        return self.score

    def save_score(self, player_name: str):
        with open('scores.txt', 'a') as file:
            file.write(f"{player_name}|{self.score}\n")

    def load_scores(self):
        scores = []
        try:
            with open('scores.txt', 'r') as file:
                for line in file:
                    name, score = line.strip().split('|')
                    scores.append((name, int(score)))
        except FileNotFoundError:
            pass
        return scores

class Game:
    def __init__(self):
        self.maze = Maze()
        self.player = Player()
        self.timer = Timer(60)  # 60 seconds time limit
        self.score_manager = ScoreManager()

    def start_game(self):
        self.maze.generate_maze()
        self.timer.start()

    def restart_game(self):
        self.player = Player()
        self.score_manager = ScoreManager()
        self.start_game()

    def update(self):
        if not self.timer.check_time():
            print("Time's up!")
            return

    def draw(self, screen):
        self.maze.draw_maze(screen)
        pygame.draw.rect(screen, (0, 0, 255), (self.player.get_position()[0] * 50, self.player.get_position()[1] * 50, 50, 50))
        # Display score and timer
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score_manager.get_score()}", True, (255, 255, 255))
        timer_text = font.render(f"Time: {self.timer.get_elapsed_time():.2f}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (10, 50))
import pygame
import random

class Frog:
    def __init__(self):
        self.position_x = 100
        self.position_y = 300
        self.jump_height = 50  # Adjusted for realistic jump

    def move_left(self):
        self.position_x -= 10

    def move_right(self):
        self.position_x += 10

    def jump(self):
        self.position_y -= self.jump_height

class Platform:
    def __init__(self, x, y, width, height):
        self.position_x = x
        self.position_y = y
        self.width = width
        self.height = height
        self.direction = random.choice([-1, 1])  # Randomly choose direction for movement
        self.speed = 2  # Speed of platform movement

    def move(self):
        self.position_x += self.direction * self.speed
        # Reverse direction if hitting screen boundaries
        if self.position_x <= 0 or self.position_x >= 400 - self.width:
            self.direction *= -1

class Game:
    def __init__(self):
        self.frog = Frog()
        self.platforms = [Platform(random.randint(0, 400), random.randint(100, 400), 100, 20) for _ in range(5)]
        self.score = 0
        self.timer = 0.0
        self.running = True
        self.clock = pygame.time.Clock()

    def start(self):
        self.load_game_data()
        self.main_loop()

    def main_loop(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.time.delay(100)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Changed to 'A' for left movement
                    self.frog.move_left()
                if event.key == pygame.K_d:  # Changed to 'D' for right movement
                    self.frog.move_right()
                if event.key == pygame.K_SPACE:
                    self.frog.jump()

    def update(self):
        for platform in self.platforms:
            platform.move()  # Update platform positions
        self.check_collision()
        self.update_score()
        self.timer += self.clock.get_time() / 1000.0  # Update timer based on clock ticks

    def render(self):
        # Placeholder for rendering logic
        pass

    def check_collision(self):
        # Placeholder for collision detection logic
        pass

    def update_score(self):
        self.score += 1  # Logic for increasing score

    def save_score(self):
        with open('scores.txt', 'a') as f:
            f.write(f"{self.score}\n")

    def load_game_data(self):
        try:
            with open('game_data.txt', 'r') as f:
                data = f.readlines()
                for line in data:
                    key, value = line.strip().split('|')
                    if key == 'frog_position':
                        self.frog.position_x = int(value)
                        self.frog.position_y = int(next(data).strip().split('|')[1])
                    elif key == 'score':
                        self.score = int(value)
                    elif key == 'timer':
                        self.timer = float(value)
        except FileNotFoundError:
            pass

    def save_game_data(self):
        with open('game_data.txt', 'w') as f:
            f.write(f"frog_position|{self.frog.position_x}|{self.frog.position_y}\n")
            f.write(f"score|{self.score}\n")
            f.write(f"timer|{self.timer}\n")

    def end_game(self):
        self.save_score()
        self.save_game_data()
        print("Game Over")
        self.running = False
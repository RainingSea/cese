import pygame
import os

class Frog:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.is_jumping = False
        self.jump_height = 10
        self.gravity = 0.5
        self.velocity_y = 0

    def move(self, direction: str):
        if direction == "left":
            self.x -= 5
        elif direction == "right":
            self.x += 5

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_height

    def update_position(self):
        if self.is_jumping:
            self.y += self.velocity_y
            self.velocity_y += self.gravity
            if self.y >= 300:  # Reset position when landing
                self.y = 300
                self.is_jumping = False

class Platform:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = "stationary"  # New attribute for platform movement
        self.speed = 2  # Speed of platform movement

    def move(self):
        if self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed

    def check_collision(self, frog: Frog) -> bool:
        return (frog.x < self.x + self.width and
                frog.x + frog.width > self.x and
                frog.y < self.y + self.height and
                frog.y + frog.height > self.y)

class Game:
    def __init__(self):
        self.frog = Frog(100, 300)
        self.platforms = [Platform(50, 400, 100, 20), Platform(200, 350, 100, 20)]
        self.platforms[0].direction = "left"  # Set direction for movement
        self.platforms[1].direction = "right"  # Set direction for movement
        self.score = 0
        self.timer = 60.0
        self.lives = 3
        self.load_data()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        running = True

        while running:
            self.handle_input()
            self.update()
            self.check_collisions()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def update(self):
        self.frog.update_position()
        for platform in self.platforms:
            platform.move()  # Update platform positions
        self.timer -= 0.016  # Decrement timer
        if self.timer <= 0:
            self.end_game()

    def draw(self, screen):
        screen.fill((0, 0, 255))  # Background color for water
        for platform in self.platforms:
            pygame.draw.rect(screen, (0, 255, 0), (platform.x, platform.y, platform.width, platform.height))
        pygame.draw.rect(screen, (255, 0, 0), (self.frog.x, self.frog.y, self.frog.width, self.frog.height))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.frog.move("left")
                if event.key == pygame.K_RIGHT:
                    self.frog.move("right")
                if event.key == pygame.K_SPACE:
                    self.frog.jump()

    def check_collisions(self):
        collision_occurred = False
        for platform in self.platforms:
            if platform.check_collision(self.frog):
                self.score += 1  # Increment score on collision
                collision_occurred = True
                break
        if not collision_occurred:
            self.lives -= 1  # Decrement lives if no collision
            if self.lives <= 0:
                self.end_game()

    def reset_game(self):
        self.frog = Frog(100, 300)
        self.score = 0
        self.timer = 60.0
        self.lives = 3

    def save_score(self):
        with open('scores.txt', 'a') as file:
            file.write(f'Score: {self.score}\n')

    def load_data(self):
        if os.path.exists('game_state.txt'):
            with open('game_state.txt', 'r') as file:
                data = file.readlines()
                for line in data:
                    if "Frog Position" in line:
                        position = line.split(": ")[1].strip().split(",")
                        self.frog.x, self.frog.y = int(position[0]), int(position[1])
                    elif "Score" in line:
                        self.score = int(line.split(": ")[1].strip())
                    elif "Timer" in line:
                        self.timer = float(line.split(": ")[1].strip())
                    elif "Lives" in line:
                        self.lives = int(line.split(": ")[1].strip())

    def end_game(self):
        self.save_score()
        print("Game Over! Score saved.")
        self.reset_game()
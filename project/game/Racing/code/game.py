import pygame
import random

class Vehicle:
    def __init__(self):
        self.speed = 0
        self.distance = 0
        self.lane = 1  # Center lane

    def accelerate(self):
        self.speed += 5
        self.distance += self.speed / 60  # Assuming 60 FPS

    def decelerate(self):
        self.speed = max(0, self.speed - 5)

    def change_lane(self, direction: str):
        new_lane = self.lane + (-1 if direction == "left" else 1)
        if 0 <= new_lane <= 2:
            self.lane = new_lane

    def stop(self):
        self.speed = 0

class Obstacle:
    def __init__(self, lane):
        self.type = random.randint(1, 3)  # Random obstacle type
        self.position = 600  # Initialize position off-screen
        self.lane = lane

    def move(self):
        self.position -= 5  # Move obstacle backward

    def check_collision(self, vehicle: Vehicle):
        # Logic to check for collision with the vehicle
        return self.position <= 0 and self.lane == vehicle.lane  # Simplified collision check

class Game:
    def __init__(self):
        self.vehicle = Vehicle()
        self.obstacles = []
        self.score = 0
        self.running = True
        self.window_width = 800
        self.window_height = 600
        self.lane_height = self.window_height / 3
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Racing Game")
        self.load_high_scores()

    def start_game(self):
        self.initialize_game_interface()
        self.game_loop()

    def initialize_game_interface(self):
        self.vehicle = Vehicle()
        self.obstacles = []
        self.score = 0
        self.running = True

    def game_loop(self):
        while self.running:
            self.update()
            self.handle_events()
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.vehicle.accelerate()
                elif event.key == pygame.K_DOWN:
                    self.vehicle.decelerate()
                elif event.key == pygame.K_LEFT:
                    self.vehicle.change_lane("left")
                elif event.key == pygame.K_RIGHT:
                    self.vehicle.change_lane("right")
                elif event.key == pygame.K_s:  # Stop the car
                    self.vehicle.stop()

    def update(self):
        # Update game state, including vehicle position, obstacle movement, and collision detection
        for obstacle in self.obstacles:
            obstacle.move()
            if obstacle.check_collision(self.vehicle):
                self.handle_slow_down_obstacle(obstacle)
                self.stop_game()
        
        # Add new obstacles periodically
        if random.randint(1, 20) == 1:  # Randomly add an obstacle
            lane = random.randint(0, 2)
            self.obstacles.append(Obstacle(lane))

    def handle_slow_down_obstacle(self, obstacle: Obstacle):
        if obstacle.type == 1:  # Assuming type 1 is a slow down obstacle
            self.vehicle.decelerate()

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        self.display_vehicle_info()
        self.render_obstacles()
        pygame.display.flip()  # Update the display

    def display_vehicle_info(self):
        font = pygame.font.Font(None, 36)
        speed_text = font.render(f'Speed: {self.vehicle.speed}', True, (255, 255, 255))
        distance_text = font.render(f'Distance: {int(self.vehicle.distance)}', True, (255, 255, 255))
        self.screen.blit(speed_text, (10, 10))
        self.screen.blit(distance_text, (10, 50))

    def render_obstacles(self):
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, (255, 0, 0), (obstacle.lane * 200 + 100, obstacle.position, 50, 50))  # Draw obstacles

    def stop_game(self):
        self.running = False
        self.save_data()

    def save_data(self):
        with open('game_data.txt', 'a') as f:
            f.write(f'Score: {self.score}\n')
        self.update_high_scores()

    def load_high_scores(self):
        try:
            with open('high_scores.txt', 'r') as f:
                self.high_score = int(f.readline().strip().split(": ")[1])
        except FileNotFoundError:
            self.high_score = 0

    def update_high_scores(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open('high_scores.txt', 'w') as f:
                f.write(f'High Score: {self.high_score}\n')
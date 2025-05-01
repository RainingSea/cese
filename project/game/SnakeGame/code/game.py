import pygame
import os
from snake import Snake
from food import Food
from score import Score

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = Score()
        self.screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.high_score = self.load_high_score()
        self.is_paused = False
        self.speed_increment_threshold = 5  # Increase speed every 5 points
        self.base_speed = 15  # Base speed
        self.current_speed = self.base_speed

    def start_game(self):
        while self.running:
            self.handle_events()
            if not self.is_paused:
                self.update_game_state()
            self.render()
            self.clock.tick(self.current_speed)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                    self.snake.direction = (0, -1)  # Move up
                elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                    self.snake.direction = (0, 1)   # Move down
                elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                    self.snake.direction = (-1, 0)  # Move left
                elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                    self.snake.direction = (1, 0)   # Move right
                elif event.key == pygame.K_p:
                    self.pause_game()

    def pause_game(self):
        self.is_paused = True
        self.show_pause_menu()

    def show_pause_menu(self):
        while self.is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_paused = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.is_paused = False

    def update_game_state(self):
        self.snake.move()
        if self.check_collision():
            self.end_game()
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.score.increase()
            self.food.generate_food()
            self.adjust_speed()

    def adjust_speed(self):
        if self.score.get_score() % self.speed_increment_threshold == 0:
            self.current_speed += 1  # Increase speed

    def check_collision(self):
        if (self.snake.body[0][0] < 0 or self.snake.body[0][0] >= 600 or
                self.snake.body[0][1] < 0 or self.snake.body[0][1] >= 400 or
                self.snake.check_self_collision()):
            return True
        return False

    def end_game(self):
        print(f"Game Over! Your score was: {self.score.get_score()}")
        if self.score.get_score() > self.high_score:
            self.high_score = self.score.get_score()
            self.save_high_score()
        self.running = False

    def render(self):
        self.screen.fill((0, 0, 0))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], 10, 10))
        self.food.draw(self.screen)  # Draw food using the Food class method
        pygame.display.flip()

    def load_high_score(self):
        if os.path.exists('high_scores.txt'):
            with open('high_scores.txt', 'r') as file:
                return int(file.readline().strip().split('|')[1])  # Load high score from file
        return 0  # Default score if file doesn't exist

    def save_high_score(self):
        with open('high_scores.txt', 'w') as file:
            file.write(f"High Score|{self.high_score}\n")  # Save high score to file
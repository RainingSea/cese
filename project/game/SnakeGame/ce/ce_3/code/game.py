import pygame
from snake import Snake
from food import Food
from score import Score

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = Score()
        self.score_value = 0
        self.game_over = False
        self.generate_food()

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        clock = pygame.time.Clock()
        while not self.game_over:
            self.handle_events()
            self.update_snake('RIGHT')  # Example direction
            self.check_collision()
            screen.fill((0, 0, 0))  # Clear screen
            self.draw(screen)
            pygame.display.flip()
            clock.tick(10)  # Control the game speed

    def generate_food(self) -> None:
        self.food.generate(60, 40)  # Generate food in grid of 60x40

    def update_snake(self, direction: str) -> None:
        self.snake.move(direction)

    def check_collision(self) -> bool:
        head = self.snake.positions[0]
        if head == self.food.position:
            self.snake.grow()
            self.score_value += 1
            self.generate_food()
        if self.snake.check_self_collision() or not (0 <= head[0] < 60 and 0 <= head[1] < 40):
            self.end_game()
            return True
        return False

    def pause_game(self) -> None:
        # Implement pause functionality
        pass

    def end_game(self) -> None:
        self.save_score()

    def save_score(self) -> None:
        self.score.update_score(self.score_value)

    def draw(self, screen) -> None:
        for segment in self.snake.positions:
            pygame.draw.rect(screen, (0, 255, 0), (segment[0] * 10, segment[1] * 10, 10, 10))
        food_pos = self.food.position
        pygame.draw.rect(screen, (255, 0, 0), (food_pos[0] * 10, food_pos[1] * 10, 10, 10))
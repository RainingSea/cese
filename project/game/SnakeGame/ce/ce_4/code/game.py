import pygame
import random

class Snake:
    def __init__(self):
        self.position = [(100, 100), (90, 100), (80, 100)]
        self.length = 3

    def move(self, direction: str) -> None:
        head_x, head_y = self.position[0]
        if direction == 'UP':
            head_y -= 10
        elif direction == 'DOWN':
            head_y += 10
        elif direction == 'LEFT':
            head_x -= 10
        elif direction == 'RIGHT':
            head_x += 10
        self.position.insert(0, (head_x, head_y))
        if len(self.position) > self.length:
            self.position.pop()

    def grow(self) -> None:
        self.length += 1

    def get_head_position(self) -> tuple:
        return self.position[0]

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn_food()

    def spawn_food(self) -> None:
        self.position = (random.randint(0, 39) * 10, random.randint(0, 29) * 10)

    def get_position(self) -> tuple:
        return self.position

class Score:
    def __init__(self):
        self.current_score = 0

    def increase(self) -> None:
        self.current_score += 1

    def get_score(self) -> int:
        return self.current_score

    def save_highscore(self) -> None:
        with open('highscore.txt', 'w') as file:
            file.write(str(self.current_score))

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = Score()
        self.is_paused = False

    def start_game(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.run_game()

    def pause_game(self) -> None:
        self.is_paused = True

    def resume_game(self) -> None:
        self.is_paused = False

    def check_collision(self) -> bool:
        if self.snake.get_head_position() == self.food.get_position():
            self.snake.grow()
            self.food.spawn_food()
            self.score.increase()
            return True
        return False

    def update_score(self) -> None:
        if self.score.current_score > 0 and self.score.current_score % 10 == 0:
            self.score.save_highscore()

    def run_game(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            if not self.is_paused:
                self.snake.move('RIGHT')  # For simplicity, always move right
                self.check_collision()
                self.update_score()
            self.screen.fill((0, 0, 0))
            for segment in self.snake.position:
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], 10, 10))
            food_position = self.food.get_position()
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(food_position[0], food_position[1], 10, 10))
            pygame.display.flip()
            self.clock.tick(15)
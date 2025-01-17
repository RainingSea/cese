import pygame
import random

class Score:
    def __init__(self) -> None:
        self.current_score = 0

    def increment(self) -> None:
        self.current_score += 1

    def get_score(self) -> int:
        return self.current_score

class Food:
    def __init__(self) -> None:
        self.position = self.generate_new_position()

    def generate_new_position(self) -> None:
        self.position = (random.randint(0, 19), random.randint(0, 19))

class Snake:
    def __init__(self) -> None:
        self.body = [(10, 10)]
        self.direction = 'RIGHT'

    def move(self) -> None:
        head_x, head_y = self.body[0]
        if self.direction == 'UP':
            head_y -= 1
        elif self.direction == 'DOWN':
            head_y += 1
        elif self.direction == 'LEFT':
            head_x -= 1
        elif self.direction == 'RIGHT':
            head_x += 1
        self.body.insert(0, (head_x, head_y))
        self.body.pop()

    def grow(self) -> None:
        self.body.append(self.body[-1])

    def check_self_collision(self) -> bool:
        return len(self.body) != len(set(self.body))

class Game:
    def __init__(self) -> None:
        self.snake = Snake()
        self.food = Food()
        self.score = Score()
        self.is_paused = False

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((400, 400))
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                        self.snake.direction = 'UP'
                    elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                        self.snake.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                        self.snake.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                        self.snake.direction = 'RIGHT'
                    elif event.key == pygame.K_p:
                        self.pause()

            if not self.is_paused:
                self.snake.move()
                if self.snake.body[0] == self.food.position:
                    self.snake.grow()
                    self.food.generate_new_position()
                    self.update_score()

                if self.check_collision():
                    self.save_high_score()
                    pygame.quit()
                    return

            screen.fill((0, 0, 0))
            for segment in self.snake.body:
                pygame.draw.rect(screen, (0, 255, 0), (segment[0]*20, segment[1]*20, 20, 20))
            pygame.draw.rect(screen, (255, 0, 0), (self.food.position[0]*20, self.food.position[1]*20, 20, 20))
            pygame.display.flip()
            clock.tick(10)

    def pause(self) -> None:
        self.is_paused = True

    def resume(self) -> None:
        self.is_paused = False

    def check_collision(self) -> bool:
        head = self.snake.body[0]
        return (head[0] < 0 or head[0] >= 20 or head[1] < 0 or head[1] >= 20 or 
                self.snake.check_self_collision())

    def update_score(self) -> None:
        self.score.increment()

    def save_high_score(self) -> None:
        with open('highscores.txt', 'a') as f:
            f.write(f"{self.score.get_score()}\n")
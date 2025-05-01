import pygame
from snake import Snake
from food import Food
from score import Score

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = Score()
        self.is_paused = False
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Snake Game")

    def start_game(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            if not self.is_paused:
                self.update_game()
            self.render()
            clock.tick(15)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_game()
                elif event.key == pygame.K_UP:
                    self.snake.direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    self.snake.direction = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    self.snake.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    self.snake.direction = 'RIGHT'

    def pause_game(self):
        self.is_paused = True
        self.display_pause_menu()

    def resume_game(self):
        self.is_paused = False

    def display_pause_menu(self):
        font = pygame.font.Font(None, 74)
        text = font.render("Paused", True, (255, 255, 255))
        self.screen.blit(text, (350, 250))
        pygame.display.flip()
        while self.is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.resume_game()

    def update_game(self):
        self.snake.move()
        if self.check_collision():
            pygame.quit()
            exit()
        if self.snake.segments[0].position == self.food.position:
            self.snake.grow()
            self.food.generate_food()
            self.score.increase()

    def check_collision(self):
        return self.snake.check_self_collision()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.display_score()
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score.get_score()}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
import pygame
from snake import Snake
from food import Food

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.is_paused = False
        self.screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption('Snake Game')

    def start_game(self):
        while True:
            self.check_events()
            if not self.is_paused:
                self.update()
                self.draw()
            pygame.display.flip()

    def update(self):
        self.snake.move()
        self.check_collisions()

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.display_score()

    def check_collisions(self):
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            self.food.spawn_food()
            self.score += 1

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause_game()

    def pause_game(self):
        self.is_paused = True
        self.show_pause_menu()

    def resume_game(self):
        self.is_paused = False

    def show_pause_menu(self):
        # Placeholder for pause menu display
        pass

    def display_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
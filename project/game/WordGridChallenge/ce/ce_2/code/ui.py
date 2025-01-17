import pygame
from game import Game

class UI:
    def __init__(self, game: Game):
        self.game = game
        self.window_size = (600, 600)
        self.font = pygame.font.Font(None, 36)
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Word Grid Challenge")
    
    def create_window(self) -> None:
        self.screen.fill((255, 255, 255))
        self.draw_grid()
        self.update_score_display()
        self.show_timer()
        pygame.display.flip()

    def draw_grid(self) -> None:
        grid_size = len(self.game.grid)
        cell_size = self.window_size[0] // grid_size
        for i in range(grid_size):
            for j in range(grid_size):
                pygame.draw.rect(self.screen, (0, 0, 0), (j * cell_size, i * cell_size, cell_size, cell_size), 1)
                text_surface = self.font.render(self.game.grid[i][j], True, (0, 0, 0))
                self.screen.blit(text_surface, (j * cell_size + cell_size // 4, i * cell_size + cell_size // 4))

    def update_score_display(self) -> None:
        score_surface = self.font.render(f"Score: {self.game.score}", True, (0, 0, 0))
        self.screen.blit(score_surface, (10, 10))

    def show_timer(self) -> None:
        elapsed_time = int(time.time() - self.game.timer)
        timer_surface = self.font.render(f"Time: {elapsed_time}s", True, (0, 0, 0))
        self.screen.blit(timer_surface, (10, 50))
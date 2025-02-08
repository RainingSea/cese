import pygame
from game import Game

class UI:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("2048 Game")
        self.font = pygame.font.Font(None, 40)

    def draw_board(self) -> None:
        self.screen.fill((187, 173, 160))
        for i in range(4):
            for j in range(4):
                tile_value = self.game.board[i][j]
                self.draw_tile(i, j, tile_value)
        pygame.display.flip()

    def draw_tile(self, i: int, j: int, value: int) -> None:
        x = j * 100
        y = i * 100
        pygame.draw.rect(self.screen, self.get_tile_color(value), (x, y, 100, 100))
        if value != 0:
            text = self.font.render(str(value), True, (255, 255, 255))
            text_rect = text.get_rect(center=(x + 50, y + 50))
            self.screen.blit(text, text_rect)

    def get_tile_color(self, value: int) -> tuple:
        colors = {
            0: (205, 193, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46),
        }
        return colors.get(value, (60, 58, 50))

    def display_score(self) -> None:
        score_text = self.font.render(f'Score: {self.game.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

    def show_game_over(self) -> None:
        game_over_text = self.font.render('Game Over', True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(200, 200))
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()
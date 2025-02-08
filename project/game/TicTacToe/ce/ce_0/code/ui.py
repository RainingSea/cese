import pygame
from game import Game

class UI:
    def __init__(self, game: Game):
        self.game = game
        self.screen = pygame.display.set_mode((300, 300))
        pygame.display.set_caption('Tic-Tac-Toe')
        self.font = pygame.font.Font(None, 74)

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        for row in range(3):
            for col in range(3):
                if self.game.board[row][col] != '':
                    text = self.font.render(self.game.board[row][col], True, (0, 0, 0))
                    self.screen.blit(text, (col * 100 + 30, row * 100 + 10))
        pygame.display.flip()

    def display_result(self, result: str):
        self.screen.fill((255, 255, 255))
        text = self.font.render(result, True, (0, 0, 0))
        self.screen.blit(text, (30, 100))
        pygame.display.flip()
        pygame.time.wait(2000)

    def restart_game(self):
        self.game.reset_game()
        self.draw_board()
import pygame
import sys
from game import Game

class Main:
    def __init__(self):
        self.game = Game()
        self.width, self.height = 300, 300
        self.cell_size = self.width // 3
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tic-Tac-Toe")
        self.font = pygame.font.Font(None, 36)

    def draw_board(self):
        for row in range(3):
            for col in range(3):
                pygame.draw.rect(self.screen, (255, 255, 255), (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 1)
                if self.game.board[row][col]:
                    text = self.font.render(self.game.board[row][col], True, (0, 0, 0))
                    self.screen.blit(text, (col * self.cell_size + self.cell_size // 4, row * self.cell_size + self.cell_size // 4))

    def display_status(self):
        status_text = "Draw!" if self.game.is_draw else f"Current Player: {self.game.current_player}"
        if self.game.winner:
            status_text = f"Winner: {self.game.winner}"
        text = self.font.render(status_text, True, (0, 0, 0))
        self.screen.blit(text, (10, self.height - 40))

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.save_result()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    row, col = y // self.cell_size, x // self.cell_size
                    self.game.play_move(row, col)

            self.screen.fill((0, 0, 0))
            self.draw_board()
            self.display_status()
            pygame.display.flip()

if __name__ == "__main__":
    Main().main()
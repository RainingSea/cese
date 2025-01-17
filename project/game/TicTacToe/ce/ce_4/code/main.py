import pygame
import sys
from game import Game

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
CELL_SIZE = SCREEN_WIDTH // 3

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tic-Tac-Toe")
        self.game = Game()
        self.font = pygame.font.Font(None, 36)
        self.running = True

    def draw_board(self):
        self.screen.fill(BG_COLOR)
        for row in range(1, 3):
            pygame.draw.line(self.screen, LINE_COLOR, (0, row * CELL_SIZE), (SCREEN_WIDTH, row * CELL_SIZE), 2)
            pygame.draw.line(self.screen, LINE_COLOR, (row * CELL_SIZE, 0), (row * CELL_SIZE, SCREEN_HEIGHT), 2)

        for r in range(3):
            for c in range(3):
                if self.game.board[r][c] != '':
                    text = self.font.render(self.game.board[r][c], True, LINE_COLOR)
                    self.screen.blit(text, (c * CELL_SIZE + CELL_SIZE // 4, r * CELL_SIZE + CELL_SIZE // 4))

    def run(self):
        while self.running:
            self.handle_events()
            self.draw_board()
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                self.game.play_move(row, col)

        if not self.running:
            pygame.quit()
            sys.exit()

def main():
    app = Main()
    app.run()

if __name__ == "__main__":
    main()
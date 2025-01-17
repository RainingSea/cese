import pygame
import sys
from game import Game

def main() -> None:
    game = Game()
    game.draw_board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x //= game.cell_size
                y //= game.cell_size
                if game.place_piece(x, y):
                    if game.check_victory():
                        game.display_winner()
                        game.save_results()
                    game.switch_player()
                    game.draw_board()

if __name__ == "__main__":
    main()
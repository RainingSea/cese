import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = event.pos
                    grid_x, grid_y = x // 40, y // 40
                    game.place_piece(grid_x, grid_y)

        game.draw_board()
        if game.check_victory():
            print(f"{'Black' if game.current_turn == 'white' else 'White'} wins!")
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
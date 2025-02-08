import pygame
from game import Game
from ui import UI

def main():
    pygame.init()
    game = Game()
    ui = UI(game)
    ui.draw_board()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // 100, x // 100
                if game.play_move(row, col):
                    ui.draw_board()
                    winner = game.check_winner()
                    if winner:
                        ui.display_result(winner)
                        game.reset_game()
                        ui.draw_board()

    pygame.quit()

if __name__ == "__main__":
    main()
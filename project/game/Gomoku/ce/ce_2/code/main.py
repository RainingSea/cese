import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Gomoku')
    game = Game()
    game.load_game_state()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                x, y = event.pos
                grid_x, grid_y = x // 40, y // 40
                if game.place_piece(grid_x, grid_y):
                    if game.check_victory():
                        game.save_game_state()
        
        game.draw_board(screen)
        game.display_winner(screen)
        pygame.display.flip()

    game.save_game_state()
    pygame.quit()

if __name__ == '__main__':
    main()
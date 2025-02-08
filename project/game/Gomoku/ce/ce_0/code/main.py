import pygame
from game import Game

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Gomoku Game')

def main() -> None:
    game = Game()
    game.load_game()
    running = True

    while running:
        screen.fill((255, 255, 255))
        game.draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                grid_x, grid_y = x // 40, y // 40
                game.place_piece(grid_x, grid_y)
        
        if game.winner:
            font = pygame.font.Font(None, 74)
            text = font.render(f'{game.winner} wins!', True, (0, 0, 0))
            screen.blit(text, (150, 250))

        pygame.display.flip()

    game.save_game()
    pygame.quit()

if __name__ == '__main__':
    main()
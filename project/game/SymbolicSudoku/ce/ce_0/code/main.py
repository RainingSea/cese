import pygame
from game import Game, Difficulty

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Symbolic Sudoku Challenge")
    
    game = Game()
    game.start_game(Difficulty.easy)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game rendering and logic would go here

    pygame.quit()

if __name__ == "__main__":
    main()
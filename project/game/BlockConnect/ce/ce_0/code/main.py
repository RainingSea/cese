import pygame
from game import Game

def main() -> None:
    pygame.init()
    game = Game()
    game.load_game_state()
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Additional event handling here

        game.display_grid()
        pygame.display.flip()

    game.save_game_state()
    pygame.quit()

if __name__ == "__main__":
    main()
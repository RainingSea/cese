import pygame
from game import Game

def main() -> str:
    pygame.init()
    game = Game()
    game.load_best_time()
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic and rendering would go here
        game.update()
        game.draw()

    pygame.quit()
    return "Game Over!"

if __name__ == "__main__":
    main()
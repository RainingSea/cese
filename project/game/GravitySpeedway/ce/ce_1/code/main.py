import pygame
from game import Game

def main() -> None:
    pygame.init()
    game = Game()
    game.load_high_scores()
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()
        game.render()

    pygame.quit()

if __name__ == "__main__":
    main()
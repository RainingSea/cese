import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.start_game()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Here we would typically update the game state and render the game
        game.letter_grid.display_grid()
        print(f'Score: {game.score.get_score()}')
        print(f'Time Remaining: {game.timer.time_remaining}')

        pygame.display.flip()

    game.save_progress()
    pygame.quit()

if __name__ == "__main__":
    main()
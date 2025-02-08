import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.start_game(difficulty=1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Here would be the code to update the display and handle user input
        # For now, we will just display the grid in the console
        game.grid.display()
        print("Elapsed Time:", game.timer.get_elapsed_time(), "seconds")

    pygame.quit()

if __name__ == "__main__":
    main()
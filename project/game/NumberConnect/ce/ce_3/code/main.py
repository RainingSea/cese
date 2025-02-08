import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.start_game()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update timer and check if time is up
        game.timer.update_timer()
        if game.timer.is_time_up():
            print("Time is up!")
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
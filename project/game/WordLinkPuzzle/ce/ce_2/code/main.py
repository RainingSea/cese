import pygame
from game import Game

def main() -> str:
    pygame.init()
    game = Game()
    game.start_game()
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state
        game.timer.update_timer()
        if game.timer.is_time_up():
            print("Time's up! Your score:", game.score.get_score())
            running = False

    game.save_progress()
    pygame.quit()
    return "Game Over"

if __name__ == "__main__":
    main()
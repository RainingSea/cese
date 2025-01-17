import pygame
import time
from game import MemoryGame

def main() -> None:
    pygame.init()
    game = MemoryGame()
    game.start_game()
    
    # Main game loop
    running = True
    start_time = time.time()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Handle card flipping with key presses (for demo purposes)
                if event.key == pygame.K_1:
                    game.handle_card_flip(0)
                elif event.key == pygame.K_2:
                    game.handle_card_flip(1)
                elif event.key == pygame.K_3:
                    game.handle_card_flip(2)
                elif event.key == pygame.K_4:
                    game.handle_card_flip(3)
                elif event.key == pygame.K_5:
                    game.handle_card_flip(4)
                elif event.key == pygame.K_6:
                    game.handle_card_flip(5)
                elif event.key == pygame.K_7:
                    game.handle_card_flip(6)
                elif event.key == pygame.K_8:
                    game.handle_card_flip(7)

        # Example of updating score based on time taken
        if game.game_active:
            elapsed_time = time.time() - start_time
            game.update_timer(elapsed_time)  # Update the timer

    pygame.quit()

if __name__ == "__main__":
    main()
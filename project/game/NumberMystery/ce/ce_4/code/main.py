import pygame
from game import Game

def main() -> str:
    pygame.init()
    game = Game()
    game.load_puzzles('puzzles.txt')
    game.start_game()
    
    # Main loop (simplified for this example)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Here you would handle user input for submitting answers and requesting hints

    pygame.quit()
    return "Game ended."

if __name__ == "__main__":
    main()
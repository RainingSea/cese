import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.load_data()
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Logic to display the puzzle and handle user input
        game.display_puzzle()
        
    pygame.quit()

if __name__ == "__main__":
    main()
import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    
    # Main menu loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Here you would handle drawing the menu and user input
        # For now, we will just call the game methods directly for demo purposes
        game.create_team("MyTeam", "path/to/logo.png")
        players = game.scout_players()
        print(players)  # Display available players for testing

    pygame.quit()

if __name__ == "__main__":
    main()
import pygame
from game import Game
from ui import UI

def main():
    game = Game()
    game.load_words("words.txt")
    game.generate_grid(5)
    game.start_timer()
    
    ui = UI(game)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        ui.create_window()
    
    pygame.quit()

if __name__ == "__main__":
    main()
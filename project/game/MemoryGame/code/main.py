import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.load_game_state()
    game.start_game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_game_state()
                pygame.quit()
                return
            game.handle_event(event)
        game.update_display()
        pygame.display.flip()

if __name__ == "__main__":
    main()
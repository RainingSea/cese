import pygame
from game import Game

def main():
    game = Game()
    game.start()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.handle_input()
        game.update()
        game.check_collisions()
        game.draw()
        
        if game.timer <= 0:
            game.save_score()
            running = False
        
        game.clock.tick(60)  # Maintain 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
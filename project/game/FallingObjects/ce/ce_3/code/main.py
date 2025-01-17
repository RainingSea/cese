import pygame
from game import Game

def main():
    game = Game()
    game.start_game()
    
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.basket.move_left()
        if keys[pygame.K_RIGHT]:
            game.basket.move_right()

        game.update()

    game.end_game()

if __name__ == "__main__":
    main()
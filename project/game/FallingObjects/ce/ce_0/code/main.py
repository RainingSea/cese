import pygame
from game import Game

def main():
    game = Game()
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.basket.move_left()
        if keys[pygame.K_RIGHT]:
            game.basket.move_right()

        game.update()
        game.render()
        game.clock.tick(60)  # Set frame rate to 60 FPS

    game.end_game()

if __name__ == "__main__":
    main()
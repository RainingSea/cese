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
            game.paddle.move('left')
        if keys[pygame.K_RIGHT]:
            game.paddle.move('right')

        game.update()
        game.draw()
        game.save_game_state()
        game.clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
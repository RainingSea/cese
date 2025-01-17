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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Example: Place bomb on space key
                    bomb = game.player.place_bomb()
                    game.bombs.append(bomb)
                elif event.key == pygame.K_UP:
                    game.player.move('up')
                elif event.key == pygame.K_DOWN:
                    game.player.move('down')
                elif event.key == pygame.K_LEFT:
                    game.player.move('left')
                elif event.key == pygame.K_RIGHT:
                    game.player.move('right')

        game.update_game()
        game.check_collisions()
        game.display_ui()

    pygame.quit()

if __name__ == "__main__":
    main()
import pygame
from game import Game

def main():
    game = Game()
    game.start()

    while game.running:
        game.handle_input()
        game.update()
        game.check_collisions()
        game.render()
        game.clock.tick(60)

    game.end_game()

if __name__ == "__main__":
    main()
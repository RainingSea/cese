import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.start_game("Logic Puzzles")  # Starting with Logic Puzzles for demo

if __name__ == "__main__":
    main()
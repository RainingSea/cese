from game import Game
import pygame

def main():
    pygame.init()  # Initialize Pygame
    game = Game()
    game.show_main_menu()
    pygame.quit()  # Ensure Pygame quits after the game ends

if __name__ == "__main__":
    main()
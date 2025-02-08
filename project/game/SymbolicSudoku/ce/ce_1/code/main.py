import pygame
from game import Game, DifficultyLevel

def main():
    pygame.init()
    game = Game()
    game.start_game(DifficultyLevel.EASY)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.display()  # This would be a method to update the display

    pygame.quit()

if __name__ == "__main__":
    main()
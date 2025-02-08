import pygame
from game import Game

def main() -> None:
    pygame.init()
    game = Game()
    images = ['image1.png', 'image2.png', 'image3.png', 'image4.png']  # Sample images
    game.start_game(images)

    # Main game loop (simplified)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
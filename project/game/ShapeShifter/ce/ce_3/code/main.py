import pygame
from game import Game, Shape

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Shape Shifter Puzzle Game")

    shapes = [
        Shape("circle", (0, 0), 0),
        Shape("square", (1, 1), 0),
        Shape("triangle", (2, 2), 0),
        Shape("rectangle", (3, 3), 0)
    ]
    target_pattern = [("circle", (0, 0), 0), ("square", (1, 1), 0), ("triangle", (2, 2), 0), ("rectangle", (3, 3), 0)]
    game = Game(shapes, target_pattern)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic and rendering would go here

    pygame.quit()

if __name__ == "__main__":
    main()
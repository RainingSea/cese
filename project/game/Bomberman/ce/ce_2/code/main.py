import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((520, 520))
    pygame.display.set_caption("Bomberman Game")

    game = Game()
    game.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.handle_input()
        game.update()

        screen.fill((255, 255, 255))
        game.render(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
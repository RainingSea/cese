import pygame
from game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Treasure Hunt Game")
    clock = pygame.time.Clock()

    game = Game()
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            game.player.move('up')
        if keys[pygame.K_DOWN]:
            game.player.move('down')
        if keys[pygame.K_LEFT]:
            game.player.move('left')
        if keys[pygame.K_RIGHT]:
            game.player.move('right')

        game.update()

        screen.fill((255, 255, 255))  # Clear screen with white
        # Render maze, player, and other UI elements here
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
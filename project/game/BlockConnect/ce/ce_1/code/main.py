import pygame
from game import Game

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Block Game")

def main() -> None:
    game = Game()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                game.select_block(y // 50, x // 50)

        screen.fill((0, 0, 0))
        game.draw_grid()
        pygame.display.flip()
        clock.tick(60)

    game.save_game_state()
    pygame.quit()

if __name__ == "__main__":
    main()
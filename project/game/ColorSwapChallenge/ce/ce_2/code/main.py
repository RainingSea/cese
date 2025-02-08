import pygame
from game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Color Swap Challenge")
    clock = pygame.time.Clock()
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Clear screen with white
        draw_grid(screen, game.grid)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def draw_grid(screen, grid) -> None:
    block_size = 70
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            color = grid[x][y].color
            pygame.draw.rect(screen, color, (y * block_size, x * block_size, block_size, block_size))

if __name__ == "__main__":
    main()
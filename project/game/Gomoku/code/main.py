import pygame
from game import Game

# Constants
WIDTH, HEIGHT = 600, 600
BACKGROUND_COLOR = (255, 204, 0)
GRID_COLOR = (0, 0, 0)
LINE_WIDTH = 2

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gomoku")
    clock = pygame.time.Clock()
    game = Game()
    game.load_game_state()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                grid_x, grid_y = x // (WIDTH // 15), y // (HEIGHT // 15)
                if game.place_piece(grid_x, grid_y):
                    game.save_game_state()

        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen)
        draw_pieces(screen, game)
        pygame.display.flip()
        clock.tick(60)

    if game.winner:
        game.save_results()

    pygame.quit()

def draw_grid(screen):
    for i in range(16):
        pygame.draw.line(screen, GRID_COLOR, (i * (WIDTH // 15), 0), (i * (WIDTH // 15), HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, GRID_COLOR, (0, i * (HEIGHT // 15)), (WIDTH, i * (HEIGHT // 15)), LINE_WIDTH)

def draw_pieces(screen, game):
    for x in range(15):
        for y in range(15):
            piece = game.board[x][y]
            if piece == 'black':
                pygame.draw.circle(screen, (0, 0, 0), (x * (WIDTH // 15) + (WIDTH // 30), y * (HEIGHT // 15) + (HEIGHT // 30)), (WIDTH // 30) // 2)
            elif piece == 'white':
                pygame.draw.circle(screen, (255, 255, 255), (x * (WIDTH // 15) + (WIDTH // 30), y * (HEIGHT // 15) + (HEIGHT // 30)), (WIDTH // 30) // 2)

if __name__ == "__main__":
    main()
import pygame
from game import Game

# Constants
WINDOW_SIZE = 400
GRID_SIZE = 4
TILE_SIZE = WINDOW_SIZE // GRID_SIZE
BACKGROUND_COLOR = (187, 173, 160)
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 40

def draw_board(screen, game):
    screen.fill(BACKGROUND_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = game.board[i][j]
            if value != 0:
                pygame.draw.rect(screen, (255, 255, 255), (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                font = pygame.font.Font(None, FONT_SIZE)
                text = font.render(str(value), True, FONT_COLOR)
                text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, (205, 193, 180), (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    score_text = font.render(f'Score: {game.score}', True, FONT_COLOR)
    screen.blit(score_text, (10, 10))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption('2048 Game')
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if game.move('up'):
                        game.generate_tile()
                elif event.key == pygame.K_DOWN:
                    if game.move('down'):
                        game.generate_tile()
                elif event.key == pygame.K_LEFT:
                    if game.move('left'):
                        game.generate_tile()
                elif event.key == pygame.K_RIGHT:
                    if game.move('right'):
                        game.generate_tile()

        draw_board(screen, game)
        if game.check_game_over():
            font = pygame.font.Font(None, FONT_SIZE)
            game_over_text = font.render('Game Over', True, FONT_COLOR)
            screen.blit(game_over_text, (WINDOW_SIZE // 2 - 60, WINDOW_SIZE // 2 - 20))
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
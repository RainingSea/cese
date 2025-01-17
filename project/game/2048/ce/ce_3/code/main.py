import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 450))
    pygame.display.set_caption("2048 Game")
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move('left')
                elif event.key == pygame.K_RIGHT:
                    game.move('right')
                elif event.key == pygame.K_UP:
                    game.move('up')
                elif event.key == pygame.K_DOWN:
                    game.move('down')
                if game.check_game_over():
                    print("Game Over!")

        screen.fill((255, 255, 255))
        draw_board(screen, game)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def draw_board(screen, game):
    for i in range(4):
        for j in range(4):
            tile_value = game.board[i][j].value
            color = (205, 193, 180) if tile_value == 0 else (238, 228, 218)
            pygame.draw.rect(screen, color, (j * 100, i * 100, 100, 100))
            if tile_value != 0:
                font = pygame.font.Font(None, 74)
                text = font.render(str(tile_value), True, (0, 0, 0))
                screen.blit(text, (j * 100 + 30, i * 100 + 20))

if __name__ == "__main__":
    main()
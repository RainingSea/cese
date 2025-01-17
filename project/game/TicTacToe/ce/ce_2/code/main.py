import pygame
from game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((300, 400))
    pygame.display.set_caption("Tic-Tac-Toe")
    clock = pygame.time.Clock()
    game = Game()
    game.load_game_data()

    font = pygame.font.Font(None, 36)
    running = True

    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // 100, x // 100
                result = game.play_move(row, col)
                if result != "Invalid move":
                    game.save_game_data()

        for row in range(3):
            for col in range(3):
                color = (200, 200, 200) if game.board[row][col] == "" else (0, 255, 0) if game.board[row][col] == "X" else (255, 0, 0)
                pygame.draw.rect(screen, color, (col * 100, row * 100, 100, 100), 0)
                if game.board[row][col] != "":
                    text = font.render(game.board[row][col], True, (0, 0, 0))
                    screen.blit(text, (col * 100 + 35, row * 100 + 30))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
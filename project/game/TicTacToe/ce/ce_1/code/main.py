import pygame
from game import Game

# Constants
WIDTH, HEIGHT = 300, 300
CELL_SIZE = WIDTH // 3
FPS = 60

def draw_board(game: Game):
    for row in range(3):
        for col in range(3):
            pygame.draw.rect(screen, (255, 255, 255), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
            if game.board[row][col] != ' ':
                font = pygame.font.Font(None, 74)
                text = font.render(game.board[row][col], True, (0, 0, 0))
                screen.blit(text, (col * CELL_SIZE + 20, row * CELL_SIZE + 10))

def display_message(message: str):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

def get_user_input() -> tuple[int, int]:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return None
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            return y // CELL_SIZE, x // CELL_SIZE
    return None

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()

# Game loop
game = Game()
game.start_timer()
running = True
while running:
    screen.fill((0, 0, 0))
    draw_board(game)
    if game.game_over:
        display_message("Game Over! Press R to restart.")
    else:
        user_input = get_user_input()
        if user_input:
            game.play_move(*user_input)

    pygame.display.flip()
    clock.tick(FPS)

    if game.game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game.restart_game()
            game.start_timer()

pygame.quit()
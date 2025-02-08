import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Sokoban Game')
    clock = pygame.time.Clock()

    game = Game()
    game.load_level('level.txt')  # Load the level from a file

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move_player('UP')
                elif event.key == pygame.K_DOWN:
                    game.move_player('DOWN')
                elif event.key == pygame.K_LEFT:
                    game.move_player('LEFT')
                elif event.key == pygame.K_RIGHT:
                    game.move_player('RIGHT')

        screen.fill((255, 255, 255))
        draw_board(screen, game.board, game.player_position)
        pygame.display.flip()
        clock.tick(60)

    game.save_game_state()  # Save the game state before exiting
    pygame.quit()

def draw_board(screen, board, player_position):
    tile_size = 40
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, (0, 0, 0), (x * tile_size, y * tile_size, tile_size, tile_size))
            elif cell == 'G':
                pygame.draw.rect(screen, (0, 255, 0), (x * tile_size, y * tile_size, tile_size, tile_size))
            elif cell == 'P':
                pygame.draw.rect(screen, (0, 0, 255), (x * tile_size, y * tile_size, tile_size, tile_size))

if __name__ == '__main__':
    main()
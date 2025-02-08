import pygame
from game import Game
from ui import UI

def main() -> None:
    pygame.init()
    game = Game()
    ui = UI(game)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move('up')
                elif event.key == pygame.K_DOWN:
                    game.move('down')
                elif event.key == pygame.K_LEFT:
                    game.move('left')
                elif event.key == pygame.K_RIGHT:
                    game.move('right')

        ui.draw_board()
        ui.display_score()

        if game.check_game_over():
            ui.show_game_over()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
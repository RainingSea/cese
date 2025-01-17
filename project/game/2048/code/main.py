import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 500))
    pygame.display.set_caption("2048 Game")
    clock = pygame.time.Clock()
    game = Game()
    game.start_game()

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
                elif event.key == pygame.K_s:
                    game.save_game()
                elif event.key == pygame.K_l:
                    game.load_game()

        screen.fill((187, 173, 160))
        # Drawing code for the board and score goes here
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
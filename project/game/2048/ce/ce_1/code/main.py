import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.start_game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    direction = pygame.key.name(event.key)
                    game.move(direction)
                elif event.key == pygame.K_s:
                    game.save_game()
                elif event.key == pygame.K_l:
                    game.load_game()
        game.check_game_over()
        pygame.display.flip()

if __name__ == "__main__":
    main()
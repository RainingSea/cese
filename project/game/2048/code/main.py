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
                if event.key == pygame.K_UP:
                    game.move("up")
                elif event.key == pygame.K_DOWN:
                    game.move("down")
                elif event.key == pygame.K_LEFT:
                    game.move("left")
                elif event.key == pygame.K_RIGHT:
                    game.move("right")
                elif event.key == pygame.K_s:
                    game.save_game_state("game_state.txt")
                elif event.key == pygame.K_l:
                    game.load_game_state("game_state.txt")

        game.check_game_over()
        pygame.display.flip()

if __name__ == "__main__":
    main()
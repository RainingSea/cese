import pygame
from game import Game

def main() -> None:
    pygame.init()
    game = Game()
    game.score_manager.load_scores('scores.txt')
    game.maze.load_maze('mazes.txt')
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.render()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
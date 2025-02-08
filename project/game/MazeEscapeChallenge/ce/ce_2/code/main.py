import pygame
from game import Game

def main() -> str:
    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    
    game = Game()
    game.start_game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_input(event)

        screen.fill((0, 0, 0))
        game.maze.render(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return "Game exited."

if __name__ == "__main__":
    main()
import pygame
from game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Shooting Game')
    
    game = Game()
    game.start_game()
    
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game.update()
        game.render(screen)
        
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second

    game.save_score(game.score)
    pygame.quit()

if __name__ == '__main__':
    main()
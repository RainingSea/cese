import pygame
from game import Game

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
FPS = 60

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048 Game")
    clock = pygame.time.Clock()
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    game.move('w')
                elif event.key == pygame.K_a:
                    game.move('a')
                elif event.key == pygame.K_s:
                    game.move('s')
                elif event.key == pygame.K_d:
                    game.move('d')
        
        screen.fill((255, 255, 255))
        game.display_board()  # Placeholder for actual rendering logic
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
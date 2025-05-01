import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 400))
    pygame.display.set_caption('Tic-Tac-Toe')
    
    game = Game()
    game.start_game()
    
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    x, y = event.pos
                    game.make_move(x // 100, y // 100)
        
        screen.fill((255, 255, 255))
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
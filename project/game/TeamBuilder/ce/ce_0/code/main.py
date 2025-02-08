import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Team Management Game")
    
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))
        # Here you would add code to draw buttons and handle UI interactions
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
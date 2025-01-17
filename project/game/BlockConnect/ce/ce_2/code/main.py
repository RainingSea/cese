import pygame
from game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Block Connect Game")
    
    game = Game()
    game.load_state()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                game.select_block(x // 100, y // 100)  # Assuming each block is 100x100 pixels
        
        screen.fill((255, 255, 255))  # Clear screen
        for i, row in enumerate(game.grid):
            for j, block in enumerate(row):
                color = (255, 255, 255) if block.color == "white" else block.color
                pygame.draw.rect(screen, color, (j * 100, i * 100, 100, 100))
        
        pygame.display.flip()
    
    game.save_state()
    pygame.quit()

if __name__ == "__main__":
    main()
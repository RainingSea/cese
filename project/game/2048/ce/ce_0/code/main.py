import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 500))
    pygame.display.set_caption("2048 Game")
    
    game = Game()
    game.initialize_board()
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
        
        screen.fill((255, 255, 255))
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
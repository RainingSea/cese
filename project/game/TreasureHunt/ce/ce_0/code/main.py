import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Treasure Hunt Game")
    clock = pygame.time.Clock()
    
    game = Game()
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.player.move('UP')
                elif event.key == pygame.K_DOWN:
                    game.player.move('DOWN')
                elif event.key == pygame.K_LEFT:
                    game.player.move('LEFT')
                elif event.key == pygame.K_RIGHT:
                    game.player.move('RIGHT')

        game.update()
        screen.fill((255, 255, 255))
        game.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
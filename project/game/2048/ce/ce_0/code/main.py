import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption('2048 Game')
    clock = pygame.time.Clock()
    
    game = Game()
    game.start_game()

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_game_state()
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move('up')
                elif event.key == pygame.K_DOWN:
                    game.move('down')
                elif event.key == pygame.K_LEFT:
                    game.move('left')
                elif event.key == pygame.K_RIGHT:
                    game.move('right')

        screen.fill((255, 255, 255))  # Clear screen
        game.draw_board()  # Draw the updated board
        pygame.display.flip()
        clock.tick(60)

    # Display game over message
    print("Game Over! Your score was:", game.score)
    pygame.quit()

if __name__ == '__main__':
    main()
import pygame
from game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Sokoban Game")
    
    game = Game()
    game.load_game_state('game_state.txt')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move_player('up')
                elif event.key == pygame.K_DOWN:
                    game.move_player('down')
                elif event.key == pygame.K_LEFT:
                    game.move_player('left')
                elif event.key == pygame.K_RIGHT:
                    game.move_player('right')

        screen.fill((255, 255, 255))  # Clear the screen
        game.render()  # Render the game state
        pygame.display.flip()  # Update the display

    game.save_game_state('game_state.txt')
    pygame.quit()

if __name__ == "__main__":
    main()
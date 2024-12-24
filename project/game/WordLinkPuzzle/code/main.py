import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Word Puzzle Game")
    
    game = Game()
    game.start_game('Easy')  # Starting the game with 'Easy' difficulty
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Clear screen with white background
        game.grid.display_grid(screen)  # Display the grid on the screen
        game.timer.display_timer(screen)  # Display the timer
        game.score.display_score(screen)  # Display the score
        game.formed_words.display_words(screen)  # Display formed words

        pygame.display.flip()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    main()
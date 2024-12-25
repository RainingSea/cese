import pygame
from game import Game

def initialize_game():
    """Initializes Pygame and creates the game window."""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Word Formation Game")
    return screen

def main():
    """Main function to run the game."""
    screen = initialize_game()
    game = Game()
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause the game
                    game.pause_game()

        screen.fill((255, 255, 255))  # Clear the screen with white
        game.grid.display_grid(screen)  # Display the grid
        display_score(screen, game.score.get_score())  # Display the score
        pygame.display.flip()  # Update the display

        game.timer.update_timer()  # Update the timer
        if not game.timer.check_time():
            running = False  # End game if time runs out

    game.save_progress()  # Save progress before quitting
    pygame.quit()

def display_score(screen, score):
    """Displays the current score on the game screen."""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))  # Display score at the top left

if __name__ == "__main__":
    main()
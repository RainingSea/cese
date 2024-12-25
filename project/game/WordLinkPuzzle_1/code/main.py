import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.start_game(difficulty='Easy')
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update the display with the current game state
        game.grid.display_grid()
        
        # Display score, timer, and formed words
        display_ui(game)

    pygame.quit()

def display_ui(game: Game):
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 36)

    # Display score
    score_text = f"Score: {game.score.get_score()}"
    score_surface = font.render(score_text, True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    # Display timer
    timer_text = f"Time Left: {game.timer.time_left}"
    timer_surface = font.render(timer_text, True, (255, 255, 255))
    screen.blit(timer_surface, (10, 50))

    # Display formed words
    words_text = "Words: " + ", ".join(game.formed_words.get_words())
    words_surface = font.render(words_text, True, (255, 255, 255))
    screen.blit(words_surface, (10, 90))

    pygame.display.flip()

if __name__ == "__main__":
    main()
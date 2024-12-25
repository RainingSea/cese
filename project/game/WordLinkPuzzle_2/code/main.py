import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Word Formation Game")
    
    game = Game()
    game.start_game()
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))  # Clear screen with white background
        
        # Draw grid
        draw_grid(screen, game.grid.get_letters())
        
        # Draw score
        draw_score(screen, game.score.get_score())
        
        # Draw timer
        draw_timer(screen, game.timer.check_time())
        
        # Draw formed words
        draw_formed_words(screen, game.formed_words)
        
        pygame.display.flip()  # Update the display
        clock.tick(60)  # Limit to 60 frames per second
    
    pygame.quit()

def draw_grid(screen, letters):
    """Draws the letter grid on the screen."""
    font = pygame.font.Font(None, 36)
    for i, row in enumerate(letters):
        for j, letter in enumerate(row):
            text = font.render(letter, True, (0, 0, 0))
            screen.blit(text, (50 + j * 50, 50 + i * 50))

def draw_score(screen, score):
    """Draws the current score on the screen."""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (50, 10))

def draw_timer(screen, time_remaining):
    """Draws the remaining time on the screen."""
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time: {time_remaining}", True, (0, 0, 0))
    screen.blit(timer_text, (650, 10))

def draw_formed_words(screen, formed_words):
    """Draws the list of formed words on the screen."""
    font = pygame.font.Font(None, 36)
    words_text = font.render("Words: " + ", ".join(formed_words), True, (0, 0, 0))
    screen.blit(words_text, (50, 550))
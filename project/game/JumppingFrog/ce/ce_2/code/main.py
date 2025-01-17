import pygame
from game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Jumping Frog Game')
    clock = pygame.time.Clock()
    game = Game()
    game.start_game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()
        game.check_collision()

        # Clear screen
        screen.fill((0, 0, 255))  # Water background

        # Draw platforms
        for platform in game.platforms:
            pygame.draw.rect(screen, (0, 255, 0), (platform.x, platform.y, platform.width, platform.height))

        # Draw frog
        pygame.draw.rect(screen, (255, 0, 0), (game.frog.x, game.frog.y, 20, 20))  # Frog representation

        # Display score and timer
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {game.score}', True, (255, 255, 255))
        timer_text = font.render(f'Timer: {int(game.timer)}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

        if game.timer <= 0:
            game.end_game()
            running = False

    pygame.quit()

if __name__ == '__main__':
    main()
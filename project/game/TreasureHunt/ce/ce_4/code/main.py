import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    game = Game()
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle user input for player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            game.player.move('UP')
        if keys[pygame.K_DOWN]:
            game.player.move('DOWN')
        if keys[pygame.K_LEFT]:
            game.player.move('LEFT')
        if keys[pygame.K_RIGHT]:
            game.player.move('RIGHT')

        # Check if player found the treasure
        if game.player.check_treasure(game.maze.treasure_location):
            game.score.increase_score()
            game.score.save_best_time(game.timer.get_time())
            game.restart_game()

        # Update game state
        game.update()

        # Render
        screen.fill((255, 255, 255))
        game.render(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
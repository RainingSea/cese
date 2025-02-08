import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Battle of Balls")
    
    game = Game()
    game.initialize_game()
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))
        
        # Draw player ball
        pygame.draw.circle(screen, (0, 0, 255), (int(game.player_ball.position[0]), int(game.player_ball.position[1])), int(game.player_ball.size))
        
        # Draw enemy balls
        for enemy in game.enemy_balls:
            pygame.draw.circle(screen, (255, 0, 0), (int(enemy.position[0]), int(enemy.position[1])), int(enemy.size))
        
        game.update()
        game.check_collisions()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
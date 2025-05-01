import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.start_game()
    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.flip_card(pos)
        game.update_display()
    pygame.quit()

if __name__ == "__main__":
    main()
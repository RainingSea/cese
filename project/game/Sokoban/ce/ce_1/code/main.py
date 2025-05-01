import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.load_game_state('game_state.txt')
    
    while True:
        game.render()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move_player('up')
                elif event.key == pygame.K_DOWN:
                    game.move_player('down')
                elif event.key == pygame.K_LEFT:
                    game.move_player('left')
                elif event.key == pygame.K_RIGHT:
                    game.move_player('right')

if __name__ == '__main__':
    main()
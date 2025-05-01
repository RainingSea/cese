import pygame
from game import Game

class Main:
    def __init__(self):
        self.game = Game()

    def main(self):
        pygame.init()
        self.game.start_game()
        self.run_game_loop()

    def run_game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x, y = pos[0] // 100, pos[1] // 100
                    self.game.make_move(x, y)

            self.game.update_display()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()
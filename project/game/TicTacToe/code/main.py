import pygame
from game import Game

class Main:
    def __init__(self):
        self.game = Game()
        self.screen = pygame.display.set_mode((300, 400))
        pygame.display.set_caption("Tic-Tac-Toe")
        self.clock = pygame.time.Clock()

    def main(self) -> str:
        pygame.init()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.game.play_move((pos[0] // 100, pos[1] // 100)):
                        winner = self.game.check_winner()
                        if winner:
                            self.game.save_result(winner.split()[0], self.game.get_duration())
                            print(winner)  # Feedback to user
            
            self.screen.fill((255, 255, 255))
            self.game.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        return "Game Over"

if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()
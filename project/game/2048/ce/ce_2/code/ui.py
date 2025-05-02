import pygame

class UI:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption('2048 Game')

    def render_board(self, tiles):
        self.screen.fill((255, 255, 255))
        for i in range(4):
            for j in range(4):
                value = tiles[i][j]
                color = (0, 0, 0) if value == 0 else (255, 255, 0)
                pygame.draw.rect(self.screen, color, (j * 100, i * 100, 100, 100))
                if value != 0:
                    font = pygame.font.Font(None, 74)
                    text = font.render(str(value), True, (0, 0, 0))
                    self.screen.blit(text, (j * 100 + 25, i * 100 + 25))
        pygame.display.flip()

    def display_score(self, score):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {score}', True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
        pygame.display.flip()

    def show_game_over(self):
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over', True, (255, 0, 0))
        self.screen.blit(text, (100, 150))
        pygame.display.flip()
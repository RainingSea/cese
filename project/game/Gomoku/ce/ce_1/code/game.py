import pygame
import sys

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def make_move(self, position):
        return position

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(15)] for _ in range(15)]

    def draw(self, screen):
        for x in range(15):
            for y in range(15):
                rect = pygame.Rect(x * 40, y * 40, 40, 40)
                pygame.draw.rect(screen, (255, 204, 0), rect)
                if self.grid[x][y] == 'black':
                    pygame.draw.circle(screen, (0, 0, 0), rect.center, 15)
                elif self.grid[x][y] == 'white':
                    pygame.draw.circle(screen, (255, 255, 255), rect.center, 15)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    def place_piece(self, position, color):
        x, y = position
        if self.grid[x][y] is None:
            self.grid[x][y] = color

class Game:
    def __init__(self):
        self.board = Board()
        self.player1 = Player("Player 1", "black")
        self.player2 = Player("Player 2", "white")
        self.current_player = self.player1
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Gomoku")

    def start_game(self):
        while True:
            self.screen.fill((255, 204, 0))
            self.board.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    position = self.handle_click(pygame.mouse.get_pos())
                    if position:
                        self.board.place_piece(position, self.current_player.color)
                        if self.check_victory():
                            print(f"{self.current_player.name} wins!")
                        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
            pygame.display.flip()

    def handle_click(self, pos):
        x, y = pos
        grid_x = x // 40
        grid_y = y // 40
        if 0 <= grid_x < 15 and 0 <= grid_y < 15:
            return (grid_x, grid_y)
        return None

    def check_victory(self):
        # Victory checking logic goes here (not implemented in this snippet)
        return False
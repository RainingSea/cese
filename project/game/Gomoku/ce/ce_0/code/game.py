import pygame

class Player:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

class Board:
    def __init__(self, size=15):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def draw_board(self, screen):
        for x in range(self.size):
            for y in range(self.size):
                rect = pygame.Rect(x * 40, y * 40, 40, 40)
                pygame.draw.rect(screen, (255, 204, 0), rect, 1)

    def update_board(self, x, y, color):
        self.grid[x][y] = color

class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player("black"), Player("white")]
        self.current_player = 0
        self.winner = None
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Gomoku")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(event.pos)

            self.screen.fill((255, 255, 255))
            self.board.draw_board(self.screen)
            pygame.display.flip()

        pygame.quit()

    def handle_mouse_click(self, pos):
        x, y = pos[0] // 40, pos[1] // 40
        if self.board.grid[x][y] is None:
            color = self.players[self.current_player].get_color()
            self.board.update_board(x, y, color)
            if self.check_victory():
                self.display_winner()
            self.current_player = 1 - self.current_player

    def check_victory(self):
        # Implement victory checking logic here
        return False

    def display_winner(self):
        # Implement winner display logic here
        pass
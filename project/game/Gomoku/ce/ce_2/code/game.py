import pygame

class Player:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

    def make_move(self, x: int, y: int):
        return (x, y)

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(15)] for _ in range(15)]

    def draw(self, screen):
        for x in range(15):
            for y in range(15):
                rect = pygame.Rect(x * 40, y * 40, 40, 40)
                pygame.draw.rect(screen, (255, 204, 153) if self.grid[x][y] is None else self.grid[x][y], rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

    def update_square(self, x: int, y: int, color: str):
        self.grid[x][y] = color

class Game:
    def __init__(self):
        self.board = Board()
        self.player1 = Player("Player1", (0, 0, 0))  # Black
        self.player2 = Player("Player2", (255, 255, 255))  # White
        self.current_player = self.player1
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Gomoku Game")

    def start_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    grid_x, grid_y = x // 40, y // 40
                    self.place_piece(grid_x, grid_y)

            self.screen.fill((255, 204, 153))
            self.board.draw(self.screen)
            pygame.display.flip()

    def check_victory(self):
        # Victory check logic would go here
        pass

    def place_piece(self, x: int, y: int):
        if self.board.grid[x][y] is None:
            self.board.update_square(x, y, self.current_player.color)
            # Check for victory after placing a piece
            if self.check_victory():
                print(f"{self.current_player.name} Wins!")
            # Switch players
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
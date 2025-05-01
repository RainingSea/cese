import pygame

class Player:
    def __init__(self, color: str):
        self.color = color

    def get_color(self) -> str:
        return self.color

class Board:
    def __init__(self, size: int = 15):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def update_board(self, x: int, y: int, color: str) -> bool:
        if 0 <= x < self.size and 0 <= y < self.size and self.grid[x][y] is None:
            self.grid[x][y] = color
            return True
        return False

    def draw(self, screen):
        for x in range(self.size):
            for y in range(self.size):
                rect = pygame.Rect(x * 40, y * 40, 40, 40)
                pygame.draw.rect(screen, color=(255, 204, 0), rect=rect, width=1)

class Game:
    def __init__(self):
        self.board = Board()
        self.player1 = Player("black")
        self.player2 = Player("white")
        self.current_player = 0  # 0 for player1, 1 for player2
        self.players = [self.player1, self.player2]
        self.winner = None
        self.load_game_state()

    def start_game(self):
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Game")
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)

            screen.fill((0, 0, 0))
            self.board.draw(screen)
            if self.winner:
                self.display_winner(screen)
            pygame.display.flip()

    def handle_mouse_click(self, pos):
        if self.winner:  # Prevent further moves after victory
            return

        x = pos[0] // 40
        y = pos[1] // 40
        if self.validate_input_for_piece_placement(x, y):
            color = self.players[self.current_player].get_color()
            if self.board.update_board(x, y, color):
                self.record_move(color, x, y)
                if self.check_victory(x, y):
                    self.winner = color
                self.current_player = 1 - self.current_player

    def validate_input_for_piece_placement(self, x: int, y: int) -> bool:
        return 0 <= x < self.board.size and 0 <= y < self.board.size and self.board.grid[x][y] is None

    def check_victory(self, x: int, y: int) -> bool:
        color = self.board.grid[x][y]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # horizontal, vertical, diagonal right, diagonal left

        for dx, dy in directions:
            count = 1
            count += self.count_consecutive(x, y, dx, dy, color)
            count += self.count_consecutive(x, y, -dx, -dy, color)
            if count >= 5:
                return True
        return False

    def count_consecutive(self, x: int, y: int, dx: int, dy: int, color: str) -> int:
        count = 0
        while 0 <= x < self.board.size and 0 <= y < self.board.size and self.board.grid[x][y] == color:
            count += 1
            x += dx
            y += dy
        return count

    def display_winner(self, screen):
        font = pygame.font.Font(None, 74)
        text = font.render(f"{self.winner} wins!", True, (255, 255, 255))
        screen.blit(text, (150, 250))

    def reset_game(self):
        self.board = Board()
        self.current_player = 0
        self.winner = None

    def record_move(self, player_color: str, move_x: int, move_y: int):
        with open('game_history.txt', 'a') as f:
            f.write(f"{player_color}|{move_x}|{move_y}|{self.winner if self.winner else 'None'}\n")

    def load_game_state(self):
        try:
            with open('game_history.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    color, x, y, winner = line.strip().split('|')
                    x, y = int(x), int(y)
                    self.board.update_board(x, y, color)
                    if winner != 'None':
                        self.winner = winner
                        self.current_player = 1 if color == self.player1.get_color() else 0
        except FileNotFoundError:
            pass

    def save_game_state(self):
        with open('scores.txt', 'w') as f:
            for x in range(self.board.size):
                for y in range(self.board.size):
                    color = self.board.grid[x][y]
                    if color is not None:
                        f.write(f"{x}|{y}|{color}\n")
            f.write(f"Winner: {self.winner if self.winner else 'None'}\n")
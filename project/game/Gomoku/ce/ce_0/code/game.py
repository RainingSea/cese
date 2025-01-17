import pygame
import json

class Game:
    def __init__(self) -> None:
        self.board = [['' for _ in range(15)] for _ in range(15)]
        self.current_player = 'black'
        self.winner = None

    def draw_board(self) -> None:
        for x in range(15):
            for y in range(15):
                rect = pygame.Rect(x * 40, y * 40, 40, 40)
                pygame.draw.rect(screen, (255, 204, 153), rect)
                if self.board[x][y] == 'black':
                    pygame.draw.circle(screen, (0, 0, 0), rect.center, 15)
                elif self.board[x][y] == 'white':
                    pygame.draw.circle(screen, (255, 255, 255), rect.center, 15)

    def place_piece(self, x: int, y: int) -> bool:
        if self.board[x][y] == '' and self.winner is None:
            self.board[x][y] = self.current_player
            self.check_victory()
            self.current_player = 'white' if self.current_player == 'black' else 'black'
            return True
        return False

    def check_victory(self) -> bool:
        # Check rows, columns and diagonals for a win
        for x in range(15):
            for y in range(15):
                if self.board[x][y] != '':
                    if self.check_direction(x, y, 1, 0) or self.check_direction(x, y, 0, 1) or \
                       self.check_direction(x, y, 1, 1) or self.check_direction(x, y, 1, -1):
                        self.winner = self.board[x][y]
                        return True
        return False

    def check_direction(self, x: int, y: int, dx: int, dy: int) -> bool:
        count = 0
        player = self.board[x][y]
        for i in range(5):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < 15 and 0 <= ny < 15 and self.board[nx][ny] == player:
                count += 1
            else:
                break
        return count == 5

    def save_game(self) -> None:
        game_data = {
            'board': self.board,
            'current_player': self.current_player,
            'winner': self.winner
        }
        with open('game_data.txt', 'w') as f:
            json.dump(game_data, f)

    def load_game(self) -> None:
        try:
            with open('game_data.txt', 'r') as f:
                game_data = json.load(f)
                self.board = game_data['board']
                self.current_player = game_data['current_player']
                self.winner = game_data['winner']
        except FileNotFoundError:
            pass
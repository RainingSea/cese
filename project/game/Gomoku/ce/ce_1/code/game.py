import pygame
import json

class Game:
    def __init__(self):
        self.board = [[None for _ in range(15)] for _ in range(15)]
        self.current_player = 'Black'
        self.winner = None
        self.players = {
            'Black': Player('Player 1', 'black'),
            'White': Player('Player 2', 'white')
        }
        self.load_game_state()

    def draw_board(self, screen):
        screen.fill((255, 204, 0))  # Orange yellow background
        for row in range(15):
            for col in range(15):
                if self.board[row][col] is not None:
                    color = self.players[self.board[row][col]].color
                    pygame.draw.circle(screen, color, (col * 40 + 20, row * 40 + 20), 15)
                pygame.draw.rect(screen, (0, 0, 0), (col * 40, row * 40, 40, 40), 1)

    def place_piece(self, x: int, y: int) -> bool:
        row, col = y // 40, x // 40
        if self.board[row][col] is None:
            self.board[row][col] = self.current_player
            if self.check_victory():
                self.winner = self.current_player
                self.save_game_state()
            self.current_player = 'White' if self.current_player == 'Black' else 'Black'
            self.save_game_state()
            return True
        return False

    def check_victory(self) -> bool:
        # Check horizontal, vertical, and diagonal for victory
        for row in range(15):
            for col in range(15):
                if self.board[row][col] is not None:
                    if self.check_direction(row, col, 1, 0) or \
                       self.check_direction(row, col, 0, 1) or \
                       self.check_direction(row, col, 1, 1) or \
                       self.check_direction(row, col, 1, -1):
                        return True
        return False

    def check_direction(self, row: int, col: int, delta_row: int, delta_col: int) -> bool:
        color = self.board[row][col]
        count = 1
        for step in range(1, 5):
            r, c = row + step * delta_row, col + step * delta_col
            if 0 <= r < 15 and 0 <= c < 15 and self.board[r][c] == color:
                count += 1
            else:
                break
        return count >= 5

    def save_game_state(self):
        with open('game_data.txt', 'w') as f:
            json.dump({
                'board': self.board,
                'current_player': self.current_player,
                'winner': self.winner
            }, f)

    def load_game_state(self):
        try:
            with open('game_data.txt', 'r') as f:
                data = json.load(f)
                self.board = data['board']
                self.current_player = data['current_player']
                self.winner = data['winner']
        except FileNotFoundError:
            pass
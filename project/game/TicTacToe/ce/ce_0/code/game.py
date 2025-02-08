import time

class Game:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_turn = 'X'
        self.timer = 0.0

    def play_move(self, row: int, col: int) -> bool:
        if self.board[row][col] == '':
            self.board[row][col] = self.current_turn
            self.current_turn = 'O' if self.current_turn == 'X' else 'X'
            return True
        return False

    def check_winner(self) -> str:
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != '':
                return row[0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != '':
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '':
            return self.board[0][2]
        if all(cell != '' for row in self.board for cell in row):
            return 'Draw'
        return ''

    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_turn = 'X'
        self.timer = 0.0

    def start_timer(self):
        self.timer = time.time()

    def stop_timer(self):
        self.timer = time.time() - self.timer
import random

class Game:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.timer = 0.0

    def play_move(self, row: int, col: int) -> str:
        if self.board[row][col] == '':
            self.board[row][col] = self.current_player
            winner = self.check_winner()
            if winner:
                self.restart()
                return f"{winner} wins!"
            if self.is_draw():
                self.restart()
                return "It's a draw!"
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        return "Move played."

    def check_winner(self) -> str:
        # Check rows, columns and diagonals for a winner
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        return None

    def is_draw(self) -> bool:
        return all(cell != '' for row in self.board for cell in row)

    def restart(self) -> None:
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def start_timer(self) -> None:
        self.timer = random.uniform(1.0, 5.0)  # Simulating a timer for the sake of example

    def stop_timer(self) -> float:
        return self.timer
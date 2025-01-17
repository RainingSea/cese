import time

class Game:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.timer = 0

    def play_move(self, row: int, col: int) -> bool:
        if self.board[row][col] == ' ' and not self.game_over:
            self.board[row][col] = self.current_player
            if self.check_winner():
                self.game_over = True
                self.save_results(f'Player {self.current_player} wins!')
            elif all(cell != ' ' for row in self.board for cell in row):
                self.game_over = True
                self.save_results('Draw!')
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self) -> str:
        for row in self.board:
            if row.count(row[0]) == 3 and row[0] != ' ':
                return row[0]
        for col in range(3):
            if all(self.board[row][col] == self.board[0][col] and self.board[0][col] != ' ' for row in range(3)):
                return self.board[0][col]
        if all(self.board[i][i] == self.board[0][0] and self.board[0][0] != ' ' for i in range(3)):
            return self.board[0][0]
        if all(self.board[i][2 - i] == self.board[0][2] and self.board[0][2] != ' ' for i in range(3)):
            return self.board[0][2]
        return ''

    def restart_game(self):
        self.__init__()

    def start_timer(self):
        self.timer = time.time()

    def stop_timer(self):
        return time.time() - self.timer

    def save_results(self, result: str):
        with open('game_results.txt', 'a') as results_file:
            results_file.write(result + '\n')
        with open('game_time.txt', 'a') as time_file:
            time_file.write(f'Time: {self.stop_timer()} seconds\n')
import time

class Game:
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.winner = None
        self.is_draw = False
        self.start_time = time.time()
        self.end_time = None

    def play_move(self, row: int, col: int) -> None:
        if self.board[row][col] == "" and self.winner is None:
            self.board[row][col] = self.current_player
            self.check_winner()
            self.check_draw()
            self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self) -> None:
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != "":
                self.winner = self.board[row][0]
                self.end_time = time.time()
                return
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                self.winner = self.board[0][col]
                self.end_time = time.time()
                return
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            self.winner = self.board[0][0]
            self.end_time = time.time()
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            self.winner = self.board[0][2]
            self.end_time = time.time()
            return

    def check_draw(self) -> None:
        if all(cell != "" for row in self.board for cell in row) and self.winner is None:
            self.is_draw = True
            self.end_time = time.time()

    def restart_game(self) -> None:
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.winner = None
        self.is_draw = False
        self.start_time = time.time()
        self.end_time = None

    def save_result(self) -> None:
        duration = self.get_duration()
        result = f"Winner: {self.winner if self.winner else 'Draw'}, Duration: {duration:.2f} seconds\n"
        with open("game_results.txt", "a") as file:
            file.write(result)

    def get_duration(self) -> float:
        if self.end_time is not None:
            return self.end_time - self.start_time
        return 0.0
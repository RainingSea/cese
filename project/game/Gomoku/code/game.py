import json

class Game:
    def __init__(self):
        self.board = [['' for _ in range(15)] for _ in range(15)]
        self.current_turn = 'black'
        self.winner = None

    def draw_board(self) -> None:
        # Placeholder for drawing the board using Pygame
        pass

    def place_piece(self, x: int, y: int) -> bool:
        if self.board[x][y] == '' and self.winner is None:
            self.board[x][y] = self.current_turn
            if self.check_victory():
                self.winner = self.current_turn
                self.display_winner()
            self.current_turn = 'white' if self.current_turn == 'black' else 'black'
            return True
        return False

    def check_victory(self) -> bool:
        for x in range(15):
            for y in range(15):
                if self.board[x][y] != '':
                    if self.check_line(x, y, 1, 0) or self.check_line(x, y, 0, 1) or \
                       self.check_line(x, y, 1, 1) or self.check_line(x, y, 1, -1):
                        return True
        return False

    def check_line(self, x: int, y: int, dx: int, dy: int) -> bool:
        piece = self.board[x][y]
        count = 1
        for step in range(1, 5):
            nx, ny = x + dx * step, y + dy * step
            if 0 <= nx < 15 and 0 <= ny < 15 and self.board[nx][ny] == piece:
                count += 1
            else:
                break
        return count >= 5

    def restart_game(self) -> None:
        self.__init__()

    def save_game_state(self) -> None:
        game_state = {
            'board': self.board,
            'current_turn': self.current_turn,
            'winner': self.winner
        }
        with open('game_state.json', 'w') as f:
            json.dump(game_state, f)

    def load_game_state(self) -> None:
        try:
            with open('game_state.json', 'r') as f:
                game_state = json.load(f)
                self.board = game_state['board']
                self.current_turn = game_state['current_turn']
                self.winner = game_state['winner']
        except FileNotFoundError:
            self.restart_game()

    def display_winner(self) -> None:
        print(f"The winner is: {self.winner}")

    def save_results(self) -> None:
        if self.winner:
            with open('game_history.txt', 'a') as f:
                f.write(f"Game {self.get_game_count()}: {self.winner} wins\n")

    def get_game_count(self) -> int:
        try:
            with open('game_history.txt', 'r') as f:
                return len(f.readlines()) + 1
        except FileNotFoundError:
            return 1
import os

class Game:
    def __init__(self):
        self.board = []
        self.player_position = (0, 0)

    def load_game_state(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            return
        
        with open(file_path, 'r') as file:
            self.board = [list(line.strip()) for line in file.readlines()]
            for y, row in enumerate(self.board):
                for x, cell in enumerate(row):
                    if cell == 'P':
                        self.player_position = (x, y)

    def save_game_state(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            for row in self.board:
                file.write(''.join(row) + '\n')

    def move_player(self, direction: str) -> None:
        x, y = self.player_position
        if direction == 'up' and y > 0:
            new_position = (x, y - 1)
        elif direction == 'down' and y < len(self.board) - 1:
            new_position = (x, y + 1)
        elif direction == 'left' and x > 0:
            new_position = (x - 1, y)
        elif direction == 'right' and x < len(self.board[0]) - 1:
            new_position = (x + 1, y)
        else:
            return
        
        if self.board[new_position[1]][new_position[0]] != '#':
            self.board[y][x] = ' '  # Clear old position
            self.board[new_position[1]][new_position[0]] = 'P'  # Update new position
            self.player_position = new_position

    def render(self) -> None:
        for row in self.board:
            print(''.join(row))
        print(f"Player position: {self.player_position}")
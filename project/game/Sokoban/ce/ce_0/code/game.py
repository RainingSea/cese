import pygame

class Game:
    def __init__(self):
        self.board = []
        self.player_position = (0, 0)
        self.goals = []

    def load_level(self, level: str) -> None:
        # Load level data from a text file
        with open(level, 'r') as file:
            lines = file.readlines()
            self.board = [list(line.strip()) for line in lines]
            for y, row in enumerate(self.board):
                for x, cell in enumerate(row):
                    if cell == 'P':
                        self.player_position = (x, y)
                    elif cell == 'G':
                        self.goals.append((x, y))

    def move_player(self, direction: str) -> bool:
        x, y = self.player_position
        if direction == 'UP':
            new_position = (x, y - 1)
        elif direction == 'DOWN':
            new_position = (x, y + 1)
        elif direction == 'LEFT':
            new_position = (x - 1, y)
        elif direction == 'RIGHT':
            new_position = (x + 1, y)
        else:
            return False

        if self.is_move_valid(new_position):
            self.player_position = new_position
            return True
        return False

    def is_move_valid(self, new_position: tuple) -> bool:
        x, y = new_position
        if 0 <= x < len(self.board[0]) and 0 <= y < len(self.board):
            return self.board[y][x] != '#'
        return False

    def save_game_state(self) -> None:
        with open('game_state.txt', 'w') as file:
            file.write(f'player_position|{self.player_position[0]}|{self.player_position[1]}\n')
            file.write(f'board|{"|".join("".join(row) for row in self.board)}\n')

    def load_game_state(self) -> None:
        with open('game_state.txt', 'r') as file:
            for line in file:
                key, *values = line.strip().split('|')
                if key == 'player_position':
                    self.player_position = (int(values[0]), int(values[1]))
                elif key == 'board':
                    self.board = [list(value) for value in values]
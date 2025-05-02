import pygame
import random

class Game:
    def __init__(self):
        pygame.font.init()  # Ensure pygame font is initialized
        self.board = self.initialize_board()
        self.score = 0

    def initialize_board(self):
        board = [[0] * 4 for _ in range(4)]
        self.generate_tile(board)
        self.generate_tile(board)
        return board

    def start_game(self):
        pass  # Initialization already handled in __init__

    def move(self, direction: str):
        if direction == "up":
            self.move_up()
        elif direction == "down":
            self.move_down()
        elif direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        self.generate_tile(self.board)

    def generate_tile(self, board):
        empty_cells = [(r, c) for r in range(4) for c in range(4) if board[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            board[r][c] = random.choice([2, 4])

    def save_game(self):
        with open("game_state.txt", "w") as f:
            for row in self.board:
                f.write("|".join(map(str, row)) + "\n")
            f.write(str(self.score) + "\n")

    def load_game(self):
        with open("game_state.txt", "r") as f:
            lines = f.readlines()
            for i in range(4):
                self.board[i] = list(map(int, lines[i].strip().split("|")))
            self.score = int(lines[4].strip())

    def check_game_over(self):
        if all(self.board[r][c] != 0 for r in range(4) for c in range(4)):
            for r in range(4):
                for c in range(4):
                    if (r < 3 and self.board[r][c] == self.board[r + 1][c]) or \
                       (c < 3 and self.board[r][c] == self.board[r][c + 1]):
                        return
            print("Game Over!")

    def move_up(self):
        for c in range(4):
            stack = []
            for r in range(4):
                if self.board[r][c] != 0:
                    stack.append(self.board[r][c])
            new_row = self.merge_tiles(stack)
            for r in range(4):
                self.board[r][c] = new_row[r]

    def move_down(self):
        for c in range(4):
            stack = []
            for r in range(3, -1, -1):
                if self.board[r][c] != 0:
                    stack.append(self.board[r][c])
            new_row = self.merge_tiles(stack)
            for r in range(4):
                self.board[3 - r][c] = new_row[r]

    def move_left(self):
        for r in range(4):
            stack = []
            for c in range(4):
                if self.board[r][c] != 0:
                    stack.append(self.board[r][c])
            new_row = self.merge_tiles(stack)
            self.board[r] = new_row

    def move_right(self):
        for r in range(4):
            stack = []
            for c in range(3, -1, -1):
                if self.board[r][c] != 0:
                    stack.append(self.board[r][c])
            new_row = self.merge_tiles(stack)
            self.board[r] = new_row[::-1]

    def merge_tiles(self, stack):
        new_row = []
        while stack:
            if len(stack) > 1 and stack[0] == stack[1]:
                new_row.append(stack.pop(0) * 2)
                stack.pop(0)
            else:
                new_row.append(stack.pop(0))
        new_row += [0] * (4 - len(new_row))
        return new_row
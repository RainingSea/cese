import random

class Game:
    def __init__(self):
        self.board = []
        self.score = 0

    def initialize_board(self):
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        self.generate_tile()
        self.generate_tile()

    def generate_tile(self):
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = random.choice([2, 4])

    def move(self, direction: str):
        if direction == "up":
            self.move_up()
        elif direction == "down":
            self.move_down()
        elif direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        self.generate_tile()
        if self.check_game_over():
            print("Game Over")

    def move_up(self):
        for j in range(4):
            stack = []
            for i in range(4):
                if self.board[i][j] != 0:
                    stack.append(self.board[i][j])
            self.merge(stack)
            for i in range(4):
                self.board[i][j] = stack[i] if i < len(stack) else 0

    def move_down(self):
        for j in range(4):
            stack = []
            for i in range(3, -1, -1):
                if self.board[i][j] != 0:
                    stack.append(self.board[i][j])
            self.merge(stack)
            for i in range(4):
                self.board[3 - i][j] = stack[i] if i < len(stack) else 0

    def move_left(self):
        for i in range(4):
            stack = []
            for j in range(4):
                if self.board[i][j] != 0:
                    stack.append(self.board[i][j])
            self.merge(stack)
            for j in range(4):
                self.board[i][j] = stack[j] if j < len(stack) else 0

    def move_right(self):
        for i in range(4):
            stack = []
            for j in range(3, -1, -1):
                if self.board[i][j] != 0:
                    stack.append(self.board[i][j])
            self.merge(stack)
            for j in range(4):
                self.board[i][3 - j] = stack[j] if j < len(stack) else 0

    def merge(self, stack):
        merged = []
        skip = False
        for i in range(len(stack)):
            if skip:
                skip = False
                continue
            if i + 1 < len(stack) and stack[i] == stack[i + 1]:
                merged.append(stack[i] * 2)
                self.score += stack[i] * 2
                skip = True
            else:
                merged.append(stack[i])
        return merged

    def check_game_over(self):
        if any(0 in row for row in self.board):
            return False
        for i in range(4):
            for j in range(4):
                if (i < 3 and self.board[i][j] == self.board[i + 1][j]) or (j < 3 and self.board[i][j] == self.board[i][j + 1]):
                    return False
        return True

    def save_game_state(self, filename: str):
        with open(filename, 'w') as f:
            f.write(f"{self.score}\n")
            for row in self.board:
                f.write(','.join(map(str, row)) + '\n')

    def load_game_state(self, filename: str):
        with open(filename, 'r') as f:
            self.score = int(f.readline().strip())
            self.board = [list(map(int, line.strip().split(','))) for line in f.readlines()]

    def draw(self, screen):
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                color = (200, 200, 200) if value == 0 else (255, 215, 0)
                pygame.draw.rect(screen, color, (j * 100, i * 100 + 50, 100, 100))
                if value != 0:
                    font = pygame.font.Font(None, 74)
                    text = font.render(str(value), True, (0, 0, 0))
                    screen.blit(text, (j * 100 + 30, i * 100 + 50))
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
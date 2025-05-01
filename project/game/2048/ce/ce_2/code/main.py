import pygame
import random
import os

class Game:
    def __init__(self):
        self.board = []
        self.score = 0
        self.initialize_game()

    def initialize_game(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.generate_tile()
        self.generate_tile()

    def move(self, direction: str):
        if direction == 'up':
            self.move_up()
        elif direction == 'down':
            self.move_down()
        elif direction == 'left':
            self.move_left()
        elif direction == 'right':
            self.move_right()
        self.generate_tile()

    def generate_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = random.choice([2, 4])

    def check_game_over(self) -> bool:
        if any(0 in row for row in self.board):
            return False
        for i in range(4):
            for j in range(4):
                if (i < 3 and self.board[i][j] == self.board[i + 1][j]) or (j < 3 and self.board[i][j] == self.board[i][j + 1]):
                    return False
        return True

    def save_game_state(self, filename: str):
        with open(filename, 'w') as f:
            for row in self.board:
                f.write(','.join(map(str, row)) + '\n')
            f.write(str(self.score) + '\n')

    def load_game_state(self, filename: str):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                lines = f.readlines()
                self.board = [list(map(int, line.strip().split(','))) for line in lines[:-1]]
                self.score = int(lines[-1].strip())

    def move_up(self):
        # Logic for moving tiles up
        for j in range(4):
            temp = [self.board[i][j] for i in range(4) if self.board[i][j] != 0]
            merged = []
            skip = False
            for i in range(len(temp)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(temp) and temp[i] == temp[i + 1]:
                    merged.append(temp[i] * 2)
                    self.score += temp[i] * 2
                    skip = True
                else:
                    merged.append(temp[i])
            merged += [0] * (4 - len(merged))
            for i in range(4):
                self.board[i][j] = merged[i]

    def move_down(self):
        # Logic for moving tiles down
        for j in range(4):
            temp = [self.board[i][j] for i in range(3, -1, -1) if self.board[i][j] != 0]
            merged = []
            skip = False
            for i in range(len(temp)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(temp) and temp[i] == temp[i + 1]:
                    merged.append(temp[i] * 2)
                    self.score += temp[i] * 2
                    skip = True
                else:
                    merged.append(temp[i])
            merged += [0] * (4 - len(merged))
            for i in range(4):
                self.board[3 - i][j] = merged[i]

    def move_left(self):
        # Logic for moving tiles left
        for i in range(4):
            temp = [self.board[i][j] for j in range(4) if self.board[i][j] != 0]
            merged = []
            skip = False
            for j in range(len(temp)):
                if skip:
                    skip = False
                    continue
                if j + 1 < len(temp) and temp[j] == temp[j + 1]:
                    merged.append(temp[j] * 2)
                    self.score += temp[j] * 2
                    skip = True
                else:
                    merged.append(temp[j])
            merged += [0] * (4 - len(merged))
            for j in range(4):
                self.board[i][j] = merged[j]

    def move_right(self):
        # Logic for moving tiles right
        for i in range(4):
            temp = [self.board[i][j] for j in range(3, -1, -1) if self.board[i][j] != 0]
            merged = []
            skip = False
            for j in range(len(temp)):
                if skip:
                    skip = False
                    continue
                if j + 1 < len(temp) and temp[j] == temp[j + 1]:
                    merged.append(temp[j] * 2)
                    self.score += temp[j] * 2
                    skip = True
                else:
                    merged.append(temp[j])
            merged += [0] * (4 - len(merged))
            for j in range(4):
                self.board[i][3 - j] = merged[j]

class UI:
    def __init__(self, game):
        self.game = game
        pygame.init()
        self.screen = pygame.display.set_mode((400, 500))
        pygame.display.set_caption('2048 Game')
        self.font = pygame.font.Font(None, 36)

    def draw_board(self):
        self.screen.fill((187, 173, 160))
        for i in range(4):
            for j in range(4):
                value = self.game.board[i][j]
                color = (204, 192, 179) if value == 0 else (238, 228, 218)
                pygame.draw.rect(self.screen, color, (j * 100 + 5, i * 100 + 5, 90, 90))
                if value != 0:
                    text = self.font.render(str(value), True, (0, 0, 0))
                    self.screen.blit(text, (j * 100 + 35, i * 100 + 35))

    def draw_score(self):
        score_text = self.font.render(f'Score: {self.game.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 410))

    def show_game_over(self):
        game_over_text = self.font.render('Game Over', True, (255, 0, 0))
        self.screen.blit(game_over_text, (150, 230))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.game.move('up')
            elif event.key == pygame.K_DOWN:
                self.game.move('down')
            elif event.key == pygame.K_LEFT:
                self.game.move('left')
            elif event.key == pygame.K_RIGHT:
                self.game.move('right')

def main():
    game = Game()
    ui = UI(game)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui.handle_input(event)

        ui.draw_board()
        ui.draw_score()
        if game.check_game_over():
            ui.show_game_over()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()
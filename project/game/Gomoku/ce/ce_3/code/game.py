import pygame
import json

class Game:
    def __init__(self):
        self.board = [['' for _ in range(15)] for _ in range(15)]
        self.current_turn = 'black'
        self.load_game_state()

    def draw_board(self):
        screen = pygame.display.set_mode((600, 600))
        screen.fill((255, 204, 0))  # Orange yellow background
        for x in range(15):
            pygame.draw.line(screen, (0, 0, 0), (x * 40, 0), (x * 40, 600))  # Vertical lines
            pygame.draw.line(screen, (0, 0, 0), (0, x * 40), (600, x * 40))  # Horizontal lines
        for x in range(15):
            for y in range(15):
                if self.board[x][y] == 'black':
                    pygame.draw.circle(screen, (0, 0, 0), (x * 40 + 20, y * 40 + 20), 15)
                elif self.board[x][y] == 'white':
                    pygame.draw.circle(screen, (255, 255, 255), (x * 40 + 20, y * 40 + 20), 15)
        pygame.display.flip()

    def place_piece(self, x: int, y: int) -> bool:
        if self.board[x][y] == '':
            self.board[x][y] = self.current_turn
            self.current_turn = 'white' if self.current_turn == 'black' else 'black'
            self.save_game_state()
            return True
        return False

    def check_victory(self) -> bool:
        # Check rows, columns and diagonals for victory
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

    def save_game_state(self) -> None:
        with open('game_state.txt', 'w') as f:
            json.dump({'board': self.board, 'current_turn': self.current_turn}, f)

    def load_game_state(self) -> None:
        try:
            with open('game_state.txt', 'r') as f:
                state = json.load(f)
                self.board = state['board']
                self.current_turn = state['current_turn']
        except FileNotFoundError:
            self.save_game_state()  # Create a new game state if file does not exist
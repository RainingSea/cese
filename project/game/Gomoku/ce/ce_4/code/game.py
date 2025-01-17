import pygame
import sys

class Game:
    def __init__(self):
        self.board = [['' for _ in range(15)] for _ in range(15)]
        self.current_player = 'Black'
        self.winner = None
        self.width = 600
        self.height = 600
        self.cell_size = self.width // 15

    def draw_board(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Gomoku Game")
        screen.fill((255, 204, 0))  # Orange yellow background

        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(screen, (0, 0, 0), (0, y), (self.width, y))

        for y in range(15):
            for x in range(15):
                if self.board[y][x] == 'Black':
                    pygame.draw.circle(screen, (0, 0, 0), (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2), self.cell_size // 3)
                elif self.board[y][x] == 'White':
                    pygame.draw.circle(screen, (255, 255, 255), (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2), self.cell_size // 3)

        pygame.display.flip()

    def place_piece(self, x: int, y: int) -> bool:
        if self.board[y][x] == '':
            self.board[y][x] = self.current_player
            return True
        return False

    def check_victory(self) -> bool:
        # Check rows, columns, and diagonals for a winner
        for y in range(15):
            for x in range(15):
                if self.board[y][x] == '':
                    continue
                if self.check_direction(x, y, 1, 0) or self.check_direction(x, y, 0, 1) or self.check_direction(x, y, 1, 1) or self.check_direction(x, y, 1, -1):
                    self.winner = self.current_player
                    return True
        return False

    def check_direction(self, x: int, y: int, dx: int, dy: int) -> bool:
        count = 0
        for i in range(5):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < 15 and 0 <= ny < 15 and self.board[ny][nx] == self.current_player:
                count += 1
            else:
                break
        return count == 5

    def switch_player(self) -> None:
        self.current_player = 'White' if self.current_player == 'Black' else 'Black'

    def display_winner(self) -> None:
        print(f"The winner is: {self.winner}")

    def save_results(self) -> None:
        with open('game_results.txt', 'a') as f:
            f.write(f"{self.winner}\n")
import pygame
import json

class Player:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

class Game:
    def __init__(self):
        self.board = [['' for _ in range(15)] for _ in range(15)]
        self.current_turn = 'black'
        self.winner = None

    def draw_board(self, screen):
        screen.fill((255, 204, 0))  # Orange yellow background
        for x in range(15):
            for y in range(15):
                if self.board[x][y] == 'black':
                    pygame.draw.circle(screen, (0, 0, 0), (x * 40 + 20, y * 40 + 20), 15)
                elif self.board[x][y] == 'white':
                    pygame.draw.circle(screen, (255, 255, 255), (x * 40 + 20, y * 40 + 20), 15)
                pygame.draw.rect(screen, (0, 0, 0), (x * 40, y * 40, 40, 40), 1)

    def place_piece(self, x: int, y: int) -> bool:
        if self.board[x][y] == '':
            self.board[x][y] = self.current_turn
            self.current_turn = 'white' if self.current_turn == 'black' else 'black'
            return True
        return False

    def check_victory(self) -> bool:
        # Check horizontal, vertical, and diagonal for victory
        for x in range(15):
            for y in range(15):
                if self.board[x][y] != '':
                    if self.check_direction(x, y, 1, 0) or self.check_direction(x, y, 0, 1) or \
                       self.check_direction(x, y, 1, 1) or self.check_direction(x, y, 1, -1):
                        self.winner = self.board[x][y]
                        return True
        return False

    def check_direction(self, x: int, y: int, dx: int, dy: int) -> bool:
        count = 0
        player_color = self.board[x][y]
        for i in range(5):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < 15 and 0 <= ny < 15 and self.board[nx][ny] == player_color:
                count += 1
            else:
                break
        return count == 5

    def reset_game(self) -> None:
        self.board = [['' for _ in range(15)] for _ in range(15)]
        self.current_turn = 'black'
        self.winner = None

    def save_game_state(self) -> None:
        with open('game_state.txt', 'w') as f:
            json.dump({'board': self.board, 'current_turn': self.current_turn, 'winner': self.winner}, f)

    def load_game_state(self) -> None:
        try:
            with open('game_state.txt', 'r') as f:
                state = json.load(f)
                self.board = state['board']
                self.current_turn = state['current_turn']
                self.winner = state['winner']
        except FileNotFoundError:
            self.reset_game()

    def display_winner(self, screen):
        if self.winner:
            font = pygame.font.Font(None, 74)
            text = font.render(f'{self.winner} wins!', True, (0, 0, 0))
            screen.blit(text, (150, 150))
import random
import pygame

class Score:
    def __init__(self) -> None:
        """Initialize the score to zero."""
        self.current_score = 0

    def update_score(self, points: int) -> None:
        """Update the score by adding points."""
        self.current_score += points

    def get_score(self) -> int:
        """Return the current score."""
        return self.current_score

class GameBoard:
    def __init__(self) -> None:
        """Initialize the game board with empty tiles and score."""
        self.tiles = [[0] * 4 for _ in range(4)]
        self.score = Score()  # Initialize score in GameBoard
        self.initialize_board()

    def initialize_board(self) -> None:
        """Set up the game board with two initial tiles."""
        for _ in range(2):
            self.generate_tile()

    def generate_tile(self) -> None:
        """Generate a new tile (2 or 4) in a random empty position."""
        empty_tiles = [(r, c) for r in range(4) for c in range(4) if self.tiles[r][c] == 0]
        if empty_tiles:
            r, c = random.choice(empty_tiles)
            self.tiles[r][c] = 4 if random.random() < 0.1 else 2

    def move_tiles(self, direction: str) -> None:
        """Move tiles in the specified direction."""
        if direction == 'left':
            self.merge_tiles('left')
        elif direction == 'right':
            self.tiles = [row[::-1] for row in self.tiles]
            self.merge_tiles('left')
            self.tiles = [row[::-1] for row in self.tiles]
        elif direction == 'up':
            self.tiles = list(map(list, zip(*self.tiles)))  # Transpose
            self.merge_tiles('left')
            self.tiles = list(map(list, zip(*self.tiles)))  # Transpose back
        elif direction == 'down':
            self.tiles = list(map(list, zip(*self.tiles)))  # Transpose
            self.tiles = [row[::-1] for row in self.tiles]
            self.merge_tiles('left')
            self.tiles = [row[::-1] for row in self.tiles]  # Transpose back

    def merge_tiles(self, direction: str) -> None:
        """Merge tiles in the specified direction."""
        for i in range(4):
            if direction == 'left':
                self.tiles[i] = self._merge_row(self.tiles[i])
            elif direction == 'up':
                self.tiles[i] = self._merge_row([self.tiles[j][i] for j in range(4)])
            elif direction == 'right':
                self.tiles[i] = self._merge_row(self.tiles[i][::-1])[::-1]
            elif direction == 'down':
                self.tiles[i] = self._merge_row([self.tiles[j][i] for j in range(4)][::-1])[::-1]

    def _merge_row(self, row: list) -> list:
        """Merge a single row of tiles and update the score."""
        new_row = [num for num in row if num != 0]
        merged_row = []
        skip = False
        for j in range(len(new_row)):
            if skip:
                skip = False
                continue
            if j + 1 < len(new_row) and new_row[j] == new_row[j + 1]:
                merged_row.append(new_row[j] * 2)
                self.score.update_score(new_row[j] * 2)  # Update score on merge
                skip = True
            else:
                merged_row.append(new_row[j])
        return merged_row + [0] * (4 - len(merged_row))

    def is_full(self) -> bool:
        """Check if the board is full."""
        return all(self.tiles[r][c] != 0 for r in range(4) for c in range(4))

class Game:
    def __init__(self) -> None:
        """Initialize the game with a new board and score."""
        self.board = GameBoard()

    def start_game(self) -> None:
        """Start the game loop."""
        self.board.initialize_board()  # Initialize the game board

    def move(self, direction: str) -> None:
        """Move the tiles in the specified direction and generate a new tile."""
        self.board.move_tiles(direction)
        if not self.check_game_over():  # Only generate a new tile if the game is not over
            self.board.generate_tile()

    def save_game(self, filename: str) -> None:
        """Save the current game state to a file."""
        with open(filename, 'w') as f:
            for row in self.board.tiles:
                f.write(' '.join(map(str, row)) + '\n')
            f.write(str(self.board.score.get_score()) + '\n')  # Save score correctly

    def load_game(self, filename: str) -> None:
        """Load the game state from a file."""
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.board.tiles = [list(map(int, line.split())) for line in lines[:-1]]
            self.board.score.current_score = int(lines[-1].strip())  # Load score correctly

    def check_game_over(self) -> bool:
        """Check if the game is over."""
        if self.board.is_full() and not any(self._can_merge()):
            print("Game Over!")
            return True
        return False

    def _can_merge(self) -> list:
        """Check if any tiles can be merged."""
        can_merge = []
        for r in range(4):
            for c in range(4):
                if self.board.tiles[r][c] == 0:
                    can_merge.append(True)
                if r < 3 and self.board.tiles[r][c] == self.board.tiles[r + 1][c]:
                    can_merge.append(True)
                if c < 3 and self.board.tiles[r][c] == self.board.tiles[r][c + 1]:
                    can_merge.append(True)
        return can_merge
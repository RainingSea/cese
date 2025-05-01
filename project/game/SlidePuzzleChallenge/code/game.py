import pygame
import random
from progress import Progress
from timer import Timer
from grid import Grid

class Game:
    def __init__(self):
        self.grid = Grid()
        self.timer = Timer()
        self.progress = Progress('progress.txt')
        self.difficulty = self.load_difficulty()

    def load_difficulty(self):
        with open('settings.txt', 'r') as file:
            return file.readline().strip().split('=')[1]

    def start_game(self):
        self.load_progress()
        self.grid.shuffle()
        self.timer.start()
        self.run_game_loop()

    def run_game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_event(event)
            self.display_current_state_of_puzzle()
            pygame.display.flip()

    def handle_key_event(self, event):
        if event.key == pygame.K_UP:
            self.move_tile(0, -1)
        elif event.key == pygame.K_DOWN:
            self.move_tile(0, 1)
        elif event.key == pygame.K_LEFT:
            self.move_tile(-1, 0)
        elif event.key == pygame.K_RIGHT:
            self.move_tile(1, 0)

    def move_tile(self, dx, dy):
        empty_tile = self.grid.find_empty_tile()
        target_x = empty_tile[0] + dy
        target_y = empty_tile[1] + dx
        if self.grid.is_adjacent(empty_tile, (target_x, target_y)):
            self.grid.slide_tile(target_x, target_y)
            self.visual_feedback_on_correct_position(target_x, target_y)
            if self.grid.is_solved():
                print("Congratulations! You've solved the puzzle.")
            if self.confirm_save():
                self.save_progress()

    def visual_feedback_on_correct_position(self, x, y):
        tile = self.grid.tiles[x][y]
        if tile.number == (x * 4 + y + 1) % 16:  # Check if the tile is in the correct position
            print(f"Tile {tile.number} is in the correct position!")

    def confirm_save(self):
        # Placeholder for confirmation logic
        return True  # Assume user confirms for now

    def save_progress(self):
        data = f"grid_state={self.grid.serialize()}\ntimer_value={self.timer.get_elapsed_time()}\ndifficulty={self.difficulty}"
        self.progress.save(data)

    def load_progress(self):
        data = self.progress.load()
        grid_state, timer_value, difficulty = data.split('\n')
        self.difficulty = difficulty.split('=')[1]
        self.grid.load_state(grid_state.split('=')[1])
        self.timer.elapsed_time = int(timer_value.split('=')[1])

    def reset_game(self):
        self.grid.reset()
        self.timer.stop()
        self.timer.start()

    def provide_hint(self):
        return "Hint: Move tile 5 to the right."

    def display_current_state_of_puzzle(self):
        for row in self.grid.tiles:
            for tile in row:
                tile.draw()

class Grid:
    def __init__(self):
        self.tiles = [[Tile(i + j * 4) for i in range(4)] for j in range(4)]
        self.tiles[3][3].is_empty = True  # Last tile is empty

    def shuffle(self):
        flat_tiles = self.flatten_tiles()
        random.shuffle(flat_tiles)
        self.tiles = [flat_tiles[i:i + 4] for i in range(0, len(flat_tiles), 4)]
        self.ensure_solvable()

    def ensure_solvable(self):
        # Check if the shuffled tiles are solvable
        inversions = 0
        flat_tiles = self.flatten_tiles()
        for i in range(len(flat_tiles)):
            for j in range(i + 1, len(flat_tiles)):
                if flat_tiles[i] > flat_tiles[j] and flat_tiles[i] != 0 and flat_tiles[j] != 0:
                    inversions += 1
        if inversions % 2 != 0:
            self.shuffle()  # Reshuffle if not solvable

    def slide_tile(self, x, y):
        empty_tile = self.find_empty_tile()
        if self.is_adjacent(empty_tile, (x, y)):
            self.tiles[empty_tile[0]][empty_tile[1]], self.tiles[x][y] = self.tiles[x][y], self.tiles[empty_tile[0]][empty_tile[1]]

    def is_solved(self):
        return all(tile.number == i for i, tile in enumerate(self.flatten_tiles()))

    def flatten_tiles(self):
        return [tile for row in self.tiles for tile in row]

    def load_state(self, state):
        numbers = list(map(int, state.split('|')))
        for i, number in enumerate(numbers):
            row, col = divmod(i, 4)
            self.tiles[row][col].number = number
            self.tiles[row][col].is_empty = (number == 0)

    def reset(self):
        self.__init__()

    def serialize(self):
        return '|'.join(str(tile.number) for tile in self.flatten_tiles())

    def find_empty_tile(self):
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                if tile.is_empty:
                    return (i, j)
        return None

    def is_adjacent(self, empty_tile, target_tile):
        return (abs(empty_tile[0] - target_tile[0]) == 1 and empty_tile[1] == target_tile[1]) or \
               (empty_tile[0] == target_tile[0] and abs(empty_tile[1] - target_tile[1]) == 1)

class Tile:
    def __init__(self, number):
        self.number = number
        self.is_empty = False

    def draw(self):
        # Logic to render the tile
        # Placeholder for rendering logic
        print(f"Tile {self.number} drawn.")
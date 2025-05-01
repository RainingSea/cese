class Tile:
    def __init__(self, tile_type: str):
        self.tile_type = tile_type

class Maze:
    def __init__(self):
        self.grid = []

    def load_maze(self, file: str) -> None:
        with open(file, 'r') as f:
            for line in f:
                row = [Tile(tile) for tile in line.strip()]
                self.grid.append(row)

    def move_tile(self, direction: str) -> None:
        # Logic to move a tile in the specified direction
        pass

    def check_win(self) -> bool:
        # Logic to check if the player has reached the exit tile
        return False
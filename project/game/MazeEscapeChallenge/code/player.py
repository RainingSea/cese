class Player:
    def __init__(self):
        self.position = (1, 1)  # Starting position

    def move(self, direction: str):
        x, y = self.position
        if direction == "UP":
            new_position = (x, max(0, y - 1))
        elif direction == "DOWN":
            new_position = (x, min(9, y + 1))
        elif direction == "LEFT":
            new_position = (max(0, x - 1), y)
        elif direction == "RIGHT":
            new_position = (min(9, x + 1), y)
        else:
            return  # Invalid direction, do nothing

        # Check if the new position is valid (not a wall)
        if self.is_valid_move(new_position):
            self.position = new_position

    def is_valid_move(self, new_position: tuple) -> bool:
        # Assuming the maze layout is accessible via the Game class
        x, y = new_position
        return self.layout[y][x] == 0  # Check if the new position is not a wall

    def check_exit(self, exit_position: tuple) -> bool:
        return self.position == exit_position
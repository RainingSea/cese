class Player:
    def __init__(self):
        self.position_x = 0  # Initialize player position
        self.position_y = 0
        self.name = ""
        self.completion_time = 0

    def move(self, direction: str, maze):
        if direction == 'up' and self.position_y > 0 and maze.walls[self.position_y - 1][self.position_x] == 0:
            self.position_y -= 1  # Move up
        elif direction == 'down' and self.position_y < maze.size - 1 and maze.walls[self.position_y + 1][self.position_x] == 0:
            self.position_y += 1  # Move down
        elif direction == 'left' and self.position_x > 0 and maze.walls[self.position_y][self.position_x - 1] == 0:
            self.position_x -= 1  # Move left
        elif direction == 'right' and self.position_x < maze.size - 1 and maze.walls[self.position_y][self.position_x + 1] == 0:
            self.position_x += 1  # Move right

    def record_time(self, time: int):
        self.completion_time = time
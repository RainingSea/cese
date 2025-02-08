class Player:
    def __init__(self):
        self.position_x = 0
        self.position_y = 0

    def move(self, direction: str):
        if direction == 'up':
            self.position_y -= 1
        elif direction == 'down':
            self.position_y += 1
        elif direction == 'left':
            self.position_x -= 1
        elif direction == 'right':
            self.position_x += 1

    def check_exit(self, maze):
        return maze.pathways[self.position_x][self.position_y] == 1
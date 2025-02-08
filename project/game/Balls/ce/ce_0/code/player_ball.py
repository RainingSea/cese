class PlayerBall:
    def __init__(self, size, position):
        self.size = size
        self.position = position

    def move(self, direction):
        if direction == 'UP':
            self.position = (self.position[0], self.position[1] - 5)
        elif direction == 'DOWN':
            self.position = (self.position[0], self.position[1] + 5)
        elif direction == 'LEFT':
            self.position = (self.position[0] - 5, self.position[1])
        elif direction == 'RIGHT':
            self.position = (self.position[0] + 5, self.position[1])

    def grow(self, amount):
        self.size += amount
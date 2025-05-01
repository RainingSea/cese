class Obstacle:
    def __init__(self, name, position):
        self.name = name
        self.position = position

class Track:
    def __init__(self):
        self.obstacles = []

    def load_track(self, file: str):
        with open(file, 'r') as f:
            for line in f:
                name, position = line.strip().split('|')
                self.obstacles.append(Obstacle(name, position))
class Player:
    def __init__(self, health, x, y):
        self.health = health
        self.x = x
        self.y = y

    def move(self, direction: str):
        if direction == 'up':
            self.y -= 1
        elif direction == 'down':
            self.y += 1
        elif direction == 'left':
            self.x -= 1
        elif direction == 'right':
            self.x += 1

    def fire(self):
        # Logic to fire a bullet
        pass

class Enemy:
    def __init__(self, health, x, y):
        self.health = health
        self.x = x
        self.y = y

    def shoot(self):
        # Logic for enemy shooting
        pass

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
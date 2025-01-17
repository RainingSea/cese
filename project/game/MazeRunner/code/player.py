import pygame

class Player:
    def __init__(self):
        self.position = (1, 1)
        self.score = 0
        self.stars_collected = 0
        self.moves = 0

    def move(self, direction: str = None) -> None:
        if direction:
            x, y = self.position
            if direction == 'UP':
                self.position = (x, y - 1)
            elif direction == 'DOWN':
                self.position = (x, y + 1)
            elif direction == 'LEFT':
                self.position = (x - 1, y)
            elif direction == 'RIGHT':
                self.position = (x + 1, y)
            self.moves += 1

    def collect_star(self) -> bool:
        # Logic to check if a star is collected
        # Placeholder for star collection logic
        # Assuming stars are at specific positions, for example:
        star_positions = [(1, 4), (2, 4), (3, 4), (4, 4)]
        if self.position in star_positions:
            self.stars_collected += 1
            return True
        return False

    def reset(self) -> None:
        self.position = (1, 1)
        self.stars_collected = 0
        self.moves = 0

    def draw(self, screen) -> None:
        # Draw player on the screen
        pygame.draw.rect(screen, (255, 0, 0), (*self.position, 20, 20))
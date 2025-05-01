import pygame

class Player:
    def __init__(self, name: str = "Player"):
        self.position = (0, 0)  # Initialize player's position at (0, 0)
        self.score = 0  # Initialize player's score at 0
        self.name = name  # Player's name

    def move(self, direction: str, maze):
        new_position = self.position
        if direction == "up":
            new_position = (self.position[0], self.position[1] - 1)  # Move up
        elif direction == "down":
            new_position = (self.position[0], self.position[1] + 1)  # Move down
        elif direction == "left":
            new_position = (self.position[0] - 1, self.position[1])   # Move left
        elif direction == "right":
            new_position = (self.position[0] + 1, self.position[1])   # Move right

        if not maze.check_collision(new_position):
            self.position = new_position  # Update position only if no collision

    def collect_star(self):
        self.score += 1  # Increment the player's score by 1 when collecting a star

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (*self.position, 20, 20))  # Draw player
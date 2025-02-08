from typing import List, Tuple

class Track:
    def __init__(self):
        self.path = []

    def load_from_file(self, file_path: str) -> None:
        with open(file_path, "r") as f:
            for line in f:
                attributes = line.strip().split("|")
                self.path.append(tuple(map(int, attributes[1:])))
    
    def draw(self, screen) -> None:
        # Placeholder for drawing track logic
        for point in self.path:
            pygame.draw.circle(screen, (0, 0, 0), point, 5)
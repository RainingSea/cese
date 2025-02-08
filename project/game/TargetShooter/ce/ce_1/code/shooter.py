import pygame

class Shooter:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def aim(self, mouse_x: int, mouse_y: int) -> None:
        self.x = mouse_x
        self.y = mouse_y

    def shoot(self) -> None:
        # Logic for shooting can be implemented here
        pass
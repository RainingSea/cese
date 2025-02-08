class Mario:
    def __init__(self, position: tuple):
        self.position = position
        self.score = 0

    def move_left(self) -> None:
        self.position = (self.position[0] - 1, self.position[1])

    def move_right(self) -> None:
        self.position = (self.position[0] + 1, self.position[1])

    def jump(self) -> None:
        # Logic for jumping (not implemented)
        pass

    def hit_block(self, block: 'Block') -> None:
        mushroom = block.hit()
        if mushroom:
            self.touch_mushroom()

    def touch_mushroom(self) -> None:
        self.score += 1  # Increase score when touching a mushroom

    def touch_enemy(self) -> None:
        self.score -= 1  # Decrease score when touching an enemy

    def reach_flagpole(self) -> None:
        # Logic for reaching the flagpole (not implemented)
        pass
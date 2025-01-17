class EnemyTank:
    def __init__(self, position_x: int, position_y: int):
        self.health = 100
        self.position_x = position_x
        self.position_y = position_y

    def shoot(self) -> None:
        # Logic for enemy shooting would go here
        pass

    def take_damage(self, amount: int) -> None:
        self.health -= amount
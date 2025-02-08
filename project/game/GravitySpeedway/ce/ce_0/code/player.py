from vehicle import Vehicle

class Player:
    def __init__(self, name: str, vehicle_name: str):
        self.name = name
        self.vehicle = Vehicle(vehicle_name, 0.5, 2.0, 150.0)
        self.speed = 0.0

    def move(self, direction: str) -> None:
        if direction == "left":
            # Logic to move left
            pass
        elif direction == "right":
            # Logic to move right
            pass

    def accelerate(self) -> None:
        self.speed += self.vehicle.acceleration

    def brake(self) -> None:
        self.speed -= self.vehicle.acceleration
        if self.speed < 0:
            self.speed = 0
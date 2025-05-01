class HUD:
    def __init__(self):
        self.speed = 0.0
        self.lap_time = 0.0

    def display(self):
        print(f"Speed: {self.speed} km/h")
        print(f"Lap Time: {self.lap_time} seconds")
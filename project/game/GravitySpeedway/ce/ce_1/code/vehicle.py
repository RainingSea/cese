class Vehicle:
    def __init__(self):
        self.name = ""
        self.handling = 0.0
        self.acceleration = 0.0
        self.top_speed = 0.0

    def load_vehicle(self, file: str):
        with open(file, 'r') as f:
            for line in f:
                name, handling, acceleration, top_speed = line.strip().split('|')
                self.name = name
                self.handling = float(handling)
                self.acceleration = float(acceleration)
                self.top_speed = float(top_speed)
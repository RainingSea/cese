class Vehicle:
    def __init__(self, make: str, model: str, year: int, mileage: int):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage

    def save(self):
        with open('vehicles.txt', 'a') as f:
            f.write(f"{self.make}|{self.model}|{self.year}|{self.mileage}\n")

    @staticmethod
    def load_vehicles() -> list:
        try:
            with open('vehicles.txt', 'r') as f:
                return [Vehicle(*line.strip().split('|')) for line in f.readlines()]
        except FileNotFoundError:
            return []
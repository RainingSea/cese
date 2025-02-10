class Vehicle:
    def __init__(self, make: str, model: str, year: int, mileage: int):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage

    def save(self) -> None:
        with open('vehicles.txt', 'a') as f:
            f.write(f"{self.make}|{self.model}|{self.year}|{self.mileage}\n")

    @staticmethod
    def load_all() -> list:
        vehicles = []
        with open('vehicles.txt', 'r') as f:
            for line in f:
                make, model, year, mileage = line.strip().split('|')
                vehicles.append(Vehicle(make, model, int(year), int(mileage)))
        return vehicles
class Vehicle:
    def __init__(self, make: str, model: str, year: int, mileage: int):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage

    def save(self) -> None:
        with open('vehicles.txt', 'a') as file:
            file.write(f"{self.make}|{self.model}|{self.year}|{self.mileage}\n")

    @staticmethod
    def load_vehicles() -> list:
        vehicles = []
        try:
            with open('vehicles.txt', 'r') as file:
                for line in file:
                    make, model, year, mileage = line.strip().split('|')
                    vehicles.append(Vehicle(make, model, int(year), int(mileage)))
        except FileNotFoundError:
            pass
        return vehicles
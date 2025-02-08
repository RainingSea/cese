import os

class DataStorage:
    def save_scores(self, score: int) -> None:
        with open('scores.txt', 'a') as file:
            file.write(f"{score}\n")

    def load_scores(self) -> list:
        if not os.path.exists('scores.txt'):
            return []
        with open('scores.txt', 'r') as file:
            return [int(line.strip()) for line in file.readlines()]

    def load_vehicles(self) -> list:
        vehicles = []
        if not os.path.exists('vehicles.txt'):
            return vehicles
        with open('vehicles.txt', 'r') as file:
            for line in file:
                name, handling, acceleration, top_speed = line.strip().split('|')
                vehicles.append(Vehicle(name, float(handling), float(acceleration), float(top_speed)))
        return vehicles
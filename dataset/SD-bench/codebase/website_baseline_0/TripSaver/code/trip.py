class Trip:
    def __init__(self, starting_point: str, destination: str, travel_date: str):
        self.starting_point = starting_point
        self.destination = destination
        self.travel_date = travel_date

    def save(self) -> None:
        with open('trips.txt', 'a') as f:
            f.write(f"{self.starting_point}|{self.destination}|{self.travel_date}\n")

    def get_suggestions(self) -> list:
        # Placeholder for transportation suggestions
        return [
            {"mode": "Bus", "cost": 20, "time": "2 hours"},
            {"mode": "Train", "cost": 50, "time": "1.5 hours"},
            {"mode": "Car", "cost": 30, "time": "2 hours"}
        ]
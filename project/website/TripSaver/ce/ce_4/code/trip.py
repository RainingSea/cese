class Trip:
    def __init__(self, starting_point: str, destination: str, travel_date: str):
        self.starting_point = starting_point
        self.destination = destination
        self.travel_date = travel_date
        self.options = []

    def save_trip(self):
        with open('trips.txt', 'a') as f:
            f.write(f"{self.starting_point}|{self.destination}|{self.travel_date}\n")

    @staticmethod
    def load_trips() -> list:
        trips = []
        try:
            with open('trips.txt', 'r') as f:
                for line in f:
                    starting_point, destination, travel_date = line.strip().split('|')
                    trips.append(Trip(starting_point, destination, travel_date))
        except FileNotFoundError:
            pass
        return trips
class TripManager:
    def __init__(self):
        self.trips = self.load_trips()

    def load_trips(self):
        trips = []
        try:
            with open('trips.txt', 'r') as file:
                for line in file:
                    trips.append(line.strip().split(','))
        except FileNotFoundError:
            pass
        return trips

    def input_trip(self, username: str, starting_point: str, destination: str, date: str) -> bool:
        trip_entry = f"{username},{starting_point},{destination},{date}\n"
        with open('trips.txt', 'a') as file:
            file.write(trip_entry)
        self.trips.append(trip_entry.strip().split(','))
        return True

    def get_transportation_options(self, starting_point: str, destination: str) -> list:
        # Static data for demonstration purposes
        options = [
            {"option": "Bus", "cost": 10, "time": "30 mins"},
            {"option": "Train", "cost": 20, "time": "15 mins"},
            {"option": "Taxi", "cost": 30, "time": "10 mins"}
        ]
        return options

    def save_preferred_option(self, username: str, option: str) -> bool:
        with open('options.txt', 'a') as file:
            file.write(f"{username},{option}\n")
        return True
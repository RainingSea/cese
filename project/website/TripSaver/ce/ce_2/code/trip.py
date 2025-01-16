class Trip:
    def __init__(self, starting_point: str, destination: str, travel_date: str):
        self.starting_point = starting_point
        self.destination = destination
        self.travel_date = travel_date

    def save(self):
        pass  # Saving is handled in TripSaverApp
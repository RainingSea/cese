class TransportationOption:
    def __init__(self, type: str, cost: float, time: float):
        self.type = type
        self.cost = cost
        self.time = time

    def save(self):
        pass  # Saving is handled in TripSaverApp
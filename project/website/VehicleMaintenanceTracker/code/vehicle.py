class Vehicle:
    """Represents a vehicle in the system."""
    
    def __init__(self, make: str, model: str, year: int, mileage: int):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.vehicle_id = id(self)  # Unique ID for the vehicle
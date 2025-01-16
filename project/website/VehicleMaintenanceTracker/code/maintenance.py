class Maintenance:
    """Represents a maintenance record for a vehicle."""
    
    def __init__(self, vehicle_id: int, task: str, date: str, mileage: int):
        self.vehicle_id = vehicle_id
        self.task = task
        self.date = date
        self.mileage = mileage
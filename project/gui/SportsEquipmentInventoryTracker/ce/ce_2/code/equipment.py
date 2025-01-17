class Equipment:
    def __init__(self, name: str, type: str, quantity: int, condition: str, availability: bool, location: str, maintenance_alert: str):
        self.name = name
        self.type = type
        self.quantity = quantity
        self.condition = condition
        self.availability = availability
        self.location = location
        self.maintenance_alert = maintenance_alert
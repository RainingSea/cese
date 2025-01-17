class Equipment:
    def __init__(self, id: str, name: str, type: str, quantity: int, condition: str, location: str, maintenance_alert: str):
        self.id = id
        self.name = name
        self.type = type
        self.quantity = quantity
        self.condition = condition
        self.location = location
        self.maintenance_alert = maintenance_alert
class Equipment:
    def __init__(self, name: str, type: str, quantity: int, condition: str, availability: bool, location: str, maintenance_alert: str):
        self.name = name
        self.type = type
        self.quantity = quantity
        self.condition = condition
        self.availability = availability
        self.location = location
        self.maintenance_alert = maintenance_alert

    def save(self):
        with open('equipment.txt', 'a') as file:
            file.write(f"{self.name}|{self.type}|{self.quantity}|{self.condition}|{self.availability}|{self.location}|{self.maintenance_alert}\n")

    @staticmethod
    def load_equipment() -> list:
        equipment_list = []
        try:
            with open('equipment.txt', 'r') as file:
                for line in file:
                    name, type_, quantity, condition, availability, location, maintenance_alert = line.strip().split('|')
                    equipment = Equipment(name, type_, int(quantity), condition, availability == 'True', location, maintenance_alert)
                    equipment_list.append(equipment)
        except FileNotFoundError:
            pass
        return equipment_list
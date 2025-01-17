class EquipmentManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.equipment = self.load_equipment()
        self.alerts = self.load_alerts()

    def add_equipment(self, name: str, quantity: int, condition: str, location: str) -> bool:
        self.equipment.append({
            'name': name,
            'quantity': quantity,
            'condition': condition,
            'location': location
        })
        self.save_equipment()
        return True

    def load_equipment(self) -> list:
        equipment = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    name, quantity, condition, location = line.strip().split(',')
                    equipment.append({
                        'name': name,
                        'quantity': int(quantity),
                        'condition': condition,
                        'location': location
                    })
        except FileNotFoundError:
            pass
        return equipment

    def save_equipment(self):
        with open(self.filename, 'w') as file:
            for item in self.equipment:
                file.write(f"{item['name']},{item['quantity']},{item['condition']},{item['location']}\n")

    def update_equipment(self, index: int, name: str, quantity: int, condition: str, location: str) -> bool:
        if 0 <= index < len(self.equipment):
            self.equipment[index] = {
                'name': name,
                'quantity': quantity,
                'condition': condition,
                'location': location
            }
            self.save_equipment()
            return True
        return False

    def search_equipment(self, query: str) -> list:
        return [item for item in self.equipment if query.lower() in item['name'].lower()]

    def set_alert(self, index: int, alert_message: str) -> bool:
        if 0 <= index < len(self.equipment):
            self.alerts[index] = alert_message
            self.save_alerts()
            return True
        return False

    def load_alerts(self) -> list:
        alerts = []
        try:
            with open('alerts.txt', 'r') as file:
                for line in file:
                    alerts.append(line.strip())
        except FileNotFoundError:
            pass
        return alerts

    def save_alerts(self):
        with open('alerts.txt', 'w') as file:
            for alert in self.alerts:
                file.write(f"{alert}\n")
class EquipmentManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.equipment = self.load_equipment()
        self.alerts = {}

    def load_equipment(self) -> list:
        equipment = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    name, quantity, condition, location = line.strip().split('|')
                    equipment.append({
                        'name': name,
                        'quantity': int(quantity),
                        'condition': condition,
                        'location': location
                    })
        except FileNotFoundError:
            open(self.filename, 'w').close()  # Create file if it doesn't exist
        return equipment

    def add_equipment(self, name: str, quantity: int, condition: str, location: str) -> bool:
        self.equipment.append({
            'name': name,
            'quantity': quantity,
            'condition': condition,
            'location': location
        })
        self.save_equipment()
        return True

    def update_equipment(self, name: str, quantity: int, condition: str, location: str) -> None:
        for item in self.equipment:
            if item['name'] == name:
                item['quantity'] = quantity
                item['condition'] = condition
                item['location'] = location
                self.save_equipment()
                return

    def get_equipment(self) -> list:
        return self.equipment

    def search_equipment(self, query: str) -> list:
        return [item for item in self.equipment if query.lower() in item['name'].lower()]

    def filter_equipment(self, condition: str, availability: bool) -> list:
        return [item for item in self.equipment if item['condition'] == condition and (item['quantity'] > 0) == availability]

    def save_equipment(self) -> None:
        with open(self.filename, 'w') as file:
            for item in self.equipment:
                file.write(f"{item['name']}|{item['quantity']}|{item['condition']}|{item['location']}\n")

    def set_alert(self, equipment_name: str, alert_message: str) -> None:
        self.alerts[equipment_name] = alert_message

    def get_equipment_details(self, name: str) -> dict:
        for item in self.equipment:
            if item['name'] == name:
                return item
        return None
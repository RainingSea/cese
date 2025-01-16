class EquipmentManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_equipment()

    def load_equipment(self):
        """Load equipment from the text file into memory."""
        self.equipment = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    name, quantity, condition, location = line.strip().split(',')
                    self.equipment.append({
                        'name': name,
                        'quantity': int(quantity),
                        'condition': condition,
                        'location': location
                    })
        except FileNotFoundError:
            pass

    def add_equipment(self, name: str, quantity: int, condition: str, location: str) -> bool:
        """Add new equipment."""
        self.equipment.append({
            'name': name,
            'quantity': quantity,
            'condition': condition,
            'location': location
        })
        with open(self.filename, 'a') as file:
            file.write(f"{name},{quantity},{condition},{location}\n")
        return True

    def update_equipment(self, name: str, quantity: int, condition: str, location: str) -> bool:
        """Update existing equipment."""
        for item in self.equipment:
            if item['name'] == name:
                item['quantity'] = quantity
                item['condition'] = condition
                item['location'] = location
                self.save_equipment()
                return True
        return False

    def save_equipment(self):
        """Save equipment data back to the text file."""
        with open(self.filename, 'w') as file:
            for item in self.equipment:
                file.write(f"{item['name']},{item['quantity']},{item['condition']},{item['location']}\n")

    def search_equipment(self, query: str) -> list:
        """Search for equipment by name."""
        return [item for item in self.equipment if query.lower() in item['name'].lower()]

    def filter_equipment(self, condition: str) -> list:
        """Filter equipment by condition."""
        return [item for item in self.equipment if item['condition'] == condition]
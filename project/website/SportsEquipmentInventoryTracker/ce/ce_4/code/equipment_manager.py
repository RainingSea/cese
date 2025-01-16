class EquipmentManager:
    def __init__(self, equipment_file: str):
        self.equipment_file = equipment_file
        self.equipment = self.load_equipment()

    def add_equipment(self, name: str, quantity: int, condition: str, availability: str, location: str) -> None:
        with open(self.equipment_file, 'a') as f:
            f.write(f"{name},{quantity},{condition},{availability},{location}\n")
        self.equipment.append((name, quantity, condition, availability, location))

    def update_equipment(self, name: str, quantity: int, condition: str, availability: str, location: str) -> None:
        self.equipment = [eq for eq in self.equipment if eq[0] != name]
        self.add_equipment(name, quantity, condition, availability, location)

    def search_equipment(self, query: str) -> list:
        return [eq for eq in self.equipment if query.lower() in eq[0].lower()]

    def filter_equipment(self, condition: str, availability: str) -> list:
        return [eq for eq in self.equipment if eq[2] == condition and eq[3] == availability]

    def load_equipment(self) -> list:
        equipment = []
        try:
            with open(self.equipment_file, 'r') as f:
                for line in f:
                    name, quantity, condition, availability, location = line.strip().split(',')
                    equipment.append((name, int(quantity), condition, availability, location))
        except FileNotFoundError:
            pass
        return equipment
class EquipmentManager:
    def __init__(self):
        self.equipment_list = self.load_equipment()

    def load_equipment(self):
        equipment = []
        with open('equipment.txt', 'r') as file:
            for line in file:
                name, quantity, condition, location = line.strip().split('|')
                equipment.append({
                    'name': name,
                    'quantity': int(quantity),
                    'condition': condition,
                    'location': location
                })
        return equipment

    def add_equipment(self, name: str, quantity: int, condition: str, location: str) -> bool:
        self.equipment_list.append({
            'name': name,
            'quantity': quantity,
            'condition': condition,
            'location': location
        })
        with open('equipment.txt', 'a') as file:
            file.write(f"{name}|{quantity}|{condition}|{location}\n")
        return True

    def view_equipment(self) -> list:
        return self.equipment_list

    def search_equipment(self, query: str) -> list:
        return [equipment for equipment in self.equipment_list if query.lower() in equipment['name'].lower()]

    def filter_equipment(self, criteria: dict) -> list:
        filtered = self.equipment_list
        for key, value in criteria.items():
            filtered = [equipment for equipment in filtered if equipment[key] == value]
        return filtered
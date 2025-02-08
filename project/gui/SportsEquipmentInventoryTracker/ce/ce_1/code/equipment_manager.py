import json

class EquipmentManager:
    def __init__(self):
        self.data = []
        self.load_data()

    def load_data(self):
        try:
            with open('equipment.json', 'r') as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = []

    def save_data(self):
        with open('equipment.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    def add_equipment(self, equipment: dict):
        self.data.append(equipment)
        self.save_data()

    def update_equipment(self, equipment_id: int, updated_data: dict):
        if 0 <= equipment_id < len(self.data):
            self.data[equipment_id].update(updated_data)
            self.save_data()

    def search_equipment(self, query: str) -> list:
        return [equipment for equipment in self.data if query.lower() in equipment['type'].lower()]

    def filter_equipment(self, criteria: dict) -> list:
        filtered_data = self.data
        for key, value in criteria.items():
            filtered_data = [equipment for equipment in filtered_data if equipment.get(key) == value]
        return filtered_data
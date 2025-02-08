import json
from equipment import Equipment

class InventoryManager:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.equipment_list = self.load_data()

    def load_data(self) -> list:
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                return [Equipment(**item) for item in data]
        except FileNotFoundError:
            return []

    def save_data(self) -> None:
        with open(self.data_file, 'w') as file:
            json.dump([vars(equipment) for equipment in self.equipment_list], file, indent=4)

    def add_equipment(self, equipment: dict) -> None:
        new_equipment = Equipment(**equipment)
        self.equipment_list.append(new_equipment)
        self.save_data()

    def update_equipment(self, name: str, updated_info: dict) -> None:
        for equipment in self.equipment_list:
            if equipment.name == name:
                for key, value in updated_info.items():
                    setattr(equipment, key, value)
                self.save_data()
                break

    def search_equipment(self, query: str) -> list:
        return [equipment for equipment in self.equipment_list if query.lower() in equipment.name.lower()]

    def filter_equipment(self, criteria: dict) -> list:
        filtered_list = self.equipment_list
        for key, value in criteria.items():
            filtered_list = [equipment for equipment in filtered_list if getattr(equipment, key) == value]
        return filtered_list
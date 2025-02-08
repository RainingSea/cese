import json
from typing import List, Dict
from equipment import Equipment

class InventoryManager:
    def __init__(self):
        self.equipment_list: List[Equipment] = []
        self.load_data()

    def add_equipment(self, equipment: Equipment) -> None:
        self.equipment_list.append(equipment)
        self.save_data()

    def update_equipment(self, equipment: Equipment) -> None:
        for index, item in enumerate(self.equipment_list):
            if item.id == equipment.id:
                self.equipment_list[index] = equipment
                break
        self.save_data()

    def delete_equipment(self, equipment_id: str) -> None:
        self.equipment_list = [item for item in self.equipment_list if item.id != equipment_id]
        self.save_data()

    def search_equipment(self, query: str) -> List[Equipment]:
        return [item for item in self.equipment_list if query.lower() in item.name.lower()]

    def filter_equipment(self, criteria: Dict) -> List[Equipment]:
        filtered_list = self.equipment_list
        for key, value in criteria.items():
            filtered_list = [item for item in filtered_list if getattr(item, key) == value]
        return filtered_list

    def load_data(self) -> None:
        try:
            with open('equipment_data.json', 'r') as file:
                data = json.load(file)
                self.equipment_list = [Equipment(**item) for item in data]
        except FileNotFoundError:
            self.equipment_list = []

    def save_data(self) -> None:
        with open('equipment_data.json', 'w') as file:
            json.dump([item.__dict__ for item in self.equipment_list], file, indent=4)
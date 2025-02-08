import json
from typing import List, Dict
from equipment import Equipment

class InventoryManager:
    def __init__(self) -> None:
        self.equipment_list: List[Equipment] = []
        self.load_data()

    def add_equipment(self, name: str, type: str, quantity: int, condition: str, location: str) -> None:
        equipment = Equipment(name, type, quantity, condition, location)
        self.equipment_list.append(equipment)
        self.save_data()

    def update_equipment(self, name: str, quantity: int, condition: str, location: str) -> None:
        for equipment in self.equipment_list:
            if equipment.name == name:
                equipment.quantity = quantity
                equipment.condition = condition
                equipment.location = location
                equipment.availability = quantity > 0
                self.save_data()
                return

    def search_equipment(self, query: str) -> List[Equipment]:
        return [equipment for equipment in self.equipment_list if query.lower() in equipment.name.lower()]

    def filter_equipment(self, criteria: Dict) -> List[Equipment]:
        filtered_list = self.equipment_list
        for key, value in criteria.items():
            filtered_list = [equipment for equipment in filtered_list if getattr(equipment, key) == value]
        return filtered_list

    def load_data(self) -> None:
        try:
            with open('equipment.json', 'r') as file:
                data = json.load(file)
                self.equipment_list = [Equipment(**item) for item in data]
        except FileNotFoundError:
            self.equipment_list = []

    def save_data(self) -> None:
        with open('equipment.json', 'w') as file:
            json.dump([equipment.__dict__ for equipment in self.equipment_list], file, indent=4)
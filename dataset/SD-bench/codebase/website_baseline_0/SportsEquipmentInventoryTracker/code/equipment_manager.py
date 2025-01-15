import json
from models import Equipment

class EquipmentManager:
    def __init__(self):
        self.equipment_list = []
        self.load_equipment()

    def add_equipment(self, equipment: Equipment) -> None:
        equipment.save()
        self.equipment_list.append(equipment)

    def update_equipment(self, equipment: Equipment) -> None:
        for idx, eq in enumerate(self.equipment_list):
            if eq.name == equipment.name:
                self.equipment_list[idx] = equipment
                break
        equipment.save()

    def filter_equipment(self, criteria: dict) -> list:
        filtered = []
        for equipment in self.equipment_list:
            if all(getattr(equipment, key) == value for key, value in criteria.items()):
                filtered.append(equipment)
        return filtered

    def load_equipment(self) -> None:
        try:
            with open('equipment.txt', 'r') as file:
                for line in file:
                    equipment_data = json.loads(line.strip())
                    self.equipment_list.append(Equipment(equipment_data['name'], equipment_data['type'],
                                                          equipment_data['quantity'], equipment_data['condition'],
                                                          equipment_data['location']))
        except FileNotFoundError:
            pass  # If the file does not exist, we simply ignore it
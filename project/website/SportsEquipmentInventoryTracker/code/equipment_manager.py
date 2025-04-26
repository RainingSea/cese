from tools import load_equipment, save_equipment

class EquipmentManager:
    def __init__(self):
        self.equipment = load_equipment()

    def add_equipment(self, name: str, type_: str, quantity: int, condition: str, location: str) -> None:
        self.equipment.append((name, type_, quantity, condition, location))
        save_equipment(self.equipment)

    def update_equipment(self, name: str, quantity: int, condition: str, location: str) -> None:
        for i, equip in enumerate(self.equipment):
            if equip[0] == name:
                self.equipment[i] = (name, equip[1], quantity, condition, location)
                save_equipment(self.equipment)
                break

    def delete_equipment(self, name: str) -> None:
        self.equipment = [equip for equip in self.equipment if equip[0] != name]
        save_equipment(self.equipment)

    def search_equipment(self, query: str):
        return [equip for equip in self.equipment if query.lower() in equip[0].lower()]

    def filter_equipment(self, criteria: str):
        return [equip for equip in self.equipment if criteria.lower() in equip[1].lower()]

    def load_equipment(self):
        self.equipment = load_equipment()

    def save_equipment(self):
        save_equipment(self.equipment)
class EquipmentManager:
    def __init__(self):
        self.equipment = []
        self.equipment_id_counter = 0

    def load_equipment(self):
        try:
            with open('equipment.txt', 'r') as file:
                for line in file:
                    name, type_, quantity, condition, location = line.strip().split('|')
                    self.equipment.append({
                        'id': self.equipment_id_counter,
                        'name': name,
                        'type': type_,
                        'quantity': int(quantity),
                        'condition': condition,
                        'location': location
                    })
                    self.equipment_id_counter += 1
        except FileNotFoundError:
            pass
        return self.equipment

    def save_equipment(self):
        with open('equipment.txt', 'w') as file:
            for item in self.equipment:
                file.write(f"{item['name']}|{item['type']}|{item['quantity']}|{item['condition']}|{item['location']}\n")

    def add_equipment(self, name: str, type_: str, quantity: int, condition: str, location: str) -> bool:
        equipment_item = {
            'id': self.equipment_id_counter,
            'name': name,
            'type': type_,
            'quantity': quantity,
            'condition': condition,
            'location': location
        }
        self.equipment.append(equipment_item)
        self.equipment_id_counter += 1
        self.save_equipment()
        return True
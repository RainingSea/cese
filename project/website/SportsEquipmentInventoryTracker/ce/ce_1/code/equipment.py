class Equipment:
    def __init__(self, name: str, type: str, quantity: int, condition: str, availability: bool, location: str):
        self.name = name
        self.type = type
        self.quantity = quantity
        self.condition = condition
        self.availability = availability
        self.location = location

    def save(self):
        with open('equipment.txt', 'a') as file:
            file.write(f"{self.name}|{self.type}|{self.quantity}|{self.condition}|{self.availability}|{self.location}\n")

    @staticmethod
    def load_equipment() -> list:
        equipment = []
        try:
            with open('equipment.txt', 'r') as file:
                for line in file:
                    name, type_, quantity, condition, availability, location = line.strip().split('|')
                    equipment.append(Equipment(name, type_, int(quantity), condition, availability == 'True', location))
        except FileNotFoundError:
            pass
        return equipment
import os

class CharityManager:
    def __init__(self):
        self.charities = {}

    def load_charities(self):
        if os.path.exists('charities.txt'):
            with open('charities.txt', 'r') as file:
                for line in file:
                    charity_id, name, description = line.strip().split('|')
                    self.charities[charity_id] = {'name': name, 'description': description}

    def get_charities(self) -> list:
        return [{'id': charity_id, 'name': charity['name']} for charity_id, charity in self.charities.items()]

    def get_charity_details(self, charity_id: str) -> dict:
        return self.charities.get(charity_id, {})
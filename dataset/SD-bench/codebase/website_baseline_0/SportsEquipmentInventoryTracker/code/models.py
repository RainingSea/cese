import json

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(json.dumps(self.__dict__) + '\n')

    @staticmethod
    def load(username: str) -> 'User':
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = json.loads(line.strip())
                if user_data['username'] == username:
                    return User(user_data['username'], user_data['password'])
        return None

class Equipment:
    def __init__(self, name: str, type: str, quantity: int, condition: str, location: str):
        self.name = name
        self.type = type
        self.quantity = quantity
        self.condition = condition
        self.location = location

    def save(self) -> None:
        with open('equipment.txt', 'a') as file:
            file.write(json.dumps(self.__dict__) + '\n')

    @staticmethod
    def load(name: str) -> 'Equipment':
        with open('equipment.txt', 'r') as file:
            for line in file:
                equipment_data = json.loads(line.strip())
                if equipment_data['name'] == name:
                    return Equipment(equipment_data['name'], equipment_data['type'],
                                     equipment_data['quantity'], equipment_data['condition'],
                                     equipment_data['location'])
        return None
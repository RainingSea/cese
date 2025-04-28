class ItemManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.items = self.load_items()

    def add_item(self, name: str, description: str, price: float) -> bool:
        with open(self.filename, 'a') as file:
            file.write(f"{name}|{description}|{price}\n")
        self.items.append(f"{name}|{description}|{price}")
        return True

    def get_items(self) -> list:
        return [item.split('|')[0] for item in self.items]

    def get_item_details(self, name: str) -> dict:
        for item in self.items:
            if item.split('|')[0] == name:
                details = item.split('|')
                return {'name': details[0], 'description': details[1], 'price': details[2]}
        return {}

    def load_items(self) -> list:
        try:
            with open(self.filename, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            logging.error(f"File '{self.filename}' not found. Returning empty item list.")
            return []
        except Exception as e:
            logging.error(f"Error loading items from '{self.filename}': {e}")
            return []
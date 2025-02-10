class ItemManager:
    def __init__(self, items_file: str):
        self.items_file = items_file
        self.items = self.load_items()

    def load_items(self) -> list:
        items = []
        try:
            with open(self.items_file, 'r') as file:
                for line in file:
                    item_id, name, description, price = line.strip().split('|')
                    items.append({'id': int(item_id), 'name': name, 'description': description, 'price': float(price)})
        except FileNotFoundError:
            pass
        return items

    def add_item(self, name: str, description: str, price: float) -> bool:
        item_id = len(self.items) + 1
        with open(self.items_file, 'a') as file:
            file.write(f"{item_id}|{name}|{description}|{price}\n")
        self.items.append({'id': item_id, 'name': name, 'description': description, 'price': price})
        return True

    def get_item_details(self, item_id: int) -> dict:
        for item in self.items:
            if item['id'] == item_id:
                return item
        return {}
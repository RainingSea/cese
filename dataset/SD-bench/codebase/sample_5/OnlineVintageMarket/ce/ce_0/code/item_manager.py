class ItemManager:
    def __init__(self):
        self.items = []
    
    def load_items(self):
        with open('items.txt', 'r') as f:
            for line in f:
                item_id, name, description, price = line.strip().split('|')
                self.items.append({
                    'id': int(item_id),
                    'name': name,
                    'description': description,
                    'price': float(price)
                })

    def add_item(self, name: str, description: str, price: float) -> None:
        item_id = len(self.items) + 1
        new_item = {'id': item_id, 'name': name, 'description': description, 'price': price}
        self.items.append(new_item)
        with open('items.txt', 'a') as f:
            f.write(f"{item_id}|{name}|{description}|{price}\n")

    def get_item_details(self, item_id: int) -> dict:
        for item in self.items:
            if item['id'] == item_id:
                return item
        return {}

    def search_items(self, query: str) -> list:
        return [item for item in self.items if query.lower() in item['name'].lower()]
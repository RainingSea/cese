class ItemManager:
    def __init__(self):
        self.items_file = 'items.txt'
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        try:
            with open(self.items_file, 'r'):
                pass
        except FileNotFoundError:
            with open(self.items_file, 'w'):
                pass

    def get_all_items(self):
        items = []
        with open(self.items_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    items.append({
                        'title': parts[0],
                        'description': parts[1],
                        'price': parts[2],
                        'seller': parts[3]
                    })
        return items

    def search_items(self, query):
        query = query.lower()
        items = self.get_all_items()
        return [item for item in items if 
                query in item['title'].lower() or 
                query in item['description'].lower()]

    def add_item(self, title, description, price, seller):
        if not title or not description or not price or not seller:
            return False
            
        with open(self.items_file, 'a') as f:
            f.write(f"{title}|{description}|{price}|{seller}\n")
        return True

    def get_item_by_id(self, item_id):
        items = self.get_all_items()
        try:
            return items[int(item_id)]
        except (IndexError, ValueError):
            return None
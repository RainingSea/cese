import os

class ItemManager:
    def __init__(self):
        self.items_file = 'items.txt'
        if not os.path.exists(self.items_file):
            open(self.items_file, 'w').close()

    def get_items(self):
        items = []
        with open(self.items_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    items.append({
                        'id': parts[0],
                        'title': parts[1],
                        'description': parts[2],
                        'price': float(parts[3]),
                        'seller': parts[4]
                    })
        return items

    def search_items(self, query):
        items = self.get_items()
        return [item for item in items 
                if query.lower() in item['title'].lower() 
                or query.lower() in item['description'].lower()]

    def get_item_details(self, item_id):
        with open(self.items_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5 and parts[0] == item_id:
                    return {
                        'id': parts[0],
                        'title': parts[1],
                        'description': parts[2],
                        'price': float(parts[3]),
                        'seller': parts[4]
                    }
        return None

    def add_item(self, title, description, price, seller):
        items = self.get_items()
        item_id = str(len(items) + 1)
        try:
            with open(self.items_file, 'a') as f:
                f.write(f"{item_id}|{title}|{description}|{price}|{seller}\n")
            return True
        except:
            return False
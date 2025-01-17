class ShoppingList:
    def __init__(self, name: str):
        self.name = name
        self.items = []

    def add_item(self, item: str, category: str) -> None:
        self.items.append({'item': item, 'category': category})

    def remove_item(self, item: str) -> None:
        self.items = [i for i in self.items if i['item'] != item]

    def set_reminder(self, date: str, time: str) -> None:
        self.reminder = {'date': date, 'time': time}
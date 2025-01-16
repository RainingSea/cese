class Order:
    def __init__(self, user, items):
        self.user = user
        self.items = items

    def save_order(self):
        with open('orders.txt', 'a') as file:
            file.write(f"{self.user.username}|{self.items}\n")
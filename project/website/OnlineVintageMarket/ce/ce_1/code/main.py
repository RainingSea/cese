class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username},{self.password}\n")

    def login(self) -> bool:
        with open('users.txt', 'r') as file:
            for line in file:
                user, pwd = line.strip().split(',')
                if user == self.username and pwd == self.password:
                    return True
        return False


class Item:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def create_listing(self):
        with open('items.txt', 'a') as file:
            file.write(f"{self.name},{self.description},{self.price}\n")

    def get_details(self) -> str:
        return f"Name: {self.name}, Description: {self.description}, Price: {self.price}"


class Main:
    def __init__(self):
        self.user = None
        self.item = None

    def main(self) -> str:
        return "Welcome to Online Vintage Market"

    def login_user(self, username: str, password: str) -> bool:
        self.user = User(username, password)
        return self.user.login()

    def register_user(self, username: str, password: str):
        self.user = User(username, password)
        self.user.register()

    def list_items(self) -> str:
        items_list = []
        with open('items.txt', 'r') as file:
            for line in file:
                items_list.append(line.strip())
        return "\n".join(items_list)

    def view_item_details(self, item_name: str) -> str:
        with open('items.txt', 'r') as file:
            for line in file:
                name, description, price = line.strip().split(',')
                if name == item_name:
                    return f"Name: {name}, Description: {description}, Price: {price}"
        return "Item not found."


if __name__ == "__main__":
    app = Main()
    print(app.main())
from flask import Flask, render_template, request, redirect, url_for
import os

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append((username, password))
        self.save_users()
        return True

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                self.users = [line.strip().split('|') for line in file.readlines()]

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

class ItemManager:
    def __init__(self):
        self.items = []
        self.load_items()

    def add_item(self, name: str, description: str, price: float) -> None:
        self.items.append((name, description, price))
        self.save_items()

    def get_items(self) -> list:
        return self.items

    def get_item_details(self, name: str) -> dict:
        for item in self.items:
            if item[0] == name:
                return {'name': item[0], 'description': item[1], 'price': item[2]}
        return {}

    def load_items(self) -> None:
        if os.path.exists('items.txt'):
            with open('items.txt', 'r') as file:
                self.items = [line.strip().split('|') for line in file.readlines()]
                self.items = [(name, desc, float(price)) for name, desc, price in self.items]

    def save_items(self) -> None:
        with open('items.txt', 'w') as file:
            for item in self.items:
                file.write('|'.join([item[0], item[1], str(item[2])]) + '\n')

app = Flask(__name__)
user_manager = UserManager()
item_manager = ItemManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    items = item_manager.get_items()
    return render_template('home.html', items=items)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        item_manager.add_item(name, description, price)
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/item/<name>')
def item_details(name):
    item = item_manager.get_item_details(name)
    return render_template('item_details.html', item=item)

if __name__ == '__main__':
    app.run(port=8379, debug=False)

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        self.save_users()
        return True

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append({'username': username, 'password': password})
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user['username']}|{user['password']}\n")


class ItemManager:
    def __init__(self):
        self.items = []
        self.load_items()

    def add_item(self, name: str, description: str, price: float) -> None:
        self.items.append({'name': name, 'description': description, 'price': price})
        self.save_items()

    def get_items(self) -> list:
        return self.items

    def get_item_details(self, name: str) -> dict:
        for item in self.items:
            if item['name'] == name:
                return item
        return {}

    def load_items(self) -> None:
        try:
            with open('items.txt', 'r') as file:
                for line in file:
                    name, description, price = line.strip().split('|')
                    self.items.append({'name': name, 'description': description, 'price': float(price)})
        except FileNotFoundError:
            pass

    def save_items(self) -> None:
        with open('items.txt', 'w') as file:
            for item in self.items:
                file.write(f"{item['name']}|{item['description']}|{item['price']}\n")


app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
item_manager = ItemManager()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
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
    app.run(port=8210, debug=False)

from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    users.append((username, password))
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append((username, password))
        with open('users.txt', 'a') as file:
            file.write(f"{username},{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

class ItemManager:
    def __init__(self):
        self.items = self.load_items()

    def load_items(self):
        items = []
        if os.path.exists('items.txt'):
            with open('items.txt', 'r') as file:
                for line in file:
                    item_name, description, price = line.strip().split(',')
                    items.append((item_name, description, float(price)))
        return items

    def add_item(self, name: str, description: str, price: float) -> None:
        self.items.append((name, description, price))
        with open('items.txt', 'a') as file:
            file.write(f"{name},{description},{price}\n")

    def get_items(self) -> list:
        return self.items

    def get_item_details(self, name: str) -> str:
        for item in self.items:
            if item[0] == name:
                return f"Name: {item[0]}, Description: {item[1]}, Price: {item[2]}"
        return "Item not found."

user_manager = UserManager()
item_manager = ItemManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists."
    return render_template('registration.html')

@app.route('/home', methods=['GET'])
def home():
    items = item_manager.get_items()
    return render_template('home.html', items=items)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        item_name = request.form['item_name']
        description = request.form['description']
        price = float(request.form['price'])
        item_manager.add_item(item_name, description, price)
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/item/<name>', methods=['GET'])
def item_details(name):
    details = item_manager.get_item_details(name)
    return render_template('item_details.html', details=details)

if __name__ == '__main__':
    app.run(port=8378, debug=False)

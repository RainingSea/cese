from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def login(self) -> bool:
        with open('users.txt', 'r') as f:
            users = f.readlines()
            for user in users:
                u, p = user.strip().split('|')
                if u == self.username and p == self.password:
                    return True
        return False

class Item:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def create_listing(self):
        with open('items.txt', 'a') as f:
            f.write(f"{self.name}|{self.description}|{self.price}\n")

    def get_details(self) -> str:
        return f"Name: {self.name}, Description: {self.description}, Price: {self.price}"

class ItemManager:
    def __init__(self):
        self.items = []

    def load_items(self):
        self.items.clear()  # Clear existing items to avoid duplicates
        if os.path.exists('items.txt'):
            with open('items.txt', 'r') as f:
                items = f.readlines()
                for item in items:
                    name, description, price = item.strip().split('|')
                    self.items.append(Item(name, description, float(price)))

    def get_items(self):
        return self.items

    def get_item_details(self, item_id: int) -> Item:
        return self.items[item_id]

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self):
        self.users.clear()  # Clear existing users to avoid duplicates
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                users = f.readlines()
                for user in users:
                    username, password = user.strip().split('|')
                    self.users.append(User(username, password))

user_manager = UserManager()
user_manager.load_users()
item_manager = ItemManager()
item_manager.load_items()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login():
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.register()
        user_manager.load_users()  # Reload users after registration
        flash('Registration successful! Please log in.')
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
        new_item = Item(name, description, price)
        new_item.create_listing()
        item_manager.load_items()  # Reload items after listing a new item
        flash('Item listed successfully!')
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/item/<int:item_id>')
def item_details(item_id):
    item = item_manager.get_item_details(item_id)
    return render_template('item_details.html', item=item)

if __name__ == '__main__':
    app.run(port=8213, debug=False)

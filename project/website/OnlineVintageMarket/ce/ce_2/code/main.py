from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")
        return True

    def login(self):
        users = load_users()
        for user in users:
            if user.username == self.username and user.password == self.password:
                return True
        return False

class Item:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    def create_listing(self):
        with open('items.txt', 'a') as f:
            f.write(f"{self.name}|{self.description}|{self.price}\n")
        return True

    def get_details(self):
        return f"Name: {self.name}, Description: {self.description}, Price: {self.price}"

def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

def load_items():
    items = []
    if os.path.exists('items.txt'):
        with open('items.txt', 'r') as f:
            for line in f:
                name, description, price = line.strip().split('|')
                items.append(Item(name, description, float(price)))
    return items

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.register()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home', methods=['GET'])
def home():
    items = load_items()
    return render_template('home.html', items=items)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        item = Item(name, description, float(price))
        item.create_listing()
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/item/<item_name>', methods=['GET'])
def item_details(item_name):
    items = load_items()
    for item in items:
        if item.name == item_name:
            return render_template('item_details.html', item=item)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=8212, debug=False)

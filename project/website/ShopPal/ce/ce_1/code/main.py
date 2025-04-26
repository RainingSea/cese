from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as f:
            return [line.strip().split('|') for line in f.readlines()]

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False  # User already exists
        self.users.append([username, password])
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as f:
            for user in self.users:
                f.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

class ProductManager:
    def __init__(self):
        self.collections = self.load_collections()
        self.price_tracking = self.load_price_tracking()

    def load_collections(self):
        if not os.path.exists('collections.txt'):
            return {}
        with open('collections.txt', 'r') as f:
            return {line.split('|')[0]: line.strip().split('|')[1:] for line in f.readlines()}

    def load_price_tracking(self):
        if not os.path.exists('price_tracking.txt'):
            return {}
        with open('price_tracking.txt', 'r') as f:
            return {line.split('|')[0]: line.strip().split('|')[1:] for line in f.readlines()}

    def add_product_to_collection(self, user: str, product: str) -> bool:
        if user not in self.collections:
            self.collections[user] = []
        self.collections[user].append(product)
        self.save_collections()
        return True

    def save_collections(self):
        with open('collections.txt', 'w') as f:
            for user, products in self.collections.items():
                f.write(user + '|' + '|'.join(products) + '\n')

    def track_price_change(self, user: str, product: str) -> bool:
        if user not in self.price_tracking:
            self.price_tracking[user] = []
        self.price_tracking[user].append(product)
        self.save_price_tracking()
        return True

    def save_price_tracking(self):
        with open('price_tracking.txt', 'w') as f:
            for user, products in self.price_tracking.items():
                f.write(user + '|' + '|'.join(products) + '\n')

    def search_products(self, query: str):
        # Placeholder for product search logic
        return []

user_manager = UserManager()
product_manager = ProductManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register(username, password):
        return redirect('/login')
    return 'Registration failed', 400

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = product_manager.search_products(query)
    return render_template('dashboard.html', results=results)

if __name__ == '__main__':
    app.run(port=8239, debug=False)

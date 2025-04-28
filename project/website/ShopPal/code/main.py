from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class CollectionManager:
    def __init__(self):
        self.collections = self.load_collections()

    def load_collections(self):
        collections = {}
        if os.path.exists('collections.txt'):
            with open('collections.txt', 'r') as file:
                for line in file:
                    parts = line.strip().split('|')
                    username = parts[0]
                    product_ids = parts[1:] if len(parts) > 1 else []
                    collections[username] = product_ids
        return collections

    def add_product(self, username: str, product_id: str) -> None:
        if username not in self.collections:
            self.collections[username] = []
        if product_id not in self.collections[username]:
            self.collections[username].append(product_id)
            self.save_collections()

    def remove_product(self, username: str, product_id: str) -> None:
        if username in self.collections and product_id in self.collections[username]:
            self.collections[username].remove(product_id)
            self.save_collections()

    def get_collection(self, username: str) -> list:
        return self.collections.get(username, [])

    def save_collections(self):
        with open('collections.txt', 'w') as file:
            for username, product_ids in self.collections.items():
                file.write(f"{username}|{'|'.join(product_ids)}\n")

class ProductManager:
    def __init__(self):
        self.products = self.load_products()

    def load_products(self):
        products = {}
        if os.path.exists('products.txt'):
            with open('products.txt', 'r') as file:
                for line in file:
                    product_id, details = line.strip().split('|')
                    products[product_id] = details
        return products

    def get_product(self, product_id: str):
        return self.products.get(product_id, {})

    def track_price_changes(self, product_id: str, new_price: float) -> None:
        # Placeholder for tracking price changes
        pass

    def receive_notifications(self, username: str, product_id: str) -> None:
        # Placeholder for enabling notifications
        pass

user_manager = UserManager()
collection_manager = CollectionManager()
product_manager = ProductManager()

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
            return "Registration failed. Username already exists."
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        product_id = request.form['product_id']
        action = request.form['action']
        if action == 'add':
            collection_manager.add_product(session['username'], product_id)
        elif action == 'remove':
            collection_manager.remove_product(session['username'], product_id)
    products = product_manager.products.keys()  # Load available products
    return render_template('dashboard.html', collection=collection_manager.get_collection(session['username']), products=products)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Invalid credentials. Please try again."

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/product/<product_id>')
def product_detail(product_id):
    product = product_manager.get_product(product_id)
    return render_template('product_detail.html', product=product)

if __name__ == '__main__':
    app.run(port=8413, debug=False)

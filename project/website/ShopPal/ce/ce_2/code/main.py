from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

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

class ProductManager:
    def __init__(self):
        self.products = self.load_products()
        self.collections = self.load_collections()

    def load_products(self):
        products = {}
        if os.path.exists('products.txt'):
            with open('products.txt', 'r') as file:
                for line in file:
                    product_id, details = line.strip().split('|', 1)
                    products[product_id] = details
        return products

    def load_collections(self):
        collections = {}
        if os.path.exists('collections.txt'):
            with open('collections.txt', 'r') as file:
                for line in file:
                    username, collection_name = line.strip().split('|')
                    if username not in collections:
                        collections[username] = []
                    collections[username].append(collection_name)
        return collections

    def add_product(self, product_id: str, details: dict) -> None:
        self.products[product_id] = details
        with open('products.txt', 'a') as file:
            file.write(f"{product_id}|{details}\n")

    def get_product(self, product_id: str) -> dict:
        return self.products.get(product_id, {})

    def create_collection(self, username: str, collection_name: str) -> None:
        if username not in self.collections:
            self.collections[username] = []
        self.collections[username].append(collection_name)
        with open('collections.txt', 'a') as file:
            file.write(f"{username}|{collection_name}\n")

    def track_price_changes(self) -> None:
        pass  # Placeholder for future implementation

user_manager = UserManager()
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
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/product/<product_id>')
def product_detail(product_id):
    product = product_manager.get_product(product_id)
    return render_template('product_detail.html', product=product)

if __name__ == '__main__':
    app.run(port=8412, debug=False)

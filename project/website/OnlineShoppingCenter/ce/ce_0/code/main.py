from flask import Flask, render_template, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self) -> list:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str, email: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False  # User already exists
        self.users.append([username, password, email])
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

class ProductManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.products = self.load_products()

    def load_products(self) -> list:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

class CartManager:
    def __init__(self, filename: str):
        self.filename = filename

    def add_to_cart(self, username: str, product_id: str) -> None:
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{product_id}\n")

    def remove_from_cart(self, username: str, product_id: str) -> None:
        lines = []
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        with open(self.filename, 'w') as file:
            for line in lines:
                if not (line.startswith(f"{username}|{product_id}")):
                    file.write(line)

    def load_cart(self, username: str) -> list:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as file:
            return [line.strip().split('|')[1] for line in file.readlines() if line.startswith(username)]

user_manager = UserManager('users.txt')
product_manager = ProductManager('products.txt')
cart_manager = CartManager('cart.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
        else:
            return "User already exists!"
    return render_template('registration.html')

@app.route('/product_listing')
def product_listing():
    products = product_manager.products
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    if 'username' in session:
        cart_manager.add_to_cart(session['username'], product_id)
    return redirect(url_for('product_listing'))

@app.route('/shopping_cart')
def shopping_cart():
    if 'username' in session:
        cart_items = cart_manager.load_cart(session['username'])
        return render_template('shopping_cart.html', cart_items=cart_items)
    return redirect(url_for('login'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Here you would typically process the payment and order confirmation
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation', methods=['POST'])
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8159, debug=True)

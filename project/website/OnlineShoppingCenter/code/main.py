from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import os
import json

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = {'password': password, 'email': email}
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        return user is not None and user['password'] == password

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = {'password': password, 'email': email}

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, details in self.users.items():
                file.write(f"{username}|{details['password']}|{details['email']}\n")

class ProductManager:
    def __init__(self):
        self.products = []
        self.load_products()

    def load_products(self) -> None:
        if os.path.exists('products.txt'):
            with open('products.txt', 'r') as file:
                for line in file:
                    self.products.append(line.strip())

    def get_products(self) -> list:
        return self.products

class CartManager:
    def __init__(self):
        self.cart = {}
        self.load_cart()

    def add_to_cart(self, product_id: str) -> None:
        if product_id in self.cart:
            self.cart[product_id] += 1
        else:
            self.cart[product_id] = 1
        self.save_cart()

    def remove_from_cart(self, product_id: str) -> None:
        if product_id in self.cart:
            del self.cart[product_id]
            self.save_cart()

    def get_cart(self) -> dict:
        return self.cart

    def save_cart(self) -> None:
        with open('cart.txt', 'w') as file:
            for product_id, quantity in self.cart.items():
                file.write(f"{product_id}|{quantity}\n")

    def load_cart(self) -> None:
        if os.path.exists('cart.txt'):
            with open('cart.txt', 'r') as file:
                for line in file:
                    product_id, quantity = line.strip().split('|')
                    self.cart[product_id] = int(quantity)

@app.route('/', methods=['GET', 'POST'])
def login():
    user_manager = UserManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('product_listing'))
        else:
            return "Login Failed"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    user_manager = UserManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
        else:
            return "Registration Failed"
    return render_template('registration.html')

@app.route('/products')
def product_listing():
    product_manager = ProductManager()
    products = product_manager.get_products()
    return render_template('product_listing.html', products=products)

@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    cart_manager = CartManager()
    if request.method == 'POST':
        data = request.get_json()
        product_id = data.get('product_id')
        cart_manager.add_to_cart(product_id)
        return '', 204
    cart = cart_manager.get_cart()
    return render_template('shopping_cart.html', cart=cart)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Here you would handle the order placement logic
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8209, debug=False)

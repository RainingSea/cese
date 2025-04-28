from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
        return users

    def register(self, username: str, password: str, email: str) -> bool:
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

    def load_products(self):
        products = []
        with open('products.txt', 'r') as file:
            for line in file:
                name, price = line.strip().split('|')
                products.append({'name': name, 'price': price})
        return products

    def get_products(self) -> list:
        return self.products

    def add_product(self, product: dict) -> None:
        self.products.append(product)
        with open('products.txt', 'a') as file:
            file.write(f"{product['name']}|{product['price']}\n")

class OrderManager:
    def __init__(self):
        self.orders = self.load_orders()

    def load_orders(self):
        orders = []
        with open('orders.txt', 'r') as file:
            for line in file:
                orders.append(line.strip())
        return orders

    def create_order(self, user: str, cart: list) -> bool:
        order_id = len(self.orders) + 1
        order_summary = f"Order ID: {order_id}, User: {user}, Cart: {cart}"
        self.orders.append(order_summary)
        with open('orders.txt', 'a') as file:
            file.write(order_summary + '\n')
        return True

    def get_order_summary(self, order_id: str) -> dict:
        for order in self.orders:
            if f"Order ID: {order_id}" in order:
                return {"summary": order}
        return {}

user_manager = UserManager()
product_manager = ProductManager()
order_manager = OrderManager()

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
    return render_template('registration.html')

@app.route('/product_listing')
def product_listing():
    products = product_manager.get_products()
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_name = request.form['product_name']
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_name)
    return redirect(url_for('product_listing'))

@app.route('/shopping_cart')
def shopping_cart():
    return render_template('shopping_cart.html', cart=session.get('cart', []))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        user = request.form['username']
        cart = session.get('cart', [])
        order_manager.create_order(user, cart)
        session.pop('cart', None)
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8371, debug=False)

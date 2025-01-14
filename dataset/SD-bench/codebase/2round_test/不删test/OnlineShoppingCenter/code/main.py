from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load_all():
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        return users

class Product:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price

    @staticmethod
    def load_all():
        products = []
        if os.path.exists('products.txt'):
            with open('products.txt', 'r') as file:
                for line in file:
                    id, name, price = line.strip().split('|')
                    products.append(Product(int(id), name, float(price)))
        return products

class Order:
    def __init__(self, user: User, products: list, shipping_address: str, payment_info: str):
        self.user = user
        self.products = products
        self.shipping_address = shipping_address
        self.payment_info = payment_info

    def save(self):
        with open('orders.txt', 'a') as file:
            product_ids = ','.join(str(product.id) for product in self.products)
            file.write(f"{self.user.username}|{product_ids}|{self.shipping_address}|{self.payment_info}\n")

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product: Product):
        self.items.append(product)

    def remove_item(self, product_id: int):
        self.items = [item for item in self.items if item.id != product_id]

    def clear(self):
        self.items = []

    def get_items(self):
        return self.items

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = User.load_all()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            session['cart'] = ShoppingCart()  # Initialize shopping cart
            return redirect(url_for('product_listing'))
    return "Invalid credentials", 401

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/product_listing')
def product_listing():
    products = Product.load_all()
    return render_template('product_listing.html', products=products)

@app.route('/shopping_cart')
def shopping_cart():
    cart = session.get('cart', ShoppingCart())
    return render_template('shopping_cart.html', items=cart.get_items())

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in Product.load_all() if p.id == product_id), None)
    if product:
        cart = session.get('cart', ShoppingCart())
        cart.add_item(product)
        session['cart'] = cart
    return redirect(url_for('product_listing'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', ShoppingCart())
    cart.remove_item(product_id)
    session['cart'] = cart
    return redirect(url_for('shopping_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        shipping_address = request.form['shipping_address']
        payment_info = request.form['payment_info']
        username = session.get('username')
        user = next((u for u in User.load_all() if u.username == username), None)
        cart = session.get('cart', ShoppingCart())
        order = Order(user, cart.get_items(), shipping_address, payment_info)
        order.save()
        cart.clear()
        session['cart'] = cart
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8064, debug=False)

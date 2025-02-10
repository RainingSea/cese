from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from product import Product
from order import Order
from cart import Cart
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and products from files
def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
    return users

def load_products():
    products = []
    if os.path.exists('products.txt'):
        with open('products.txt', 'r') as f:
            for line in f:
                id, name, price = line.strip().split('|')
                products.append(Product(int(id), name, float(price)))
    return products

users = load_users()
products = load_products()
cart = Cart()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        users.append(new_user)
        new_user.save_to_file()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/products')
def product_listing():
    return render_template('products.html', products=products)

@app.route('/cart')
def view_cart():
    return render_template('cart.html', items=cart.get_items())

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p.id == product_id), None)
    if product:
        cart.add_item(product)
    return redirect(url_for('product_listing'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        order = Order(session['user'], cart.get_items())
        order.save_to_file()
        cart.items.clear()  # Clear the cart after checkout
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8673, debug=False)

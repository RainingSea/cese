from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from product import Product
from order import Order

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file.read().strip().split('\n'):
            username, password, email = line.split('|')
            users.append(User(username, password, email))
    return users

def load_products():
    products = []
    with open('products.txt', 'r') as file:
        for line in file.read().strip().split('\n'):
            id, name, price, description = line.split('|')
            products.append(Product(int(id), name, float(price), description))
    return products

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
        new_user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/product_listing')
def product_listing():
    products = load_products()
    return render_template('product_listing.html', products=products)

@app.route('/shopping_cart')
def shopping_cart():
    return render_template('shopping_cart.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        user = session.get('user')
        selected_products = []  # This should be populated with selected users' cart items
        order = Order(user, selected_products)
        order.save_order()
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8057, debug=False)

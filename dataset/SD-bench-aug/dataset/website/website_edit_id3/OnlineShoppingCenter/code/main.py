from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from product import Product
from cart import Cart
from order import Order

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Load users from users.txt
def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
    except FileNotFoundError:
        pass
    return users

# Load products from products.txt
def load_products():
    products = []
    try:
        with open('products.txt', 'r') as file:
            for line in file:
                id, name, price = line.strip().split('|')
                products.append(Product(int(id), name, float(price)))
    except FileNotFoundError:
        pass
    return products

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['user'] = user.to_dict()  # Store user info in session
            return redirect(url_for('product_listing'))
    return redirect(url_for('login'))  # Redirect back to login if failed

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

@app.route('/shopping_cart', methods=['GET', 'POST'])
def shopping_cart():
    if 'cart' not in session:
        session['cart'] = Cart()  # Initialize cart if not present
    cart = session['cart']
    
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        action = request.form['action']
        if action == 'remove':
            cart.remove_item(product_id)
    
    return render_template('shopping_cart.html', items=cart.view_cart())

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        shipping_address = request.form['shipping_address']
        payment_info = request.form['payment_info']
        user = session.get('user')
        cart = session['cart']
        order = Order(user, cart, shipping_address, payment_info)
        order.save_order()
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    user = session.get('user')
    cart = session.get('cart')
    return render_template('order_confirmation.html', user=user, cart=cart.view_cart())

if __name__ == '__main__':
    app.run(port=8148, debug=True)

from flask import Flask, render_template, request, redirect, session, flash
from user import User
from product import Product
from shopping_cart import ShoppingCart
from order import Order
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

# Load users from the text file
def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
    return users

# Save users to the text file
def save_user(user):
    with open('users.txt', 'a') as file:
        file.write(f"{user.username}|{user.password}|{user.email}\n")

# Load products from the text file
def load_products():
    products = []
    if os.path.exists('products.txt'):
        with open('products.txt', 'r') as file:
            for line in file:
                id, name, price = line.strip().split('|')
                products.append(Product(int(id), name, float(price)))
    return products

# Load shopping cart from session
def load_cart():
    if 'cart' not in session:
        session['cart'] = ShoppingCart()
    return session['cart']

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        users = load_users()
        if any(user.username == username for user in users):
            flash('Username already exists!')
            return redirect('/register')
        new_user = User(username, password, email)
        save_user(new_user)
        flash('Registration successful! Please log in.')
        return redirect('/login')
    return render_template('registration.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                flash('Login successful!')
                return redirect('/products')
        flash('Invalid username or password!')
    return render_template('login.html')

@app.route('/products')
def products():
    if 'username' not in session:
        flash('You need to log in first!')
        return redirect('/login')
    product_list = load_products()
    return render_template('product_listing.html', products=product_list)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'username' not in session:
        flash('You need to log in first!')
        return redirect('/login')
    product_list = load_products()
    product = next((p for p in product_list if p.id == product_id), None)
    if product:
        cart = load_cart()
        cart.add_item(product)
        session['cart'] = cart
        flash(f'Added {product.name} to cart.')
    else:
        flash('Product not found.')
    return redirect('/products')

@app.route('/shopping_cart')
def shopping_cart():
    if 'username' not in session:
        flash('You need to log in first!')
        return redirect('/login')
    cart = load_cart()
    return render_template('shopping_cart.html', cart=cart.get_items())

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'username' not in session:
        flash('You need to log in first!')
        return redirect('/login')
    cart = load_cart()
    cart.remove_item(product_id)
    session['cart'] = cart
    flash('Item removed from cart.')
    return redirect('/shopping_cart')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'username' not in session:
        flash('You need to log in first!')
        return redirect('/login')
    
    cart = load_cart()
    
    if request.method == 'POST':
        shipping_address = request.form['shipping_address']
        payment_info = request.form['payment_info']
        order = Order(user=session['username'], items=cart.get_items(), shipping_address=shipping_address, payment_info=payment_info)
        order.save()
        cart.clear()
        session['cart'] = cart
        flash('Order placed successfully!')
        return redirect('/order_confirmation')
    
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    if 'username' not in session:
        flash('You need to log in first!')
        return redirect('/login')
    return render_template('order_confirmation.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('cart', None)
    flash('You have been logged out.')
    return redirect('/login')

@app.route('/')
def home():
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
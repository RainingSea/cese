from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from product import Product
from cart import Cart
from order import Order

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Load users from the users.txt file
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

# Load products from the products.txt file
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
    user = next((u for u in users if u.username == username and u.password == password), None)
    
    if user:
        session['user'] = user
        return redirect(url_for('product_listing'))
    return redirect(url_for('login'))

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
        session['cart'] = Cart()
    cart = session['cart']
    
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        product = next((p for p in load_products() if p.id == product_id), None)
        if product:
            cart.add_item(product)
        else:
            cart.remove_item(product_id)
    
    return render_template('shopping_cart.html', items=cart.view_cart())

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        shipping_address = request.form['shipping_address']
        payment_info = request.form['payment_info']
        cart = session.get('cart', Cart())
        order = Order(session['user'], cart, shipping_address, payment_info)
        order.save_order()
        return redirect(url_for('order_confirmation', order=order))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    order_details = request.args.get('order')
    return render_template('order_confirmation.html', order_details=order_details)

if __name__ == '__main__':
    app.run(port=8147, debug=True)

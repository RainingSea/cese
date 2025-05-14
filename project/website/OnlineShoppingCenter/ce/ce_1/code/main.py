from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

    def register(self, username, password, email):
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_user, stored_pass, _ = line.strip().split('|')
                if stored_user == username and stored_pass == password:
                    return True
        return False

class ProductManager:
    def __init__(self, products_file='products.txt'):
        self.products_file = products_file
        if not os.path.exists(self.products_file):
            open(self.products_file, 'w').close()

    def get_products(self):
        products = []
        with open(self.products_file, 'r') as f:
            for line in f:
                pid, name, price, desc = line.strip().split('|')
                products.append({
                    'id': pid,
                    'name': name,
                    'price': price,
                    'description': desc
                })
        return products

class CartManager:
    def __init__(self, carts_file='carts.txt'):
        self.carts_file = carts_file
        if not os.path.exists(self.carts_file):
            open(self.carts_file, 'w').close()

    def add_to_cart(self, username, product_id):
        with open(self.carts_file, 'a') as f:
            f.write(f"{username}|{product_id}|1\n")
        return True

    def remove_from_cart(self, username, product_id):
        lines = []
        with open(self.carts_file, 'r') as f:
            for line in f:
                user, pid, _ = line.strip().split('|')
                if not (user == username and pid == product_id):
                    lines.append(line)
        
        with open(self.carts_file, 'w') as f:
            f.writelines(lines)
        return True

    def get_cart(self, username):
        cart = []
        with open(self.carts_file, 'r') as f:
            for line in f:
                user, pid, qty = line.strip().split('|')
                if user == username:
                    cart.append({
                        'product_id': pid,
                        'quantity': qty
                    })
        return cart

class OrderManager:
    def __init__(self, orders_file='orders.txt'):
        self.orders_file = orders_file
        if not os.path.exists(self.orders_file):
            open(self.orders_file, 'w').close()

    def create_order(self, username, cart, shipping_info):
        order_id = len(open(self.orders_file).readlines()) + 1001
        product_ids = ','.join([item['product_id'] for item in cart])
        with open(self.orders_file, 'a') as f:
            f.write(f"{order_id}|{username}|{product_ids}|{shipping_info}\n")
        return order_id

user_manager = UserManager()
product_manager = ProductManager()
cart_manager = CartManager()
order_manager = OrderManager()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('products'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/products')
def products():
    products = product_manager.get_products()
    return render_template('products.html', products=products)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    username = 'user1'  # Simplified for demo
    if request.method == 'POST':
        if 'remove' in request.form:
            product_id = request.form['product_id']
            cart_manager.remove_from_cart(username, product_id)
        elif 'add' in request.form:
            product_id = request.form['product_id']
            cart_manager.add_to_cart(username, product_id)
    cart_items = cart_manager.get_cart(username)
    products = product_manager.get_products()
    cart_with_details = []
    for item in cart_items:
        for product in products:
            if product['id'] == item['product_id']:
                cart_with_details.append({
                    'product': product,
                    'quantity': item['quantity']
                })
    return render_template('cart.html', cart=cart_with_details)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    username = 'user1'  # Simplified for demo
    if request.method == 'POST':
        shipping_info = f"{request.form['address']},{request.form['city']},{request.form['country']}"
        cart = cart_manager.get_cart(username)
        order_id = order_manager.create_order(username, cart, shipping_info)
        return redirect(url_for('confirmation', order_id=order_id))
    return render_template('checkout.html')

@app.route('/confirmation')
def confirmation():
    order_id = request.args.get('order_id')
    return render_template('confirmation.html', order_id=order_id)

if __name__ == '__main__':
    app.run(port=8019, debug=False)

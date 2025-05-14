from flask import Flask, render_template, request, redirect, url_for, session
import json
import time
import os

app = Flask(__name__)
app.secret_key = 'demo_secret_key'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

    def validate_user(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2 and parts[0] == username and parts[1] == password:
                    return True
        return False

    def register_user(self, username, password, email):
        if not username or not password or not email:
            return False
        
        with open(self.users_file, 'a+') as f:
            f.seek(0)
            for line in f:
                if line.startswith(username + '|'):
                    return False
            f.write(f"{username}|{password}|{email}\n")
        return True

class ProductCatalog:
    def __init__(self, products_file='products.txt'):
        self.products_file = products_file
        if not os.path.exists(self.products_file):
            open(self.products_file, 'w').close()

    def get_products(self):
        products = []
        with open(self.products_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    products.append({
                        'id': parts[0],
                        'name': parts[1],
                        'price': float(parts[2]),
                        'description': parts[3]
                    })
        return products

    def get_product(self, product_id):
        with open(self.products_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4 and parts[0] == product_id:
                    return {
                        'id': parts[0],
                        'name': parts[1],
                        'price': float(parts[2]),
                        'description': parts[3]
                    }
        return None

class OrderProcessor:
    def __init__(self, orders_file='orders.txt'):
        self.orders_file = orders_file
        if not os.path.exists(self.orders_file):
            open(self.orders_file, 'w').close()

    def create_order(self, username, items, total):
        order_id = str(int(time.time()))
        with open(self.orders_file, 'a') as f:
            f.write(f"{order_id}|{username}|{json.dumps(items)}|{total}|{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        return order_id

user_manager = UserManager()
product_catalog = ProductCatalog()
order_processor = OrderProcessor()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if user_manager.validate_user(username, password):
            session['username'] = username
            return redirect(url_for('products'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if user_manager.register_user(username, password, email):
            return redirect(url_for('login'))
        return render_template('register.html', error='Registration failed')
    return render_template('register.html')

@app.route('/products')
def products():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('products.html', products=product_catalog.get_products())

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 'cart' not in session:
        session['cart'] = {}
    
    if request.method == 'POST':
        action = request.form.get('action')
        product_id = request.form.get('product_id')
        
        if action == 'add':
            product = product_catalog.get_product(product_id)
            if product:
                if product_id in session['cart']:
                    session['cart'][product_id]['quantity'] += 1
                else:
                    session['cart'][product_id] = {
                        'name': product['name'],
                        'price': product['price'],
                        'quantity': 1
                    }
                session.modified = True
        elif action == 'remove':
            if product_id in session['cart']:
                del session['cart'][product_id]
                session.modified = True
    
    cart_items = []
    total = 0.0
    for product_id, item in session.get('cart', {}).items():
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity']
        })
        total += item['price'] * item['quantity']
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'username' not in session or 'cart' not in session or not session['cart']:
        return redirect(url_for('products'))
    
    if request.method == 'POST':
        shipping_address = request.form.get('shipping_address')
        payment_info = request.form.get('payment_info')
        
        if not shipping_address or not payment_info:
            return render_template('checkout.html', error='Please fill all fields')
        
        items = []
        total = 0.0
        for product_id, item in session['cart'].items():
            items.append({
                'product_id': product_id,
                'name': item['name'],
                'price': item['price'],
                'quantity': item['quantity']
            })
            total += item['price'] * item['quantity']
        
        order_id = order_processor.create_order(session['username'], items, total)
        session.pop('cart', None)
        return redirect(url_for('confirm', order_id=order_id))
    
    total = 0.0
    for item in session['cart'].values():
        total += item['price'] * item['quantity']
    
    return render_template('checkout.html', total=total)

@app.route('/confirm/<order_id>')
def confirm(order_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    with open('orders.txt', 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 5 and parts[0] == order_id and parts[1] == session['username']:
                return render_template('confirm.html', 
                    order_id=order_id,
                    items=json.loads(parts[2]),
                    total=float(parts[3]),
                    timestamp=parts[4]
                )
    
    return redirect(url_for('products'))

if __name__ == '__main__':
    app.run(port=8020, debug=False)

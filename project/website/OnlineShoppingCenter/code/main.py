from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self) -> dict:
        users = {}
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password, email = line.strip().split(',')
                users[username] = {'password': password, 'email': email}
        return users

    def register(self, username: str, password: str, email: str) -> bool:
        if username not in self.users:
            self.users[username] = {'password': password, 'email': email}
            with open(self.users_file, 'a') as file:
                file.write(f"{username},{password},{email}\n")
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        return user is not None and user['password'] == password

    def get_user_data(self, username: str) -> dict:
        user = self.users.get(username)
        if user:
            return {'username': username, 'email': user['email']}
        return {}

class ProductManager:
    def __init__(self, products_file: str):
        self.products_file = products_file
        self.products = self.load_products()

    def load_products(self) -> list:
        products = []
        with open(self.products_file, 'r') as file:
            for line in file:
                product_data = line.strip().split(',')
                products.append({'id': product_data[0], 'name': product_data[1], 'price': float(product_data[2])})
        return products

    def get_all_products(self) -> list:
        return self.products

class OrderManager:
    def __init__(self, orders_file: str):
        self.orders_file = orders_file
        self.order_id_counter = self.load_order_id_counter()

    def load_order_id_counter(self) -> int:
        if os.path.exists(self.orders_file):
            with open(self.orders_file, 'r') as file:
                lines = file.readlines()
                if lines:
                    last_order = lines[-1].strip().split(',')
                    return int(last_order[0]) + 1
        return 1

    def create_order(self, username: str, cart: dict) -> bool:
        total_price = 0
        with open(self.orders_file, 'a') as file:
            for product_id, quantity in cart.items():
                product = next((p for p in product_manager.get_all_products() if p['id'] == product_id), None)
                if product:
                    total_price += quantity * product['price']
                    file.write(f"{self.order_id_counter},{username},{product_id},{quantity},{total_price}\n")
            self.order_id_counter += 1
        return True

    def get_order_summary(self, order_id: str) -> dict:
        with open(self.orders_file, 'r') as file:
            for line in file:
                order_data = line.strip().split(',')
                if order_data[0] == order_id:
                    return {'order_id': order_data[0], 'username': order_data[1], 'product_id': order_data[2], 'quantity': order_data[3], 'total_price': order_data[4]}
        return {}

user_manager = UserManager('users.txt')
product_manager = ProductManager('products.txt')
order_manager = OrderManager('orders.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('product_listing'))
    return redirect(url_for('login'))

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
    if 'username' not in session:
        return redirect(url_for('login'))
    products = product_manager.get_all_products()
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    if 'cart' not in session:
        session['cart'] = {}
    if product_id in session['cart']:
        session['cart'][product_id] += 1
    else:
        session['cart'][product_id] = 1
    return redirect(url_for('product_listing'))

@app.route('/remove_from_cart/<product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    if 'cart' in session and product_id in session['cart']:
        del session['cart'][product_id]
    return redirect(url_for('shopping_cart'))

@app.route('/shopping_cart')
def shopping_cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    cart = session.get('cart', {})
    return render_template('shopping_cart.html', cart=cart)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = session.get('username')
        order_created = order_manager.create_order(username, session.get('cart', {}))
        session.pop('cart', None)
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8373, debug=False)

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Order:
    def __init__(self, user, items):
        self.user = user
        self.items = items

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str, email: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        self.users.append(User(username, password, email))
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return True
        return False

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}|{user.email}\n")

class ProductManager:
    def __init__(self):
        self.products = self.load_products()

    def load_products(self):
        products = []
        try:
            with open('products.txt', 'r') as file:
                for line in file:
                    name, price = line.strip().split('|')
                    products.append(Product(name, float(price)))
        except FileNotFoundError:
            pass
        return products

    def get_products(self):
        return self.products

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product: Product):
        self.items.append(product)

    def remove_item(self, product: Product):
        self.items.remove(product)

    def get_items(self):
        return self.items

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.product_manager = ProductManager()
        self.order_manager = []

    def main(self):
        app.run(port=8208, debug=False)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if Main().user_manager.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/product_listing')
def product_listing():
    products = Main().product_manager.get_products()
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart/<product_name>')
def add_to_cart(product_name):
    product = next((p for p in Main().product_manager.get_products() if p.name == product_name), None)
    if product:
        cart = session.get('cart', ShoppingCart())
        cart.add_item(product)
        session['cart'] = cart
    return redirect(url_for('product_listing'))

@app.route('/shopping_cart')
def shopping_cart():
    cart = session.get('cart', ShoppingCart())
    return render_template('shopping_cart.html', items=cart.get_items())

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Process checkout logic here
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    Main().main()
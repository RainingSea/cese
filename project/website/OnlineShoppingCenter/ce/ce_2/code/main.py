from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
        return users

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class ProductManager:
    def __init__(self):
        self.products = self.load_products()

    def load_products(self) -> list:
        products = []
        with open('products.txt', 'r') as file:
            for line in file:
                products.append(line.strip())
        return products

class CartManager:
    def __init__(self):
        self.cart = self.load_cart()

    def load_cart(self) -> dict:
        cart = {}
        try:
            with open('cart.txt', 'r') as file:
                for line in file:
                    product_id, quantity = line.strip().split('|')
                    cart[product_id] = int(quantity)
        except FileNotFoundError:
            pass
        return cart

    def add_to_cart(self, product_id: str) -> None:
        if product_id in self.cart:
            self.cart[product_id] += 1
        else:
            self.cart[product_id] = 1
        self.save_cart()

    def remove_from_cart(self, product_id: str) -> None:
        if product_id in self.cart:
            del self.cart[product_id]
            self.save_cart()

    def view_cart(self) -> dict:
        return self.cart

    def save_cart(self) -> None:
        with open('cart.txt', 'w') as file:
            for product_id, quantity in self.cart.items():
                file.write(f"{product_id}|{quantity}\n")

app = Flask(__name__)

user_manager = UserManager()
product_manager = ProductManager()
cart_manager = CartManager()

@app.route('/')
def login():
    return render_template('login.html')

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
    products = product_manager.products
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    cart_manager.add_to_cart(product_id)
    return redirect(url_for('product_listing'))

@app.route('/shopping_cart')
def shopping_cart():
    cart = cart_manager.view_cart()
    return render_template('shopping_cart.html', cart=cart)

@app.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    cart_manager.remove_from_cart(product_id)
    return redirect(url_for('shopping_cart'))

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    # Here we would process the order
    return redirect(url_for('order_confirmation'))

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8372, debug=False)

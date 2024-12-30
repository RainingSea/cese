from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load(username: str) -> 'User':
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1], user_data[2])
        return None

class Product:
    def __init__(self, id: int, name: str, price: float, description: str):
        self.id = id
        self.name = name
        self.price = price
        self.description = description

    @staticmethod
    def load_all() -> list:
        products = []
        with open('products.txt', 'r') as file:
            for line in file:
                product_data = line.strip().split('|')
                product = Product(int(product_data[0]), product_data[1], float(product_data[2]), product_data[3])
                products.append(product)
        return products

class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, product: Product) -> None:
        if product.id in self.items:
            self.items[product.id]['quantity'] += 1
        else:
            self.items[product.id] = {'product': product, 'quantity': 1}

    def remove_item(self, product_id: int) -> None:
        if product_id in self.items:
            del self.items[product_id]

    def view_cart(self) -> dict:
        return self.items

class Order:
    def __init__(self, user: User, items: dict, shipping_address: str, payment_info: str):
        self.user = user
        self.items = items
        self.shipping_address = shipping_address
        self.payment_info = payment_info

    def save(self) -> None:
        with open('orders.txt', 'a') as file:
            order_data = {
                'username': self.user.username,
                'items': self.items,
                'shipping_address': self.shipping_address,
                'payment_info': self.payment_info
            }
            file.write(json.dumps(order_data) + '\n')

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

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    user = User.load(username)
    if user and user.password == password:
        session['username'] = user.username
        session['shopping_cart'] = ShoppingCart()  # Initialize shopping cart
        return redirect(url_for('product_listing'))
    return redirect(url_for('login'))

@app.route('/product_listing')
def product_listing():
    products = Product.load_all()
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form['product_id'])
    product = next((p for p in Product.load_all() if p.id == product_id), None)
    if product:
        session['shopping_cart'].add_item(product)
    return redirect(url_for('product_listing'))

@app.route('/shopping_cart')
def shopping_cart():
    cart = session.get('shopping_cart', ShoppingCart())
    return render_template('shopping_cart.html', cart=cart.view_cart())

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('shopping_cart', ShoppingCart())
    cart.remove_item(product_id)
    return redirect(url_for('shopping_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        shipping_address = request.form['shipping_address']
        payment_info = request.form['payment_info']
        user = User.load(session['username'])
        cart = session.get('shopping_cart', ShoppingCart())
        order = Order(user, cart.view_cart(), shipping_address, payment_info)
        order.save()
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
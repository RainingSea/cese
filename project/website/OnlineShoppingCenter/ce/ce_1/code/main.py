from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load_all():
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users

class Product:
    def __init__(self, id: int, name: str, price: float, description: str):
        self.id = id
        self.name = name
        self.price = price
        self.description = description

    @staticmethod
    def load_all():
        products = []
        try:
            with open('products.txt', 'r') as f:
                for line in f:
                    id, name, price, description = line.strip().split('|')
                    products.append(Product(int(id), name, float(price), description))
        except FileNotFoundError:
            pass
        return products

class Order:
    def __init__(self, user_id: str, items: list, total: float):
        self.user_id = user_id
        self.items = items
        self.total = total

    def save(self):
        with open('orders.txt', 'a') as f:
            f.write(f"{self.user_id}|{json.dumps(self.items)}|{self.total}\n")

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
    products = Product.load_all()
    return render_template('product_listing.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    return redirect(url_for('product_listing'))

@app.route('/shopping_cart')
def shopping_cart():
    cart = session.get('cart', [])
    products = Product.load_all()
    cart_items = [product for product in products if product.id in cart]
    return render_template('shopping_cart.html', cart_items=cart_items)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        user_id = session.get('user_id', 'guest')
        items = session.get('cart', [])
        total = sum(Product.load_all()[item - 1].price for item in items)
        order = Order(user_id, items, total)
        order.save()
        session.pop('cart', None)
        return redirect(url_for('order_confirmation'))
    return render_template('checkout.html')

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(port=8670, debug=False)

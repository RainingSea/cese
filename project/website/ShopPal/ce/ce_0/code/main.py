from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from product_manager import ProductManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'

user_manager = UserManager()
product_manager = ProductManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        product_info = {
            'id': request.form['product_id'],
            'description': request.form['description'],
            'reviews': request.form['reviews'],
            'price': request.form['price']
        }
        product_manager.add_product(product_info)
    return render_template('dashboard.html', collections=product_manager.collections)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    user_manager.load_users()
    product_manager.load_products()
    product_manager.load_collections()
    app.run(port=8410, debug=False)

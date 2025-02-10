from flask import Flask, render_template, redirect, request, session
from UserManager import UserManager
from ProductManager import ProductManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
product_manager = ProductManager('products.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    
    user = user_manager.load(session['username'])
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_description = request.form['product_description']
        product_price = float(request.form['product_price'])
        product_manager.add_product(user, product_name, product_description, product_price)

    products = product_manager.get_products(user)
    return render_template('dashboard.html', products=products)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8695, debug=False)

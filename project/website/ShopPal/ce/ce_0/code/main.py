from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from ProductManager import ProductManager
from CollectionManager import CollectionManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
product_manager = ProductManager('products.txt')
collection_manager = CollectionManager('collections.txt')

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
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session:
        collections = collection_manager.load_collection(session['username'])
        return render_template('dashboard.html', collections=collections)
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/product/<product_id>')
def product_detail(product_id):
    product = product_manager.get_product_details(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8692, debug=False)

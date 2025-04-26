from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from user_manager import UserManager
from product_manager import ProductManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
            return redirect('/')
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_description = request.form['product_description']
        product_price = float(request.form['product_price'])
        product_manager.add_product(product_name, product_description, product_price)

    user_collections = user_manager.get_user_collections(session['username'])
    return render_template('dashboard.html', collections=user_collections)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8240, debug=False)

from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from UserManager import UserManager
from WishlistManager import WishlistManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager('users.txt')
wishlist_manager = WishlistManager('wishlist.txt')

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register(username, password):
        return redirect('/')
    return "Registration failed", 400

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/dashboard')
    return "Login failed", 400

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    wishlist_items = wishlist_manager.view_wishlist(session['username'])
    return render_template('dashboard.html', items=wishlist_items)

@app.route('/add_item', methods=['POST'])
def add_item():
    if 'username' not in session:
        return redirect('/')
    item_name = request.form['item_name']
    description = request.form['description']
    price = float(request.form['price'])
    wishlist_manager.add_item(session['username'], item_name, description, price)
    return redirect('/dashboard')

@app.route('/remove_item', methods=['POST'])
def remove_item():
    if 'username' not in session:
        return redirect('/')
    item_name = request.form['item_name']
    wishlist_manager.remove_item(session['username'], item_name)
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(port=8459, debug=False)

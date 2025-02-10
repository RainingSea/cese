from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from wishlist_manager import WishlistManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
user_manager = UserManager('users.txt')
wishlist_manager = WishlistManager('wishlist_')

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

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    if request.method == 'POST':
        item_name = request.form['item_name']
        description = request.form['description']
        desired_price = float(request.form['desired_price'])
        wishlist_manager.add_item(username, item_name, description, desired_price)
    
    wishlist_items = wishlist_manager.view_wishlist(username)
    return render_template('dashboard.html', items=wishlist_items)

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
    app.run(port=8701, debug=False)

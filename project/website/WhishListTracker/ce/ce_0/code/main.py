from flask import Flask, render_template, request, redirect, url_for, session
from user import User, UserController
from wishlist import WishlistItem, WishlistController

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_controller = UserController()
wishlist_controller = WishlistController()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_controller.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'add_item' in request.form:
            name = request.form['name']
            description = request.form['description']
            price = float(request.form['price'])
            wishlist_controller.add_item(name, description, price)

    items = wishlist_controller.view_items()
    return render_template('dashboard.html', items=items)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8698, debug=False)

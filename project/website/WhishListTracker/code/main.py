from flask import Flask, render_template, request, redirect, url_for, flash, session
from user_manager import UserManager
from wishlist_manager import WishlistManager
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a random secret key for security
user_manager = UserManager('users.txt')
wishlist_manager = WishlistManager('wishlist.txt')

@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login_page'))
        else:
            flash('Username already exists.')
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        description = request.form.get('description')
        desired_price = request.form.get('desired_price')

        if not item_name or not description or not desired_price:
            flash('All fields are required.')
        else:
            try:
                desired_price = float(desired_price)
                if 'remove_item' in request.form:
                    if wishlist_manager.remove_item(item_name):
                        flash('Item removed from wishlist.')
                    else:
                        flash('Item not found in wishlist.')
                else:
                    if wishlist_manager.add_item(item_name, description, desired_price):
                        flash('Item added to wishlist.')
                    else:
                        flash('Item already exists in wishlist.')
            except ValueError:
                flash('Desired price must be a valid number.')

    items = wishlist_manager.view_items()
    return render_template('dashboard.html', items=items)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(port=8461, debug=False)

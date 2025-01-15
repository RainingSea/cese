from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from wishlist_item import WishlistItem

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.load_users()
        if any(user.username == username for user in users):
            return "Username is already taken", 400
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Displays the dashboard and handles wishlist item management."""
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_description = request.form['item_description']
        item_price = float(request.form['item_price'])
        new_item = WishlistItem(item_name, item_description, item_price)
        new_item.save()
        return redirect(url_for('dashboard'))  # Redirect after POST to avoid resubmission
    items = WishlistItem.load_items()
    return render_template('dashboard.html', items=items)

@app.route('/remove_item/<string:item_name>', methods=['POST'])
def remove_item(item_name):
    """Removes an item from the wishlist."""
    WishlistItem.remove_item(item_name)
    return redirect(url_for('dashboard'))

@app.route('/update_item/<string:item_name>', methods=['POST'])
def update_item(item_name):
    """Updates an existing wishlist item."""
    new_description = request.form['item_description']
    new_price = float(request.form['item_price'])
    WishlistItem.update_item(item_name, new_description, new_price)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    """Logs out the user."""
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8564, debug=False)

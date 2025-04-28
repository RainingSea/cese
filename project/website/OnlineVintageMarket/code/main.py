from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from item_manager import ItemManager
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
user_manager = UserManager('users.txt')
item_manager = ItemManager('items.txt')

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username  # Store username in session
        logging.info(f"User '{username}' logged in successfully.")
        return redirect(url_for('home'))
    logging.warning(f"Failed login attempt for user '{username}'.")
    return render_template('login.html', error="Invalid username or password.")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            logging.info(f"User '{username}' registered successfully.")
            return redirect(url_for('login'))
        logging.warning(f"Registration failed: Username '{username}' already exists.")
        return render_template('registration.html', error="Username already exists.")
    return render_template('registration.html')

@app.route('/home', methods=['GET'])
def home():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    items = item_manager.get_items()
    return render_template('home.html', items=items)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    if request.method == 'POST':
        item_name = request.form['item_name']
        description = request.form['description']
        price = float(request.form['price'])
        if item_manager.add_item(item_name, description, price):
            logging.info(f"Item '{item_name}' added successfully.")
            return redirect(url_for('home'))
        logging.warning(f"Failed to add item '{item_name}'.")
    return render_template('listing.html')

@app.route('/item/<item_name>', methods=['GET'])
def item_details(item_name):
    details = item_manager.get_item_details(item_name)
    if not details:
        logging.warning(f"Item '{item_name}' not found.")
        return redirect(url_for('home'))
    return render_template('item_details.html', details=details)

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    logging.info("User logged out successfully.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8381, debug=False)

from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_users()

    def load_users(self):
        """Load users from the specified file."""
        self.users = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        """Register a new user if the username does not already exist."""
        if self.user_exists(username):
            return False
        self.users[username] = password
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        """Check if the provided credentials are valid."""
        return self.users.get(username) == password

    def user_exists(self, username: str) -> bool:
        """Check if a user exists."""
        return username in self.users

class WishlistManager:
    def __init__(self, username: str):
        self.filename = f'wishlist_{username}.txt'
        self.load_items()

    def load_items(self):
        """Load wishlist items from the user's file."""
        self.items = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    item_name, description, desired_price = line.strip().split('|')
                    self.items.append({
                        'item_name': item_name,
                        'description': description,
                        'desired_price': float(desired_price)
                    })

    def add_item(self, item_name: str, description: str, price: float) -> bool:
        """Add a new item to the wishlist."""
        self.items.append({'item_name': item_name, 'description': description, 'desired_price': price})
        with open(self.filename, 'a') as file:
            file.write(f"{item_name}|{description}|{price}\n")
        return True

    def view_items(self) -> list:
        """Return the list of items in the wishlist."""
        return self.items

    def update_item(self, old_name: str, new_name: str, new_description: str, new_price: float) -> bool:
        """Update an existing item in the wishlist."""
        for item in self.items:
            if item['item_name'] == old_name:
                item['item_name'] = new_name
                item['description'] = new_description
                item['desired_price'] = new_price
                self.save_items()
                return True
        return False

    def remove_item(self, item_name: str) -> bool:
        """Remove an item from the wishlist."""
        original_length = len(self.items)
        self.items = [item for item in self.items if item['item_name'] != item_name]
        if len(self.items) < original_length:
            self.save_items()
            return True
        return False

    def save_items(self):
        """Save the current wishlist items to the file."""
        with open(self.filename, 'w') as file:
            for item in self.items:
                file.write(f"{item['item_name']}|{item['description']}|{item['desired_price']}\n")

@app.route('/')
def login():
    """Render the login page."""
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            flash("Username already exists!", "error")
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Render the dashboard for logged-in users."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    wishlist_manager = WishlistManager(session['username'])
    
    if request.method == 'POST':
        if 'add_item' in request.form:
            item_name = request.form['item_name']
            description = request.form['description']
            price = float(request.form['desired_price'])
            wishlist_manager.add_item(item_name, description, price)
        elif 'update_item' in request.form:
            old_name = request.form['old_name']
            new_name = request.form['new_name']
            new_description = request.form['new_description']
            new_price = float(request.form['new_price'])
            wishlist_manager.update_item(old_name, new_name, new_description, new_price)
        elif 'remove_item' in request.form:
            item_name = request.form['item_name']
            wishlist_manager.remove_item(item_name)

    items = wishlist_manager.view_items()
    return render_template('dashboard.html', items=items)

@app.route('/do_login', methods=['POST'])
def do_login():
    """Handle user login."""
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    flash("Invalid credentials!", "error")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """Log out the user."""
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    user_manager = UserManager('users.txt')
    app.run(port=8289, debug=False)

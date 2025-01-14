from flask import Flask, render_template, request, redirect, session, flash
from user_manager import UserManager
from item_manager import ItemManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
user_manager = UserManager()
item_manager = ItemManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = user_manager.find_user(username)
        if user and user.validate_password(password):
            session['username'] = username
            return redirect('/home')
        else:
            flash('Invalid username or password. Please try again.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if user_manager.find_user(username):
            flash('Username already exists. Please choose a different one.')
        else:
            user_manager.add_user(username, password)
            return redirect('/')
    return render_template('register.html')

@app.route('/home')
def home():
    """Render home page with available items."""
    items = item_manager.items
    if not items:
        flash('No items available at the moment.')
    return render_template('home.html', items=items)

@app.route('/item/<name>')
def item_details(name):
    """Render details of a specific item."""
    item = item_manager.find_item(name)
    if not item:
        flash('Item not found.')
        return redirect('/home')
    return render_template('item_details.html', item=item)

@app.route('/listing', methods=['GET', 'POST'])
def create_listing():
    """Handle item listing creation."""
    if 'username' not in session:
        flash('You must be logged in to create a listing.')
        return redirect('/')
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        if price.isdigit() or (price.replace('.', '', 1).isdigit() and price.count('.') < 2):
            item_manager.add_item(name, description, float(price))
            return redirect('/home')
        else:
            flash('Invalid price. Please enter a valid number.')
    return render_template('listing.html')

@app.route('/search', methods=['GET'])
def search_items():
    """Handle item search by name."""
    query = request.args.get('query', '')
    items = item_manager.search_items(query)
    return render_template('home.html', items=items)

if __name__ == '__main__':
    user_manager.load_users()
    item_manager.load_items()
    app.run(port=8470, debug=False)

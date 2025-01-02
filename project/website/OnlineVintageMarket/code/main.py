from flask import Flask, render_template, request, redirect, url_for, flash
from user_manager import User, UserManager
from item_manager import Item, ItemManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

user_manager = UserManager()
item_manager = ItemManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.authenticate(username, password):
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.add_user(User(username, password))
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    items = item_manager.get_items()
    search_query = request.form.get('search_query')
    if search_query:
        items = [item for item in items if search_query.lower() in item.name.lower()]
    return render_template('home.html', items=items)

@app.route('/create_item', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        item_manager.add_item(Item(name, description, price))
        flash('Item created successfully!')
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/item/<item_name>')
def item_details(item_name):
    item = item_manager.search_item(item_name)
    return render_template('item_details.html', item=item)

if __name__ == '__main__':
    user_manager.load_users()
    item_manager.load_items()
    app.run(port=8183, debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
from user_manager import UserManager
from item_manager import ItemManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
user_manager = UserManager()
item_manager = ItemManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists')
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_query = request.form['search_query']
        items = item_manager.search_item(search_query)
        return render_template('home.html', items=items)
    items = item_manager.get_all_items()
    return render_template('home.html', items=items)

@app.route('/item/<int:item_id>')
def item_details(item_id):
    item = item_manager.get_item_by_id(item_id)
    return render_template('item_details.html', item=item)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        item_manager.create_listing(name, description, price)
        flash('Item listing created successfully!')
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/navigation')
def navigation():
    return render_template('navigation.html')

if __name__ == '__main__':
    user_manager.load_users()
    item_manager.load_items()
    app.run(debug=True)
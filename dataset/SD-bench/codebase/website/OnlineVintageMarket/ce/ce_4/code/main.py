from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from ItemManager import ItemManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a more secure key in production

user_manager = UserManager('users.txt')
item_manager = ItemManager('items.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register_user(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form['search']
        items = item_manager.search_items(query)
    else:
        items = item_manager.load_items()
    return render_template('home.html', items=items)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        item_manager.add_item(Item(name, description, price))
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/item/<int:item_id>')
def item_details(item_id):
    items = item_manager.load_items()
    item = items[item_id] if item_id < len(items) else None
    return render_template('item_details.html', item=item)

if __name__ == '__main__':
    app.run(port=8469, debug=False)

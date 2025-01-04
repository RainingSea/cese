from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from item_manager import ItemManager, Item

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
item_manager = ItemManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/home')
def home():
    items = item_manager.get_items()
    return render_template('home.html', items=items)

@app.route('/item/<string:name>')
def item_details(name):
    item = item_manager.get_item_details(name)
    return render_template('item_details.html', item=item)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        item_name = request.form['name']
        item_description = request.form['description']
        item_price = float(request.form['price'])
        new_item = Item(item_name, item_description, item_price)
        item_manager.add_item(new_item)
        return redirect(url_for('home'))
    return render_template('listing.html')

if __name__ == '__main__':
    user_manager.load_users()
    item_manager.load_items()
    app.run(debug=True)
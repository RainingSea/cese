from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from item_manager import ItemManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
user_manager = UserManager()
item_manager = ItemManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    items = item_manager.get_items()
    return render_template('home.html', items=items)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/item/<name>', methods=['GET'])
def item_details(name):
    if 'username' not in session:
        return redirect(url_for('login'))
    item = item_manager.get_item_details(name)
    return render_template('item_details.html', item=item)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        new_item = Item(name, description, price)
        item_manager.add_item(new_item)
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    user_manager.load_users()
    item_manager.load_items()
    app.run(debug=True)
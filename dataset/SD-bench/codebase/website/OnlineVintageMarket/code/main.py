from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from item import Item

app = Flask(__name__)
app.secret_key = 'supersecretkey'
users = User().load_users()
items = Item().load_items()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User()
    if user.authenticate(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('login.html', error='Invalid credentials.')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User().register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    items = Item().load_items()  # Ensure we load items each time
    return render_template('home.html', items=items)

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        Item().add_item(name, description, price)
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/item/<name>')
def item_details(name):
    item = Item().search_item(name)
    return render_template('item_details.html', item=item)

if __name__ == '__main__':
    app.run(port=8309, debug=False)

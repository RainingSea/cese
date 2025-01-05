from flask import Flask, render_template, request, redirect, session
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
            return redirect('/')
    return render_template('register.html')

@app.route('/home')
def home():
    items = item_manager.load_items()
    return render_template('home.html', items=items)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/home')
    return redirect('/')

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        item_manager.add_item(name, description, price)
        return redirect('/home')
    return render_template('listing.html')

@app.route('/item/<item_name>')
def item_details(item_name):
    item = item_manager.search_item(item_name)
    return render_template('item_details.html', item=item)

if __name__ == '__main__':
    app.run(port=8101, debug=False)

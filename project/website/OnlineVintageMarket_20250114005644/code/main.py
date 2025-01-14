from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from item import Item

app = Flask(__name__)
app.secret_key = 'supersecretkey'
users = User.load_users()
items = Item.load_items()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in users if user.username == username and user.password == password), None)
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', items=items)

@app.route('/item/<name>', methods=['GET'])
def item_details(name):
    item = next((item for item in items if item.name == name), None)
    if item is None:
        return "Item not found", 404
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
        new_item.save()
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    filtered_items = [item for item in items if query.lower() in item.name.lower()]
    return render_template('search_results.html', items=filtered_items, query=query)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8460, debug=False)

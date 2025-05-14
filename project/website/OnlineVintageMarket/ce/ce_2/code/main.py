from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file

    def register(self, username, password):
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_user, stored_pass = line.strip().split('|')
                if stored_user == username and stored_pass == password:
                    return True
        return False

class ItemManager:
    def __init__(self, items_file='items.txt'):
        self.items_file = items_file

    def get_items(self):
        items = []
        with open(self.items_file, 'r') as f:
            for line in f:
                item_id, title, description, price, seller = line.strip().split('|')
                items.append({
                    'id': item_id,
                    'title': title,
                    'description': description,
                    'price': price,
                    'seller': seller
                })
        return items

    def search_items(self, query):
        items = self.get_items()
        return [item for item in items if query.lower() in item['title'].lower()]

    def add_item(self, title, description, price, seller):
        items = self.get_items()
        new_id = str(len(items) + 1)
        with open(self.items_file, 'a') as f:
            f.write(f"{new_id}|{title}|{description}|{price}|{seller}\n")
        return True

    def get_item_details(self, item_id):
        items = self.get_items()
        for item in items:
            if item['id'] == item_id:
                return item
        return None

user_manager = UserManager()
item_manager = ItemManager()

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    items = item_manager.get_items()
    return render_template('home.html', items=items, username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/listing', methods=['GET', 'POST'])
def listing():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        item_manager.add_item(title, description, price, session['username'])
        return redirect(url_for('home'))
    return render_template('listing.html')

@app.route('/item/<item_id>')
def item_details(item_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    item = item_manager.get_item_details(item_id)
    if not item:
        return redirect(url_for('home'))
    return render_template('item_details.html', item=item)

@app.route('/search')
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    query = request.args.get('q', '')
    items = item_manager.search_items(query)
    return render_template('home.html', items=items, username=session['username'], search_query=query)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8115, debug=False)

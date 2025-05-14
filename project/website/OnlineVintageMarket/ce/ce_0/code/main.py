from flask import Flask, render_template, request, redirect, url_for, session
import json
import time
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class FileStorage:
    @staticmethod
    def read_users():
        users = {}
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users[username] = {'password': password, 'email': email}
        except FileNotFoundError:
            pass
        return users

    @staticmethod
    def write_user(username, data):
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{data['password']}|{data['email']}\n")
        return True

    @staticmethod
    def read_items():
        items = []
        try:
            with open('items.txt', 'r') as f:
                for line in f:
                    items.append(json.loads(line.strip()))
        except FileNotFoundError:
            pass
        return items

    @staticmethod
    def write_item(item):
        with open('items.txt', 'a') as f:
            f.write(json.dumps(item) + '\n')
        return True

    @staticmethod
    def add_session(username):
        with open('sessions.txt', 'a') as f:
            f.write(f"{username}|{time.time()}\n")

    @staticmethod
    def remove_session(username):
        sessions = []
        try:
            with open('sessions.txt', 'r') as f:
                for line in f:
                    user, _ = line.strip().split('|')
                    if user != username:
                        sessions.append(line)
        except FileNotFoundError:
            pass
        
        with open('sessions.txt', 'w') as f:
            f.writelines(sessions)

class OnlineVintageMarket:
    def __init__(self):
        self.storage = FileStorage()
        self.current_user = None

    def login(self, username, password):
        users = self.storage.read_users()
        if username in users and users[username]['password'] == password:
            self.current_user = username
            self.storage.add_session(username)
            return True
        return False

    def register(self, username, password, email):
        users = self.storage.read_users()
        if username in users:
            return False
        self.storage.write_user(username, {'password': password, 'email': email})
        return True

    def add_item(self, name, description, price):
        item_id = f"{int(time.time())}{random.randint(100,999)}"
        item = {
            'id': item_id,
            'name': name,
            'description': description,
            'price': float(price),
            'seller': self.current_user
        }
        return self.storage.write_item(item)

    def search_items(self, query):
        items = self.storage.read_items()
        if not query:
            return items
        return [item for item in items if query.lower() in item['name'].lower() or 
                query.lower() in item['description'].lower()]

    def get_item_details(self, item_id):
        items = self.storage.read_items()
        for item in items:
            if item['id'] == item_id:
                return item
        return None

market = OnlineVintageMarket()

@app.route('/')
def login_route():
    if 'username' in session:
        return redirect(url_for('home_route'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    if market.login(username, password):
        session['username'] = username
        return redirect(url_for('home_route'))
    return redirect(url_for('login_route'))

@app.route('/register')
def register_route():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    if market.register(username, password, email):
        return redirect(url_for('login_route'))
    return redirect(url_for('register_route'))

@app.route('/home')
def home_route():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    query = request.args.get('query', '')
    items = market.search_items(query)
    return render_template('home.html', items=items)

@app.route('/listing')
def listing_route():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    return render_template('listing.html')

@app.route('/listing', methods=['POST'])
def listing_post():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    market.add_item(name, description, price)
    return redirect(url_for('home_route'))

@app.route('/item/<item_id>')
def item_route(item_id):
    if 'username' not in session:
        return redirect(url_for('login_route'))
    item = market.get_item_details(item_id)
    if not item:
        return redirect(url_for('home_route'))
    return render_template('item.html', item=item)

@app.route('/logout')
def logout():
    if 'username' in session:
        market.storage.remove_session(session['username'])
        session.pop('username', None)
    return redirect(url_for('login_route'))

if __name__ == '__main__':
    app.run(port=8113, debug=False)

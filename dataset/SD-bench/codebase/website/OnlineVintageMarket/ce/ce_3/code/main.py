from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from item import Item

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class App:
    def __init__(self):
        self.users = User.load_all()
        self.items = Item.load_all()

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def add_item(self, name: str, description: str, price: float) -> None:
        new_item = Item(name, description, price)
        new_item.save()
        self.items.append(new_item)

    def search_items(self, query: str) -> list:
        return [item for item in self.items if query.lower() in item.name.lower()]

    def get_item_details(self, name: str) -> Item:
        for item in self.items:
            if item.name == name:
                return item
        return None

app_instance = App()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if app_instance.login(username, password):
        return redirect(url_for('home_page'))
    return redirect(url_for('login_page'))

@app.route('/register')
def registration_page():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if app_instance.register(username, password):
        return redirect(url_for('login_page'))
    return redirect(url_for('registration_page'))

@app.route('/home')
def home_page():
    return render_template('home.html', items=app_instance.items)

@app.route('/listing')
def listing_page():
    return render_template('listing.html')

@app.route('/listing', methods=['POST'])
def add_listing():
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])
    app_instance.add_item(name, description, price)
    return redirect(url_for('home_page'))

@app.route('/item/<name>')
def item_details(name):
    item = app_instance.get_item_details(name)
    return render_template('item_details.html', item=item)

if __name__ == '__main__':
    app.run(port=8468, debug=False)

from flask import Flask, render_template, request, redirect, url_for, session
from auth import AuthManager
from items import ItemManager

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'

auth_manager = AuthManager()
item_manager = ItemManager()

@app.route('/')
def home():
    if 'username' not in session or not auth_manager.is_logged_in(session['username']):
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '')
    if search_query:
        items = item_manager.search_items(search_query)
    else:
        items = item_manager.get_all_items()
    
    return render_template('home.html', items=items, username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if auth_manager.register(username, password, email):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Registration failed")
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/item/<item_id>')
def item_details(item_id):
    if 'username' not in session or not auth_manager.is_logged_in(session['username']):
        return redirect(url_for('login'))
    
    item = item_manager.get_item_by_id(item_id)
    if not item:
        return redirect(url_for('home'))
    
    return render_template('item.html', item=item)

@app.route('/create_listing', methods=['GET', 'POST'])
def create_listing():
    if 'username' not in session or not auth_manager.is_logged_in(session['username']):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        if item_manager.add_item(title, description, price, session['username']):
            return redirect(url_for('home'))
        else:
            return render_template('listing.html', error="Failed to create listing")
    
    return render_template('listing.html')

if __name__ == '__main__':
    app.run(port=8114, debug=False)

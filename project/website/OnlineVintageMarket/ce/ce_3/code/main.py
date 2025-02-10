from flask import Flask, render_template, request, redirect, url_for, session
from auth import Auth
from listing import Listing

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

auth = Auth()
listing = Listing()

@app.route('/')
def home():
    items = listing.view_listings()
    return render_template('home.html', items=items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/listing', methods=['GET', 'POST'])
def create_listing():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        listing.create_listing(name, description, price)
        return redirect(url_for('home'))
    return render_template('listing.html')

if __name__ == '__main__':
    app.run(port=8559, debug=False)

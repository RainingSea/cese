from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from culture_manager import CultureManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
culture_manager = CultureManager('cultures.txt', 'bookmarks.txt')

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
        else:
            return "Registration failed. Username already exists."
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    cultures = culture_manager.load_cultures()
    return render_template('dashboard.html', cultures=cultures)

@app.route('/culture/<culture_name>')
def culture_details(culture_name):
    details = culture_manager.get_culture_details(culture_name)
    return render_template('culture_details.html', details=details)

@app.route('/bookmarks')
def bookmarks():
    if 'username' in session:
        bookmarks = culture_manager.load_bookmarks(session['username'])
        return render_template('bookmarks.html', bookmarks=bookmarks)
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return "Login failed. Check your username and password."

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=9020, debug=False)

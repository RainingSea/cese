from flask import Flask, render_template, request, redirect, url_for, session, flash
from user_manager import UserManager
from culture_manager import CultureManager
from bookmark_manager import BookmarkManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
culture_manager = CultureManager()
bookmark_manager = BookmarkManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.', 'danger')
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login'))
    cultures = culture_manager.load_cultures()
    return render_template('dashboard.html', cultures=cultures)

@app.route('/culture/<culture_name>')
def culture_details(culture_name):
    if 'username' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login'))
    details = culture_manager.get_culture_details(culture_name)
    return render_template('culture_details.html', details=details)

@app.route('/bookmarks')
def bookmarks():
    if 'username' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login'))
    bookmarks = bookmark_manager.load_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    flash('Invalid username or password. Please try again.', 'danger')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    user_manager.load_users()
    culture_manager.load_cultures()
    bookmark_manager.load_bookmarks()
    app.run(port=8150, debug=False)

from flask import Flask, render_template, request, redirect, url_for, session, flash
from user_manager import UserManager
from culture_manager import CultureManager
from bookmark_manager import BookmarkManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
culture_manager = CultureManager()
bookmark_manager = BookmarkManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username may already exist.')
            return redirect(url_for('register'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect(url_for('login'))
    cultures = culture_manager.get_all_cultures()
    return render_template('dashboard.html', cultures=cultures)

@app.route('/culture/<string:culture_name>', methods=['GET', 'POST'])
def culture_details(culture_name):
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect(url_for('login'))
    details = culture_manager.get_culture_details(culture_name)
    if request.method == 'POST':
        username = session.get('username')
        if bookmark_manager.add_bookmark(username, culture_name):
            flash(f'{culture_name} has been bookmarked.')
        else:
            flash(f'{culture_name} is already in your bookmarks.')
        return redirect(url_for('culture_details', culture_name=culture_name))
    return render_template('culture_details.html', details=details)

@app.route('/bookmarks')
def bookmarks():
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect(url_for('login'))
    username = session.get('username')
    user_bookmarks = bookmark_manager.get_bookmarks(username)
    return render_template('bookmarks.html', bookmarks=user_bookmarks)

@app.route('/remove_bookmark/<string:culture_name>')
def remove_bookmark(culture_name):
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect(url_for('login'))
    username = session.get('username')
    if bookmark_manager.remove_bookmark(username, culture_name):
        flash(f'{culture_name} has been removed from your bookmarks.')
    else:
        flash(f'Failed to remove {culture_name} from your bookmarks.')
    return redirect(url_for('bookmarks'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8314, debug=False)

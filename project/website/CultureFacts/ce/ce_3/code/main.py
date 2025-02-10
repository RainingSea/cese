from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from CultureManager import CultureManager
from BookmarkManager import BookmarkManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

user_manager = UserManager('users.txt')
culture_manager = CultureManager('cultures.txt')
bookmark_manager = BookmarkManager('bookmarks.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    cultures = culture_manager.get_cultures()
    return render_template('dashboard.html', cultures=cultures)

@app.route('/culture/<string:culture_name>', methods=['GET'])
def culture_details(culture_name):
    details = culture_manager.get_culture_details(culture_name)
    return render_template('culture_details.html', details=details)

@app.route('/bookmarks', methods=['GET'])
def bookmarks():
    bookmarks = bookmark_manager.get_bookmarks()
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8614, debug=False)

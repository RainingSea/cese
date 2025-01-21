from flask import Flask, render_template, request, redirect, session
from user import User
from culture import Culture
from bookmark import Bookmark

app = Flask(__name__)
app.secret_key = 'supersecretkey'

user_manager = User()
culture_manager = Culture()
bookmark_manager = Bookmark()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    cultures = culture_manager.get_cultures()
    return render_template('dashboard.html', cultures=cultures)

@app.route('/culture/<name>')
def culture_details(name):
    details = culture_manager.get_culture_details(name)
    return render_template('culture_details.html', details=details)

@app.route('/bookmarks')
def bookmarks():
    user = session.get('username')
    user_bookmarks = bookmark_manager.get_bookmarks(user)
    return render_template('bookmarks.html', bookmarks=user_bookmarks)

if __name__ == '__main__':
    app.run(port=9017, debug=False)

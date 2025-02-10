from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from entry import Entry
from auth import Auth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and entries from files
user_manager = User()
entry_manager = Entry()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        auth = Auth(user_manager)
        if auth.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    auth = Auth(user_manager)
    if auth.login(username, password):
        session['username'] = username
        return redirect(url_for('journal'))
    return redirect(url_for('login'))

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        destination = request.form['destination']
        date = request.form['date']
        activities = request.form['activities']
        photos = request.form['photos']
        reflections = request.form['reflections']
        entry_manager.save(destination, date, activities, photos, reflections)

    entries = entry_manager.load_entries()
    return render_template('journal.html', entries=entries)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8665, debug=False)

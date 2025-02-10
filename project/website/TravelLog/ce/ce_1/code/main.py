from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from EntryManager import EntryManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'
user_manager = UserManager('users.txt')
entry_manager = EntryManager('entries.txt')

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
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        destination = request.form['destination']
        date = request.form['date']
        activities = request.form['activities']
        photos = request.form['photos']
        reflections = request.form['reflections']
        entry_manager.create_entry(session['username'], destination, date, activities, photos, reflections)

    entries = entry_manager.load_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8666, debug=False)

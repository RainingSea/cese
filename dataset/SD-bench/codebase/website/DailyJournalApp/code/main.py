from flask import Flask, render_template, request, redirect, url_for, flash, session
from UserManager import UserManager
from JournalManager import JournalManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
journal_manager = JournalManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, please try again.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another.')
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    entries = journal_manager.load_entries()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        journal_manager.create_entry(title, content)
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', entries=entries)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8304, debug=False)

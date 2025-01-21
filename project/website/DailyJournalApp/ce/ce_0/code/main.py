from flask import Flask, render_template, redirect, url_for, request, session
from auth import Auth
from user import User
from journal_entry import JournalEntry

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

auth = Auth()
user = User()
journal_entry = JournalEntry()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    entries = journal_entry.load_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        journal_entry = JournalEntry(title, content)
        journal_entry.save()
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8932, debug=False)

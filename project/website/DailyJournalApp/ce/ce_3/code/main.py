from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from journal_entry import JournalEntry

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and journal entries from files
users = User().load_users()
journal_entries = JournalEntry().load_entries()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User(username, password).save():
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', entries=journal_entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        JournalEntry(title, content).save_entry()
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if User(username, password).login():
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8935, debug=False)

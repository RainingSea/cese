from flask import Flask, render_template, request, redirect, session
from auth import Auth
from user import User
from journal_entry import JournalEntry

app = Flask(__name__)
app.secret_key = 'your_secret_key'
auth = Auth()
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
            return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        entries = journal_entry.load_all()
        return render_template('dashboard.html', entries=entries)
    return redirect('/')

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            journal_entry.title = title
            journal_entry.content = content
            journal_entry.save()
            return redirect('/dashboard')
        return render_template('new_entry.html')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8526, debug=False)

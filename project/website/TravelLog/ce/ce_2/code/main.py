from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from journal_manager import JournalManager
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
journal_manager = JournalManager('journal_entries.txt')

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
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('journal_entry'))
    return redirect(url_for('login'))

@app.route('/journal_entry', methods=['GET', 'POST'])
def journal_entry():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        destination = request.form['destination']
        dates = request.form['dates']
        activities = request.form['activities']
        photos = request.files['photos']
        reflections = request.form['reflections']
        if photos:
            photos.save(os.path.join('static/uploads', photos.filename))
        journal_manager.create_entry(destination, dates, activities, photos.filename, reflections)
    
    entries = journal_manager.view_entries()
    return render_template('journal_entry.html', entries=entries)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8440, debug=False)

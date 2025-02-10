from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from JournalManager import JournalManager
from User import User
from JournalEntry import JournalEntry

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
journal_manager = JournalManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user_manager.add_user(user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if request.method == 'POST':
        username = session['username']
        destination = request.form['destination']
        dates = request.form['dates']
        activities = request.form['activities']
        photos = request.form.getlist('photos')
        reflections = request.form['reflections']
        entry = JournalEntry(username, destination, dates, activities, photos, reflections)
        journal_manager.add_entry(entry)
        return redirect(url_for('journal'))
    return render_template('journal.html', entries=journal_manager.entries)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = user_manager.find_user(username)
    if user and user.password == password:
        session['username'] = username
        return redirect(url_for('journal'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8668, debug=False)

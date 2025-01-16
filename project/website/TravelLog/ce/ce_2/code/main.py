from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from journal_entry import JournalEntry
from travel_log_app import TravelLogApp

app = Flask(__name__)
app.secret_key = 'supersecretkey'
travel_log_app = TravelLogApp()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if travel_log_app.register(username, password):
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
        photos = request.form.getlist('photos')
        reflections = request.form['reflections']
        travel_log_app.create_entry(destination, date, activities, photos, reflections)

    entries = travel_log_app.view_entries()
    return render_template('dashboard.html', entries=entries)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if travel_log_app.login(username, password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8667, debug=False)

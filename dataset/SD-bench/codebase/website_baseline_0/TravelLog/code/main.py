from flask import Flask, render_template, request, redirect, url_for, session, flash
from UserManager import UserManager
from EntryManager import EntryManager
from models import User, JournalEntry

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager()
entry_manager = EntryManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = user_manager.find_user(username)
    if user and user.password == password:
        session['username'] = username
        return redirect(url_for('journal'))
    else:
        flash('Invalid username or password.')
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user_manager.save_user(user):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already taken. Please choose another.')
    return render_template('register.html')

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        destination = request.form['destination']
        dates = request.form['dates']
        activities = request.form['activities']
        photos = request.form.getlist('photos')
        reflections = request.form['reflections']
        entry = JournalEntry(destination, dates, activities, photos, reflections)
        entry_manager.save_entry(entry)
        return redirect(url_for('view_entries'))
    return render_template('journal.html')

@app.route('/view_entries')
def view_entries():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    entries = entry_manager.load_entries()
    return render_template('view_entries.html', entries=entries)

@app.route('/edit_entry/<destination>/<dates>', methods=['GET', 'POST'])
def edit_entry(destination, dates):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    entry = next((e for e in entry_manager.load_entries() if e.destination == destination and e.dates == dates), None)
    if request.method == 'POST':
        new_destination = request.form['destination']
        new_dates = request.form['dates']
        new_activities = request.form['activities']
        new_photos = request.form.getlist('photos')
        new_reflections = request.form['reflections']
        new_entry = JournalEntry(new_destination, new_dates, new_activities, new_photos, new_reflections)
        entry_manager.edit_entry(entry, new_entry)
        return redirect(url_for('view_entries'))
    return render_template('edit_entry.html', entry=entry)

@app.route('/delete_entry/<destination>/<dates>', methods=['POST'])
def delete_entry(destination, dates):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    entry = next((e for e in entry_manager.load_entries() if e.destination == destination and e.dates == dates), None)
    if entry:
        entry_manager.delete_entry(entry)
    return redirect(url_for('view_entries'))

@app.route('/search_entries', methods=['GET', 'POST'])
def search_entries():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    search_results = []
    if request.method == 'POST':
        search_term = request.form['search_term']
        search_results = entry_manager.search_entries(search_term)
    return render_template('search_entries.html', entries=search_results)

@app.route('/share_entry/<destination>/<dates>', methods=['POST'])
def share_entry(destination, dates):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    entry = next((e for e in entry_manager.load_entries() if e.destination == destination and e.dates == dates), None)
    if entry:
        message = entry_manager.share_entry(entry)
        flash(message)
    return redirect(url_for('view_entries'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8559, debug=False)

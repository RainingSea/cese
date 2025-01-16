from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from journal_manager import JournalEntryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager('users.txt')
journal_manager = JournalEntryManager('entries.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register_user(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Username already exists.")
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('journal'))
    return redirect(url_for('login'))

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
        journal_manager.create_entry(destination, dates, activities, photos, reflections)

    entries = journal_manager.load_entries()
    return render_template('journal.html', entries=entries)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/edit_entry/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        destination = request.form['destination']
        dates = request.form['dates']
        activities = request.form['activities']
        photos = request.form.getlist('photos')
        reflections = request.form['reflections']
        journal_manager.update_entry(entry_id, destination, dates, activities, photos, reflections)
        return redirect(url_for('journal'))

    entry = journal_manager.get_entry(entry_id)
    return render_template('edit_entry.html', entry=entry)

@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    journal_manager.delete_entry(entry_id)
    return redirect(url_for('journal'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    search_results = []
    if request.method == 'POST':
        query = request.form['query']
        search_results = journal_manager.search_entries(query)

    entries = journal_manager.load_entries()
    return render_template('search.html', entries=entries, search_results=search_results)

@app.route('/share_entry/<int:entry_id>', methods=['POST'])
def share_entry(entry_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    entry = journal_manager.get_entry(entry_id)
    # Here you would implement the sharing functionality (e.g., via email or social media)
    # For now, we will just redirect back to the journal
    return redirect(url_for('journal'))

if __name__ == '__main__':
    app.run(port=8670, debug=False)

from flask import Flask, render_template, request, redirect, url_for, session, flash
from auth import UserManager
from recommendations import PreferenceManager, DestinationManager

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

user_manager = UserManager('users.txt')
pref_manager = PreferenceManager('preferences.txt')
dest_manager = DestinationManager('destinations.txt', 'favorites.txt')

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('preferences'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            session['username'] = username
            return redirect(url_for('preferences'))
        flash('Username already exists')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('preferences'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        budget = int(request.form['budget'])
        activities = request.form.getlist('activities')
        climate = request.form['climate']
        pref_manager.save_preferences(session['username'], budget, activities, climate)
        return redirect(url_for('recommendations'))
    
    return render_template('preferences.html')

@app.route('/recommendations')
def recommendations():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    prefs = pref_manager.get_preferences(session['username'])
    if not prefs:
        return redirect(url_for('preferences'))
    
    recs = dest_manager.get_recommendations(prefs)
    return render_template('recommendations.html', recommendations=recs)

@app.route('/save_favorite/<destination>')
def save_favorite(destination):
    if 'username' not in session:
        return redirect(url_for('login'))
    dest_manager.save_favorite(session['username'], destination)
    return redirect(url_for('recommendations'))

if __name__ == '__main__':
    app.run(port=8071, debug=False)

from flask import Flask, render_template, request, redirect, url_for, session, flash
from user import User
from preferences import Preferences
from destination import Destination
from favorites import Favorites

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    return User.load_all()

def load_destinations():
    return Destination.load_all()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def user_login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('preferences'))
    flash('Invalid username or password')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if any(user.username == username for user in users):
            flash('Username already exists. Please choose another one.')
            return redirect(url_for('register'))
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        budget = float(request.form['budget'])
        activities = request.form.getlist('activities')
        climate = request.form['climate']
        preferences = Preferences(budget, activities, climate)
        preferences.save()
        return redirect(url_for('recommendations'))
    return render_template('preferences.html')

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    destinations = load_destinations()
    if request.method == 'POST':
        user = session.get('username')
        destination_name = request.form['destination']
        favorites = Favorites(user)
        favorites.destinations.append(destination_name)
        favorites.save()
    return render_template('recommendations.html', destinations=destinations)

@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    user = session.get('username')
    favorites = Favorites(user)
    if request.method == 'POST':
        destination_name = request.form['destination']
        favorites.destinations.append(destination_name)
        favorites.save()
    return render_template('favorites.html', favorites=favorites.destinations)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/destination/<name>')
def destination_detail(name):
    destinations = load_destinations()
    destination = next((d for d in destinations if d.name == name), None)
    return render_template('destination_detail.html', destination=destination)

if __name__ == '__main__':
    app.run(port=8560, debug=False)

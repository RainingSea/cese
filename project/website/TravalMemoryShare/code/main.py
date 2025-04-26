from flask import Flask, render_template, request, redirect, url_for, session, flash
from UserManager import UserManager
from AlbumManager import AlbumManager
from InteractionManager import InteractionManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
album_manager = AlbumManager()
interaction_manager = InteractionManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
        else:
            flash("Username already exists!")
    return render_template('registration.html')

@app.route('/album_creation', methods=['GET', 'POST'])
def album_creation():
    if request.method == 'POST':
        user = session.get('username')
        album_data = request.form.to_dict()
        if album_manager.create_album(user, album_data):
            flash("Album created successfully!")
        else:
            flash("Failed to create album.")
        return redirect(url_for('album_exploration'))
    return render_template('album_creation.html')

@app.route('/album_exploration')
def album_exploration():
    albums = album_manager.explore_albums()
    return render_template('album_exploration.html', albums=albums)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('album_exploration'))
    flash("Invalid username or password!")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8261, debug=False)

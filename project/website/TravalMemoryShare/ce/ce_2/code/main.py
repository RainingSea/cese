from flask import Flask, render_template, request, redirect, url_for, session
from user import User, UserController
from album import Album, AlbumController
from interaction import Interaction, InteractionController
from data_storage import DataStorage

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
data_storage = DataStorage()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_controller = UserController()
        if user_controller.register_user(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('registration.html', error="Username already exists.")
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user_controller = UserController()
    if user_controller.login_user(username, password):
        session['username'] = username
        return redirect(url_for('explore'))
    return render_template('login.html', error="Invalid username or password.")

@app.route('/explore')
def explore():
    albums = data_storage.load_albums()
    return render_template('explore.html', albums=albums)

@app.route('/create_album', methods=['GET', 'POST'])
def create_album():
    if request.method == 'POST':
        title = request.form['title']
        is_public = 'is_public' in request.form
        album_controller = AlbumController()
        album_controller.create_album(title, session['username'], is_public)
        return redirect(url_for('explore'))
    return render_template('album.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8326, debug=False)

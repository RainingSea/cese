from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from album_manager import AlbumManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
user_manager = UserManager()
album_manager = AlbumManager()

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
        return redirect(url_for('album_creation'))
    return redirect(url_for('login'))

@app.route('/album_creation', methods=['GET', 'POST'])
def album_creation():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        album_data = {
            'title': request.form['title'],
            'photos': request.form.getlist('photos'),
            'privacy': request.form['privacy']
        }
        album_manager.create_album(session['username'], album_data)
        return redirect(url_for('explore'))
    return render_template('album_creation.html')

@app.route('/explore')
def explore():
    if 'username' not in session:
        return redirect(url_for('login'))
    albums = album_manager.explore_albums()
    return render_template('explore.html', albums=albums)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8657, debug=False)

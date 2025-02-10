from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from album import Album
from interaction import Interaction
from storage import Storage

app = Flask(__name__)
app.secret_key = 'supersecretkey'
storage = Storage()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        storage.save_user(new_user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/albums', methods=['GET', 'POST'])
def albums():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        user_id = session.get('username')
        new_album = Album(user_id, title, description)
        storage.save_album(new_album)
        return redirect(url_for('albums'))
    user_albums = storage.load_albums()
    return render_template('albums.html', albums=user_albums)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = storage.load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('albums'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8654, debug=False)

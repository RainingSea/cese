from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password])
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

class AlbumManager:
    def __init__(self):
        self.albums = self.load_albums()

    def load_albums(self):
        if not os.path.exists('albums.txt'):
            return []
        with open('albums.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def create_album(self, user: str, album_data: dict) -> None:
        self.albums.append([user, album_data['title'], album_data['description']])
        self.save_albums()

    def save_albums(self):
        with open('albums.txt', 'w') as file:
            for album in self.albums:
                file.write('|'.join(album) + '\n')

    def get_albums(self) -> list:
        return self.albums

class InteractionManager:
    def __init__(self):
        self.interactions = self.load_interactions()

    def load_interactions(self):
        if not os.path.exists('interactions.txt'):
            return []
        with open('interactions.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def like_album(self, user: str, album_id: str) -> None:
        self.interactions.append([user, album_id, 'like'])
        self.save_interactions()

    def comment_on_album(self, user: str, album_id: str, comment: str) -> None:
        self.interactions.append([user, album_id, comment])
        self.save_interactions()

    def save_interactions(self):
        with open('interactions.txt', 'w') as file:
            for interaction in self.interactions:
                file.write('|'.join(interaction) + '\n')

@app.route('/', methods=['GET', 'POST'])
def login():
    user_manager = UserManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/albums')
        else:
            flash("Invalid credentials", "error")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    user_manager = UserManager()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash("Registration successful", "success")
            return redirect('/')
        else:
            flash("Username already exists", "error")
    return render_template('registration.html')

@app.route('/albums', methods=['GET', 'POST'])
def albums():
    album_manager = AlbumManager()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        album_manager.create_album(session['username'], {'title': title, 'description': description})
        flash("Album created successfully", "success")
        return redirect('/albums')
    return render_template('album_view.html', albums=album_manager.get_albums())

@app.route('/album_creation', methods=['GET', 'POST'])
def album_creation():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        album_manager = AlbumManager()
        album_manager.create_album(session['username'], {'title': title, 'description': description})
        flash("Album created successfully", "success")
        return redirect('/albums')
    return render_template('album_creation.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out", "success")
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8433, debug=False)

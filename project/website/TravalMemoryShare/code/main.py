from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1])
        return None

class Album:
    def __init__(self, title: str, description: str, owner: str, is_private: bool = False):
        self.title = title
        self.description = description
        self.images = []
        self.owner = owner
        self.is_private = is_private

    def save(self):
        with open('albums.txt', 'a') as f:
            f.write(f"{self.title}|{self.description}|{self.owner}|{self.is_private}|{'|'.join(self.images)}\n")

    @staticmethod
    def load(title: str):
        with open('albums.txt', 'r') as f:
            for line in f:
                album_data = line.strip().split('|')
                if album_data[0] == title:
                    album = Album(album_data[0], album_data[1], album_data[2], album_data[3] == 'True')
                    album.images = album_data[4:]
                    return album
        return None

class Interaction:
    def __init__(self, album_title: str, user: str, type: str, comment: str = None):
        self.album_title = album_title
        self.user = user
        self.type = type
        self.comment = comment

    def save(self):
        with open('interactions.txt', 'a') as f:
            if self.comment:
                f.write(f"{self.album_title}|{self.user}|{self.type}|{self.comment}\n")
            else:
                f.write(f"{self.album_title}|{self.user}|{self.type}\n")

class Application:
    def __init__(self):
        self.users = []
        self.albums = []
        self.interactions = []

    def register(self, username: str, password: str) -> bool:
        if User.load(username) is None:
            user = User(username, password)
            user.save()
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        user = User.load(username)
        return user is not None and user.password == password

    def create_album(self, title: str, description: str, owner: str, is_private: bool) -> None:
        album = Album(title, description, owner, is_private)
        album.save()

    def like_album(self, album_title: str, user: str) -> None:
        interaction = Interaction(album_title, user, 'like')
        interaction.save()

    def comment_on_album(self, album_title: str, user: str, comment: str) -> None:
        interaction = Interaction(album_title, user, 'comment', comment)
        interaction.save()

    def get_albums(self) -> list:
        albums = []
        with open('albums.txt', 'r') as f:
            for line in f:
                album_data = line.strip().split('|')
                album = Album(album_data[0], album_data[1], album_data[2], album_data[3] == 'True')
                album.images = album_data[4:]
                albums.append(album)
        return albums

    def get_public_albums(self) -> list:
        return [album for album in self.get_albums() if not album.is_private]

    def notify_new_album(self, album_title: str):
        # Placeholder for notification logic
        pass

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Application().register(username, password):
            flash('Registration successful!')
            return redirect(url_for('login'))
        else:
            flash('Username already exists.')
    return render_template('register.html')

@app.route('/album/create', methods=['GET', 'POST'])
def create_album():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        owner = request.form['owner']
        is_private = 'is_private' in request.form
        if title:
            album = Album(title, description, owner, is_private)
            if 'file' in request.files:
                file = request.files['file']
                if file:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    album.images.append(filename)
            album.save()
            Application().notify_new_album(title)  # Notify users about the new album
            flash('Album created successfully!')
            return redirect(url_for('album_gallery'))
        else:
            flash('Album title is required.')
    return render_template('album_create.html')

@app.route('/album/gallery')
def album_gallery():
    albums = Application().get_public_albums()
    return render_template('album_gallery.html', albums=albums)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8327, debug=False)

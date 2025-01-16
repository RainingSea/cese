from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load() -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

class Album:
    def __init__(self, title: str, photos: list, is_private: bool):
        self.title = title
        self.photos = photos
        self.is_private = is_private

    def save(self) -> None:
        with open('albums.txt', 'a') as f:
            f.write(f"{self.title}|{','.join(self.photos)}|{self.is_private}\n")

    @staticmethod
    def load() -> list:
        albums = []
        try:
            with open('albums.txt', 'r') as f:
                for line in f:
                    title, photos, is_private = line.strip().split('|')
                    albums.append(Album(title, photos.split(','), is_private == 'True'))
        except FileNotFoundError:
            pass
        return albums

class Interaction:
    def __init__(self, user: str, album_id: str, interaction_type: str):
        self.user = user
        self.album_id = album_id
        self.type = interaction_type

    def save(self) -> None:
        with open('interactions.txt', 'a') as f:
            f.write(f"{self.user}|{self.album_id}|{self.type}\n")

class App:
    def register(self, username: str, password: str) -> None:
        user = User(username, password)
        user.save()

    def login(self, username: str, password: str) -> User:
        users = User.load()
        for user in users:
            if user.username == username and user.password == password:
                return user
        return None

    def create_album(self, title: str, photos: list, is_private: bool) -> Album:
        album = Album(title, photos, is_private)
        album.save()
        return album

    def view_albums(self) -> list:
        return Album.load()

    def like_album(self, album_id: str, user: str) -> None:
        interaction = Interaction(user, album_id, 'like')
        interaction.save()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    app_instance = App()
    user = app_instance.login(username, password)
    if user:
        session['username'] = user.username
        return redirect(url_for('album_page'))
    return 'Login Failed'

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_instance = App()
        app_instance.register(username, password)
        return redirect(url_for('login_page'))
    return render_template('registration.html')

@app.route('/albums')
def album_page():
    app_instance = App()
    albums = app_instance.view_albums()
    return render_template('album.html', albums=albums)

if __name__ == '__main__':
    app.run(port=8656, debug=False)

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_users():
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

class Album:
    def __init__(self, title: str, description: str, owner: str):
        self.title = title
        self.description = description
        self.owner = owner
        self.photos = []

    def add_photo(self, photo: str):
        self.photos.append(photo)

    def save(self):
        with open('albums.txt', 'a') as file:
            file.write(f"{self.title}|{self.description}|{self.owner}|{'|'.join(self.photos)}\n")

    @staticmethod
    def load_albums():
        albums = []
        try:
            with open('albums.txt', 'r') as file:
                for line in file:
                    parts = line.strip().split('|')
                    title, description, owner = parts[0], parts[1], parts[2]
                    photos = parts[3:] if len(parts) > 3 else []
                    album = Album(title, description, owner)
                    album.photos = photos
                    albums.append(album)
        except FileNotFoundError:
            pass
        return albums

class Interaction:
    def __init__(self, album_id: str, user_id: str):
        self.album_id = album_id
        self.user_id = user_id
        self.likes = []
        self.comments = {}

    def add_like(self, user_id: str):
        if user_id not in self.likes:
            self.likes.append(user_id)

    def add_comment(self, user_id: str, comment: str):
        self.comments[user_id] = comment

    def save(self):
        with open('interactions.txt', 'a') as file:
            file.write(f"{self.album_id}|{self.user_id}|{'|'.join(self.likes)}|{str(self.comments)}\n")

class Application:
    def register(self, username: str, password: str) -> bool:
        users = User.load_users()
        if any(user.username == username for user in users):
            return False  # Username already exists
        new_user = User(username, password)
        new_user.save()
        return True  # Registration successful

    def login(self, username: str, password: str) -> bool:
        users = User.load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username  # Store username in session
                return True  # Login successful
        return False  # Invalid credentials

    def logout(self):
        session.pop('username', None)  # Remove username from session

    def create_album(self, title: str, description: str, owner: str) -> Album:
        new_album = Album(title, description, owner)
        new_album.save()
        return new_album

    def view_album(self, album_id: str) -> Album:
        albums = Album.load_albums()
        for album in albums:
            if album.title == album_id:  # Assuming album_id is the title for simplicity
                return album
        return None

    def like_album(self, album_id: str, user_id: str):
        # Implementation for liking an album would go here
        pass

    def comment_on_album(self, album_id: str, user_id: str, comment: str):
        # Implementation for commenting on an album would go here
        pass

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_instance = Application()
        if app_instance.register(username, password):
            flash('Registration successful!')
            return redirect(url_for('login_page'))
        else:
            flash('Username already exists.')
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    app_instance = Application()
    if app_instance.login(username, password):
        flash('Login successful!')
        return redirect(url_for('album_create_page'))
    else:
        flash('Invalid credentials.')
        return redirect(url_for('login_page'))

@app.route('/logout')
def logout_user():
    app_instance = Application()
    app_instance.logout()
    flash('You have been logged out.')
    return redirect(url_for('login_page'))

@app.route('/album/create', methods=['GET', 'POST'])
def album_create_page():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        owner = session.get('username')  # Get the logged-in user's username
        app_instance = Application()
        app_instance.create_album(title, description, owner)
        flash('Album created successfully!')
        return redirect(url_for('album_view_page'))
    return render_template('album_create.html')

@app.route('/album/view')
def album_view_page():
    albums = Album.load_albums()
    return render_template('album_view.html', albums=albums)

if __name__ == '__main__':
    app.run(port=8322, debug=False)

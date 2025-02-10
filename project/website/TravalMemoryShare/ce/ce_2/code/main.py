from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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
    def __init__(self, title: str, owner: str):
        self.title = title
        self.images = []
        self.owner = owner

    def add_image(self, image_path: str):
        self.images.append(image_path)

    def save(self):
        with open('albums.txt', 'a') as f:
            f.write(f"{self.title}|{self.owner}|{','.join(self.images)}\n")

    @staticmethod
    def load(owner: str):
        albums = []
        with open('albums.txt', 'r') as f:
            for line in f:
                album_data = line.strip().split('|')
                if album_data[1] == owner:
                    albums.append(Album(album_data[0], album_data[1]))
                    albums[-1].images = album_data[2].split(',') if album_data[2] else []
        return albums

class Comment:
    def __init__(self, album_id: str, username: str, content: str):
        self.album_id = album_id
        self.username = username
        self.content = content

    def save(self):
        with open('comments.txt', 'a') as f:
            f.write(f"{self.album_id}|{self.username}|{self.content}\n")

    @staticmethod
    def load(album_id: str):
        comments = []
        with open('comments.txt', 'r') as f:
            for line in f:
                comment_data = line.strip().split('|')
                if comment_data[0] == album_id:
                    comments.append(Comment(comment_data[0], comment_data[1], comment_data[2]))
        return comments

class MainApp:
    def __init__(self):
        self.users = []
        self.albums = []

    def register(self, username: str, password: str) -> bool:
        if User.load(username) is None:
            user = User(username, password)
            user.save()
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        user = User.load(username)
        if user and user.password == password:
            session['username'] = username
            return True
        return False

    def create_album(self, title: str, owner: str) -> Album:
        album = Album(title, owner)
        album.save()
        return album

    def add_comment(self, album_id: str, username: str, content: str):
        comment = Comment(album_id, username, content)
        comment.save()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_instance = MainApp()
        if app_instance.register(username, password):
            return redirect('/')
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login_action():
    username = request.form['username']
    password = request.form['password']
    app_instance = MainApp()
    if app_instance.login(username, password):
        return redirect('/gallery')
    return redirect('/')

@app.route('/gallery')
def gallery_page():
    app_instance = MainApp()
    if 'username' in session:
        albums = Album.load(session['username'])
        return render_template('gallery.html', albums=albums)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8655, debug=False)

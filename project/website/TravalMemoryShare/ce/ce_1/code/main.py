from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return {}
        with open('users.txt', 'r') as f:
            return dict(line.strip().split('|') for line in f)

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as f:
            for username, password in self.users.items():
                f.write(f"{username}|{password}\n")

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class AlbumManager:
    def __init__(self):
        self.albums = self.load_albums()

    def load_albums(self):
        if not os.path.exists('albums.txt'):
            return {}
        with open('albums.txt', 'r') as f:
            return json.load(f)

    def create_album(self, user: str, album_data: dict) -> bool:
        if user not in self.albums:
            self.albums[user] = []
        self.albums[user].append(album_data)
        self.save_albums()
        return True

    def save_albums(self):
        with open('albums.txt', 'w') as f:
            json.dump(self.albums, f)

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
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another one.')
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect(url_for('album_creation'))
    else:
        flash('Invalid username or password.')
        return redirect(url_for('login'))

@app.route('/album_creation', methods=['GET', 'POST'])
def album_creation():
    if request.method == 'POST':
        album_data = {
            'title': request.form['title'],
            'images': request.form.getlist('images')
        }
        album_manager.create_album(request.form['username'], album_data)
        flash('Album created successfully!')
        return redirect(url_for('gallery'))
    return render_template('album_creation.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', albums=album_manager.albums)

if __name__ == '__main__':
    app.run(port=8259, debug=False)

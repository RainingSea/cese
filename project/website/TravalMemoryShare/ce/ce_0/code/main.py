from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False  # User already exists
        self.users.append([username, password])
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def follow_user(self, follower: str, followed: str) -> bool:
        # This method will be implemented in interactions management
        return True

class AlbumManager:
    def __init__(self):
        self.albums = self.load_albums()

    def load_albums(self):
        if not os.path.exists('albums.txt'):
            return []
        with open('albums.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def create_album(self, title: str, username: str, images: list) -> bool:
        self.albums.append([title, username, ','.join(images), 'public'])
        self.save_albums()
        return True

    def save_albums(self):
        with open('albums.txt', 'w') as file:
            for album in self.albums:
                file.write('|'.join(album) + '\n')

    def customize_album(self, album_id: str, layout: str) -> bool:
        # Placeholder for customization logic
        return True

    def explore_albums(self) -> list:
        return self.albums

    def interact_with_album(self, album_id: str, interaction_type: str, user: str) -> bool:
        # Placeholder for interaction logic
        return True

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register(username, password):
        return redirect('/')
    return "Registration failed", 400

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/album_exploration')
    return "Login failed", 400

@app.route('/album_exploration')
def album_exploration():
    albums = album_manager.explore_albums()
    return render_template('album_exploration.html', albums=albums)

if __name__ == '__main__':
    user_manager = UserManager()
    album_manager = AlbumManager()
    app.run(port=8430, debug=False)

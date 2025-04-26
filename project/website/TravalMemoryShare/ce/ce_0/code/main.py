from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append({'username': username, 'password': password})
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user['username'] == username and user['password'] == password for user in self.users)

class AlbumManager:
    def __init__(self):
        self.albums = self.load_albums()

    def load_albums(self):
        albums = []
        if os.path.exists('albums.txt'):
            with open('albums.txt', 'r') as file:
                for line in file:
                    title, description, user = line.strip().split('|')
                    albums.append({'title': title, 'description': description, 'user': user})
        return albums

    def create_album(self, user: str, title: str, description: str) -> bool:
        self.albums.append({'title': title, 'description': description, 'user': user})
        with open('albums.txt', 'a') as file:
            file.write(f"{title}|{description}|{user}\n")
        return True

    def explore_albums(self):
        return self.albums

class InteractionManager:
    def __init__(self):
        self.interactions = self.load_interactions()

    def load_interactions(self):
        interactions = []
        if os.path.exists('interactions.txt'):
            with open('interactions.txt', 'r') as file:
                for line in file:
                    interactions.append(line.strip())
        return interactions

    def like_album(self, album_id: str, user: str) -> bool:
        # Implementation for liking an album
        return True

    def comment_on_album(self, album_id: str, user: str, comment: str) -> bool:
        # Implementation for commenting on an album
        return True

    def follow_user(self, follower: str, followed: str) -> bool:
        # Implementation for following a user
        return True

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
        else:
            return "Username already exists!"
    return render_template('registration.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        album_manager.create_album(session['username'], title, description)
        return redirect(url_for('explore'))
    return render_template('album_creation.html')

@app.route('/explore')
def explore():
    albums = album_manager.explore_albums()
    return render_template('explore.html', albums=albums)

if __name__ == '__main__':
    user_manager = UserManager()
    album_manager = AlbumManager()
    interaction_manager = InteractionManager()
    app.run(port=8258, debug=False)

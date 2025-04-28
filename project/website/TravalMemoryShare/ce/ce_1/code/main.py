from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load user data
def load_users():
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
    return users

# Load album data
def load_albums():
    albums = []
    if os.path.exists('albums.txt'):
        with open('albums.txt', 'r') as file:
            for line in file:
                title, images, privacy = line.strip().split('|')
                albums.append({'title': title, 'images': images.split(','), 'privacy': privacy})
    return albums

# Load interactions data
def load_interactions():
    interactions = []
    if os.path.exists('interactions.txt'):
        with open('interactions.txt', 'r') as file:
            for line in file:
                user, album, likes, comments = line.strip().split('|')
                interactions.append({'user': user, 'album': album, 'likes': int(likes), 'comments': comments.split(',')})
    return interactions

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.txt', 'a') as file:
            file.write(f'{username}|{password}\n')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/album/create', methods=['GET', 'POST'])
def create_album():
    if request.method == 'POST':
        title = request.form['title']
        images = request.form.getlist('images')
        privacy = request.form['privacy']
        with open('albums.txt', 'a') as file:
            file.write(f'{title}|{",".join(images)}|{privacy}\n')
        return redirect(url_for('view_album'))
    return render_template('album_create.html')

@app.route('/album/view')
def view_album():
    albums = load_albums()
    return render_template('album_view.html', albums=albums)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8431, debug=False)

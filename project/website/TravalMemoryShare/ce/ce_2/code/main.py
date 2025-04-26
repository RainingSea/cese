from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def login(self):
        with open('users.txt', 'r') as f:
            users = f.readlines()
            for user in users:
                uname, pwd = user.strip().split('|')
                if uname == self.username and pwd == self.password:
                    return True
        return False

    def follow(self):
        pass  # Placeholder for future implementation

class Album:
    def __init__(self, title, description, images, visibility):
        self.title = title
        self.description = description
        self.images = images
        self.visibility = visibility

    def create(self):
        with open('albums.txt', 'a') as f:
            f.write(f"{self.title}|{self.description}|{self.images}|{self.visibility}\n")

    def customize(self):
        pass  # Placeholder for future implementation

    def share(self):
        pass  # Placeholder for future implementation

class Interaction:
    def __init__(self, user, album):
        self.user = user
        self.album = album
        self.likes = 0
        self.comments = []

    def like(self):
        self.likes += 1

    def comment(self, comment):
        self.comments.append(comment)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.register()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/album/create', methods=['GET', 'POST'])
def create_album():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        images = request.form['images']
        visibility = request.form['visibility']
        album = Album(title, description, images, visibility)
        album.create()
        flash('Album created successfully!')
        return redirect(url_for('explore'))
    return render_template('album_creation.html')

if __name__ == '__main__':
    app.run(port=8260, debug=False)

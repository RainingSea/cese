from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class User:
    def __init__(self, username: str, password: str, bio: str = ""):
        self.username = username
        self.password = password
        self.bio = bio

    def get_profile(self) -> str:
        return f"Username: {self.username}, Bio: {self.bio}"

class Article:
    def __init__(self, article_id: int, content: str, author: str):
        self.id = article_id
        self.content = content
        self.author = author

    def get_article(self) -> str:
        return f"Article ID: {self.id}, Content: {self.content}, Author: {self.author}"

class Interaction:
    def __init__(self):
        self.likes = []
        self.comments = {}
        self.followers = []

    def add_like(self, username: str, article_id: int) -> None:
        self.likes.append((username, article_id))

    def add_comment(self, username: str, article_id: int, comment: str) -> None:
        if article_id not in self.comments:
            self.comments[article_id] = []
        self.comments[article_id].append((username, comment))

    def add_follower(self, follower: str, followee: str) -> None:
        self.followers.append((follower, followee))

def load_users():
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = User(username, password)
    return users

def load_articles():
    articles = []
    if os.path.exists('articles.txt'):
        with open('articles.txt', 'r') as file:
            for line in file:
                article_id, content, author = line.strip().split('|')
                articles.append(Article(int(article_id), content, author))
    return articles

users = load_users()
articles = load_articles()
interactions = Interaction()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = User(username, password)
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form['username']
        bio = request.form['bio']
        users[username].bio = bio
        return redirect(url_for('profile'))
    return render_template('profile.html', user=users)

@app.route('/feed')
def feed():
    return render_template('feed.html', articles=articles)

if __name__ == '__main__':
    app.run(port=8247, debug=False)

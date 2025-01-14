from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class Tip:
    def __init__(self, content: str):
        self.content = content

    def save(self) -> None:
        with open('tips.txt', 'a') as f:
            f.write(f"{self.content}\n")

class Article:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self) -> None:
        with open('articles.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}\n")

class ForumPost:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def save(self) -> None:
        with open('forum.txt', 'a') as f:
            f.write(f"{self.username}|{self.content}\n")

def load_users():
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users[username] = password
    return users

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/submit_tip', methods=['GET', 'POST'])
def submit_tip():
    if request.method == 'POST':
        content = request.form['content']
        tip = Tip(content)
        tip.save()
        return redirect(url_for('dashboard'))
    return render_template('tips.html')

@app.route('/submit_article', methods=['GET', 'POST'])
def submit_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        article = Article(title, content)
        article.save()
        return redirect(url_for('dashboard'))
    return render_template('articles.html')

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        post = ForumPost(session['username'], content)
        post.save()
        return redirect(url_for('forum'))
    return render_template('forum.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8458, debug=False)

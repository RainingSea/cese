from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_all():
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

class Tip:
    def __init__(self, content: str):
        self.content = content

    def save(self):
        with open('tips.txt', 'a') as f:
            f.write(f"{self.content}\n")

    @staticmethod
    def load_all():
        tips = []
        if os.path.exists('tips.txt'):
            with open('tips.txt', 'r') as f:
                for line in f:
                    tips.append(Tip(line.strip()))
        return tips

class ForumPost:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def save(self):
        with open('forum.txt', 'a') as f:
            f.write(f"{self.username}|{self.content}\n")

    @staticmethod
    def load_all():
        posts = []
        if os.path.exists('forum.txt'):
            with open('forum.txt', 'r') as f:
                for line in f:
                    username, content = line.strip().split('|')
                    posts.append(ForumPost(username, content))
        return posts

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.load_all()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
        return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        content = request.form['content']
        new_tip = Tip(content)
        new_tip.save()
        return redirect(url_for('tips'))
    
    tips = Tip.load_all()
    return render_template('tips.html', tips=tips)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        new_post = ForumPost(session['username'], content)
        new_post.save()
        return redirect(url_for('forum'))
    
    posts = ForumPost.load_all()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(port=8169, debug=True)

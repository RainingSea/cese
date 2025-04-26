from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def register(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")
        return True

    def login(self):
        with open('users.txt', 'r') as f:
            users = f.readlines()
            for user in users:
                u, p, _ = user.strip().split('|')
                if u == self.username and p == self.password:
                    return True
        return False

    def update_profile(self):
        # Profile update logic can be implemented here
        return True

    @staticmethod
    def load_users():
        users = []
        with open('users.txt', 'r') as f:
            users = [line.strip().split('|') for line in f.readlines()]
        return users

class Tip:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def submit_tip(self):
        with open('tips.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.author}\n")
        return True

    @staticmethod
    def view_tips():
        with open('tips.txt', 'r') as f:
            return [line.strip().split('|') for line in f.readlines()]

class Resource:
    def __init__(self, title, link, description):
        self.title = title
        self.link = link
        self.description = description

    def add_resource(self):
        with open('resources.txt', 'a') as f:
            f.write(f"{self.title}|{self.link}|{self.description}\n")
        return True

    @staticmethod
    def view_resources():
        with open('resources.txt', 'r') as f:
            return [line.strip().split('|') for line in f.readlines()]

class ForumPost:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def submit_post(self):
        with open('forum_posts.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.author}\n")
        return True

    @staticmethod
    def view_posts():
        with open('forum_posts.txt', 'r') as f:
            return [line.strip().split('|') for line in f.readlines()]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password, '')
        if user.login():
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        user.register()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    users = User.load_users()
    return render_template('dashboard.html', users=users)

@app.route('/submit_tip', methods=['GET', 'POST'])
def submit_tip():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        tip = Tip(title, content, author)
        tip.submit_tip()
        return redirect(url_for('dashboard'))
    return render_template('submit_tip.html')

@app.route('/view_resources')
def view_resources():
    resources = Resource.view_resources()
    return render_template('view_resources.html', resources=resources)

@app.route('/forum')
def forum():
    posts = ForumPost.view_posts()
    return render_template('forum.html', posts=posts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form submission
        return redirect(url_for('dashboard'))
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8166, debug=False)

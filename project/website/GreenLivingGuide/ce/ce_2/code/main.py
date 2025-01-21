from flask import Flask, render_template, request, redirect, session
import json

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
    def load_users() -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

class Tip:
    def __init__(self, content: str):
        self.content = content

    def save(self):
        with open('tips.txt', 'a') as f:
            f.write(f"{self.content}\n")

    @staticmethod
    def load_tips() -> list:
        tips = []
        try:
            with open('tips.txt', 'r') as f:
                for line in f:
                    tips.append(Tip(line.strip()))
        except FileNotFoundError:
            pass
        return tips

class Article:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open('articles.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}\n")

    @staticmethod
    def load_articles() -> list:
        articles = []
        try:
            with open('articles.txt', 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    articles.append(Article(title, content))
        except FileNotFoundError:
            pass
        return articles

class ForumPost:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def save(self):
        with open('forum.txt', 'a') as f:
            f.write(f"{self.username}|{self.content}\n")

    @staticmethod
    def load_posts() -> list:
        posts = []
        try:
            with open('forum.txt', 'r') as f:
                for line in f:
                    username, content = line.strip().split('|')
                    posts.append(ForumPost(username, content))
        except FileNotFoundError:
            pass
        return posts

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    tips = Tip.load_tips()
    articles = Article.load_articles()
    return render_template('dashboard.html', tips=tips, articles=articles)

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        content = request.form['content']
        new_tip = Tip(content)
        new_tip.save()
        return redirect('/tips')
    tips = Tip.load_tips()
    return render_template('tips.html', tips=tips)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_article = Article(title, content)
        new_article.save()
        return redirect('/articles')
    articles = Article.load_articles()
    return render_template('articles.html', articles=articles)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        new_post = ForumPost(session['username'], content)
        new_post.save()
        return redirect('/forum')
    posts = ForumPost.load_posts()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(port=8952, debug=False)

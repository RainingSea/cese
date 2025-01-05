from flask import Flask, render_template, request, redirect, url_for, session
from typing import List

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def validate_password(self, password: str) -> bool:
        return self.password == password

class Tip:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def save(self):
        with open('tips.txt', 'a') as f:
            f.write(f"{self.content}|{self.author}\n")

class Article:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        with open('articles.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.author}\n")

class ForumPost:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def save(self):
        with open('forum.txt', 'a') as f:
            f.write(f"{self.content}|{self.author}\n")

class App:
    def __init__(self):
        self.users: List[User] = []
        self.tips: List[Tip] = []
        self.articles: List[Article] = []
        self.forum_posts: List[ForumPost] = []
        self.load_data()

    def load_data(self):
        # Load users
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                self.users.append(User(username, password))
        
        # Load tips
        with open('tips.txt', 'r') as f:
            for line in f:
                content, author = line.strip().split('|')
                self.tips.append(Tip(content, author))
        
        # Load articles
        with open('articles.txt', 'r') as f:
            for line in f:
                title, content, author = line.strip().split('|')
                self.articles.append(Article(title, content, author))
        
        # Load forum posts
        with open('forum.txt', 'r') as f:
            for line in f:
                content, author = line.strip().split('|')
                self.forum_posts.append(ForumPost(content, author))

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.validate_password(password):
                session['username'] = username
                return True
        return False

    def register(self, username: str, password: str):
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)

    def submit_tip(self, content: str, author: str):
        new_tip = Tip(content, author)
        new_tip.save()
        self.tips.append(new_tip)

    def submit_article(self, title: str, content: str, author: str):
        new_article = Article(title, content, author)
        new_article.save()
        self.articles.append(new_article)

    def submit_forum_post(self, content: str, author: str):
        new_post = ForumPost(content, author)
        new_post.save()
        self.forum_posts.append(new_post)

app = Flask(__name__)
app.secret_key = 'supersecretkey'
application = App()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', articles=application.articles, tips=application.tips)

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if request.method == 'POST':
        content = request.form['content']
        author = application.users[0].username  # Assuming the first user in session
        application.submit_tip(content, author)
        return redirect(url_for('tips'))
    return render_template('tips.html', tips=application.tips)

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = application.users[0].username  # Assuming the first user in session
        application.submit_article(title, content, author)
        return redirect(url_for('articles'))
    return render_template('articles.html', articles=application.articles)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        content = request.form['content']
        author = application.users[0].username  # Assuming the first user in session
        application.submit_forum_post(content, author)
        return redirect(url_for('forum'))
    return render_template('forum.html', posts=application.forum_posts)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    application.register(username, password)
    return redirect(url_for('login_page'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if application.login(username, password):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(port=8026, debug=False)

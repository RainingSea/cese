from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username, password, bio=''):
        self.username = username
        self.password = password
        self.bio = bio

class Article:
    def __init__(self, article_id, content, author):
        self.id = article_id
        self.content = content
        self.author = author

class Like:
    def __init__(self, article_id, username):
        self.article_id = article_id
        self.username = username

class Comment:
    def __init__(self, article_id, username, comment):
        self.article_id = article_id
        self.username = username
        self.comment = comment

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def register(self, username, password):
        if self._user_exists(username):
            return False, "Username already exists!"
        self.users.append(User(username, password))
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True, ""

    def _user_exists(self, username):
        return any(user.username == username for user in self.users)

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def update_profile(self, username, bio):
        for user in self.users:
            if user.username == username:
                user.bio = bio
                self._save_users()
                return True
        return False

    def _save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")

class ArticleManager:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self):
        articles = []
        if os.path.exists('articles.txt'):
            with open('articles.txt', 'r') as file:
                for line in file:
                    article_id, content, author = line.strip().split('|')
                    articles.append(Article(article_id, content, author))
        return articles

    def share_article(self, username, content):
        article_id = str(len(self.articles) + 1)
        new_article = Article(article_id, content, username)
        self.articles.append(new_article)
        with open('articles.txt', 'a') as file:
            file.write(f"{article_id}|{content}|{username}\n")
        return True

    def like_article(self, article_id, username):
        with open('likes.txt', 'a') as file:
            file.write(f"{article_id}|{username}\n")
        return True

    def comment_article(self, article_id, username, comment):
        with open('comments.txt', 'a') as file:
            file.write(f"{article_id}|{username}|{comment}\n")
        return True

user_manager = UserManager()
article_manager = ArticleManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/feed')
    return "Invalid username or password!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, message = user_manager.register(username, password)
        if success:
            return redirect('/')
        else:
            return message
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        bio = request.form['bio']
        user_manager.update_profile(session['username'], bio)
    return render_template('profile.html', user=session['username'])

@app.route('/feed')
def feed():
    if 'username' not in session:
        return redirect('/')
    return render_template('feed.html', articles=article_manager.articles)

@app.route('/share', methods=['POST'])
def share():
    if 'username' not in session:
        return redirect('/')
    content = request.form['content']
    article_manager.share_article(session['username'], content)
    return redirect('/feed')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8249, debug=False)

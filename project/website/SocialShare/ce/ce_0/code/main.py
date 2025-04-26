from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

class User:
    def __init__(self, username: str, password: str, bio: str = ""):
        self.username = username
        self.password = password
        self.bio = bio

    def register(self, username: str, password: str) -> bool:
        if self._user_exists(username):
            return False
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}|{self.bio}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        users = self._load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def update_profile(self, bio: str) -> None:
        self.bio = bio
        users = self._load_users()
        with open('users.txt', 'w') as f:
            for user in users:
                if user['username'] == self.username:
                    f.write(f"{self.username}|{self.password}|{self.bio}\n")
                else:
                    f.write(f"{user['username']}|{user['password']}|{user['bio']}\n")

    def _user_exists(self, username: str) -> bool:
        users = self._load_users()
        return any(user['username'] == username for user in users)

    def _load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, bio = line.strip().split('|')
                    users.append({'username': username, 'password': password, 'bio': bio})
        except FileNotFoundError:
            pass
        return users

class Article:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def share_article(self, title: str, content: str, author: str) -> None:
        with open('articles.txt', 'a') as f:
            f.write(f"{title}|{content}|{author}\n")

class Comment:
    def __init__(self, article_id: int, comment_text: str, user: str):
        self.article_id = article_id
        self.comment_text = comment_text
        self.user = user

    def add_comment(self, article_id: int, comment_text: str, user: str) -> None:
        with open('comments.txt', 'a') as f:
            f.write(f"{article_id}|{comment_text}|{user}\n")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register(username, password):
            return redirect(url_for('login'))
        else:
            return "User already exists."
    return render_template('registration.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        bio = request.form['bio']
        # Assume current_user is set
        current_user.update_profile(bio)
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/content_share', methods=['GET', 'POST'])
def content_share():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = current_user.username  # Assume current_user is set
        article = Article(title, content, author)
        article.share_article(title, content, author)
        return redirect(url_for('discovery'))
    return render_template('content_share.html')

@app.route('/discovery')
def discovery():
    return render_template('discovery.html')

if __name__ == '__main__':
    app.run(port=8246, debug=False)

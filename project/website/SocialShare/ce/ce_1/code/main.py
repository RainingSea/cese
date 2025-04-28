from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def update_profile(self, username: str, bio: str) -> bool:
        # Placeholder for future implementation
        return True

class ContentManager:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self):
        articles = []
        if os.path.exists('articles.txt'):
            with open('articles.txt', 'r') as f:
                for line in f:
                    articles.append(line.strip())
        return articles

    def upload_article(self, username: str, content: str) -> bool:
        with open('articles.txt', 'a') as f:
            f.write(f"{username}|{content}\n")
        self.articles.append(content)
        return True

    def get_feed(self) -> list:
        return self.articles

    def like_article(self, article_id: int) -> bool:
        # Placeholder for future implementation
        return True

    def comment_article(self, article_id: int, comment: str) -> bool:
        # Placeholder for future implementation
        return True

user_manager = UserManager()
content_manager = ContentManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Registration failed. Username already exists."
    return render_template('registration.html')

@app.route('/profile')
def profile():
    # Placeholder for profile implementation
    return render_template('profile.html')

@app.route('/feed')
def feed():
    articles = content_manager.get_feed()
    return render_template('feed.html', articles=articles)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']
        content_manager.upload_article(username, content)
        return redirect(url_for('feed'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(port=8419, debug=False)
